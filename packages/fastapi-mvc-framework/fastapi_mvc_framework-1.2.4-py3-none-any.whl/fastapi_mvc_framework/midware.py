import os,time,typing
from fastapi import FastAPI, HTTPException,exceptions,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,FileResponse,Response
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
from .config import _log,config
from .midware_session import (SessionMiddleware,FileStorage,MemoryStorage,RedisStorage,SessionStorage,_SESSION_STORAGES)
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import   Scope 
from .view import _View
from .config import config
class MvcStaticFiles(StaticFiles):
    pass
    # def get_path(self, scope: Scope) -> str:
    #     """
    #     Given the ASGI scope, return the `path` string to serve up,
    #     with OS specific path separators, and any '..', '.' components removed.
    #     """
    #     return os.path.normpath(os.path.join(*scope["path"].split("/")))
    
    # def lookup_path(
    #     self, path: str
    # ) -> typing.Tuple[str, typing.Optional[os.stat_result]]:
    #     for directory in self.all_directories:
    #         joined_path = os.path.join(directory, path)
    #         if self.follow_symlink:
    #             full_path = os.path.abspath(joined_path)
    #         else:
    #             full_path = os.path.realpath(joined_path)
    #         directory = os.path.realpath(directory)
    #         if os.path.commonprefix([full_path, directory]) != directory:
    #             # Don't allow misbehaving clients to break out of the static files
    #             # directory.
    #             continue
    #         try:
    #             return full_path, os.stat(full_path)
    #         except (FileNotFoundError, NotADirectoryError):
    #             continue
    #     return "", None

def init(app :FastAPI,debug:bool = False):
    async def on_startup():
        pass
    app.router.on_startup = [on_startup]
    
    cors_cfg = config.get("cors")
    if cors_cfg:
        app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_cfg.get('allow_origins'),
        allow_credentials=cors_cfg.get("allow_credentials"),
        allow_methods=cors_cfg.get("allow_methods",["*"]),
        allow_headers=cors_cfg.get("allow_headers",["*"]),
        )
    __roots = {}
    for _dir  in  app._app_views_dirs: 
        _url = app._app_views_dirs[_dir] 
        if not _url.startswith('/'):
            _url='/'+_url
        _dir=_dir.replace("\\",'/')
        if _url=='/':
            __roots[_dir] = _url
        else:
            app.mount(_url,MvcStaticFiles(directory=_dir),name=_dir)       
        #mount public resources
    public_dir =  os.path.abspath(config.get("public_dir" ) )
    if not os.path.exists(public_dir):
        os.mkdir(public_dir) 
    app.mount('/public',  StaticFiles(directory=public_dir), name='public')

    if config.get("upload"):
            updir = config.get("upload")['dir'] or "uploads"
    else:
        updir = 'uploads'
    app.mount('/uploads',  StaticFiles(directory=updir), name='uploads')
    
    for _dir in __roots:
        app.mount(__roots[_dir],MvcStaticFiles(directory=_dir),name=_dir)
    
    #session midware
    _session_cfg:typing.Dict = config.get("session")
    _session_options = {}
    if _session_cfg:
        _storageType=_session_cfg.get("type","")
        if _storageType!="":
            if _storageType=='file':
                _session_options["storage"] = _SESSION_STORAGES[_storageType](dir=_session_cfg.get("dir","./sessions"))
            else:
                _session_options["storage"] = _SESSION_STORAGES[_storageType]()
            
        _session_options['secret_key'] = _session_cfg.get("secret_key","") 
    app.add_middleware(SessionMiddleware,**_session_options)

    def error_page(code:int,request,e):
        page = config.get(f"error_{code}_page")
        if page and os.path.exists(page):
            viewObj = _View(request=request,response=None,tmpl_path=os.path.abspath(os.path.dirname(page)))
            file = os.path.basename(page)
            content=[]
            if debug:
                exc_traceback = e.__traceback__ 
                # show traceback the last files and location
                tb_summary = traceback.extract_tb(exc_traceback) 
                
                for filename, line, func, text in tb_summary: 
                    content.append(f"{filename}:{line} in {func}") 
                 
            context = {'error':e,'debug':debug,'debug_info':content}
            
            return viewObj(file,context,status_code=404)
        return None
    
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, e:StarletteHTTPException):
        
        ret = error_page(404,request=request,e=e)
        if ret:
            return ret
        else:
            content = "<h1>404 Not Found(URL Exception)</h1>"
            content += '<h3>please check url</h3>'
            if debug:
                content += '<p>' + str(e.detail) + '</p>'
            return HTMLResponse(content=content, status_code=404)
   
    @app.exception_handler(Exception)
    async def validation_exception_handler(request, e:Exception):
        ret = error_page(500,request=request,e=e)
        if ret:
            return ret
        else:
            content = "<h1>500 Internal Server Error</h1>"
            if debug: 
                exc_traceback = e.__traceback__ 
                # show traceback the last files and location
                tb_summary = traceback.extract_tb(exc_traceback) 
                content += '<p>'
                for filename, line, func, text in tb_summary: 
                    content += (f"{filename}:{line} in {func}</br>") 
                content += '</p>'
                content += '<p>Error description:' + str(e.args)  + '</p>'
            return HTMLResponse(content=content, status_code=500)


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        _log.error(f"OMG! The client sent invalid data!: {exc}")
        return await request_validation_exception_handler(request, exc)

    @app.route('/public/error_404.html',['GET','POST','HEAD','OPTION','PUT','DELETE'])
    def _error1(request):
        raise HTTPException(404,"Not Found.")
        # return Response(content = None,status_code= 404)
    @app.route('/public/error_500.html',['GET','POST','HEAD','OPTION','PUT','DELETE'])
    def _error2(request):
        raise HTTPException(404,"Not Found.")
    

    #/favicon.ico
    @app.get("/favicon.ico")
    def _get_favicon():
        if os.path.exists("./public/favicon.ico"): 
            return FileResponse("./public/favicon.ico")
        else:
            return Response(content = None,status_code= 404)
        
    @app.middleware("http")
    async def preprocess_request(request: Request, call_next):
        # _log.debug(f"dispatch on preprocess_request")
        if debug:
            start_time = time.time() 
        #pre call to controller method
        response:Response = await call_next(request)

        if debug:
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)  
        return response 
    
    