 
from fastapi import FastAPI,UploadFile,File,Header, Depends,HTTPException,Request,Response, status as StateCodes
from fastapi.responses import RedirectResponse,HTMLResponse,PlainTextResponse
from .view import _View
 
from .config import config,ROOT_PATH,_log
import os,uuid
from hashlib import md5
from typing import Dict
from logging import Logger
import inspect
import datetime

__session_config = config.get('session') 
_session_key = "session_id"
if __session_config:
    _session_key = __session_config.get("key","session_id")
# _sessionManager = SessionManager(storage=_SESSION_STORAGES[__session_config['type']](__session_config['dir'],__session_config['secretkey']))


     
class BaseController:
     
    @property
    def log(self)->Logger:
        return _log
    @property 
    def cookies(self)->Dict[str,str]: 
        """
        cookies object
        """
        return self._cookies 
    
    @property
    def request(self)->Request :
        """currenty request object"""
        return self._request
    @property
    def flash(self):
        return self._request.session['flash']
    @flash.setter
    def flash(self,value):
        """
            set the message of once to store (it will clear on next request at finished)
        """
        self._request.state.keep_flash = True
        self._request['session']['flash'] = value
    @property
    def response(self)->Response :
        return self._response
    def __getitem__(self,key):
        """
            return the request param by name
        """
        return self.get_param(key) 
    def get_param(self,key):
        if key in self._form:
            return self._form[key]
        if key in self._json:
            return self._json[key]
        if key in self._query:
            return self._query[key]
        return None 
     
    @property
    def session(self)->Dict:
        """
            the session object
        """
        return self._session  
    @classmethod
    def redirect(self,url ,statu_code=StateCodes.HTTP_303_SEE_OTHER):
        """
        return RedirectResponse to the special URL   
        """
        return RedirectResponse(url,status_code=statu_code)
    
    def _verity_successed(self,user,redirect,msg="User authentication successed!"):
        """
        return Response for Verity successed information
        if redirect is provide,then redirect to the redirect URL
        """
        pass
        
    def _user_logout(self,msg="You are successed logout!"):
        """return Response for logout to root('/')"""
        pass

    def _verity_error(self,msg="User authentication failed!"):
        """return Response for show Verity failed infomation"""
        pass
     
    # @property
    def view(self,content:str="",view_path:str="", format:str="html", context: dict={},local2context:bool=True,**kwargs): 
        """
        return a Response by template file
        if :view_path is empty ,it's will look for current method in the view directory(offen is app dir views\controller's name)
        """
        def url_for(url:str="",type:str="static",**kws):
            url_path :str = self.__view_url__ 
            url = url.strip()
            if type!='static' or kws: #url route
                if kws:
                    url_path = ""
                    pairs = []
                    if 'app' in kws and kws['app'].strip():
                        pairs.append(kws['app'].strip())
                    if 'controller' in kws  and kws['controller'].strip():
                        pairs.append(kws['controller'].strip())
                    if 'version' in kws  and kws['version'].strip():
                        pairs.append(kws['version'].strip())
                    if 'action' in kws  and kws['action'].strip():
                        pairs.append(kws['action'].strip())
                    elif url :
                        pairs.append(url)
                    url_path = "/"+"/".join(pairs)
                    return url_path
                    pass
                else:
                        
                    url_path = self.__template_path__.replace('{controller}',self.__controller_name__).replace("{version}",self.__version__)
                    return url_path + "/" + url.strip()
            else:
                url_path += '/' + self.__controller_name__
                if self.__version__:
                    url_path += '/' + self.__version__
                return url_path + "/"  + url.strip()
            
        if content:
            if format=='html':
                return HTMLResponse(content,**kwargs)
            elif format=='text':
                return PlainTextResponse(content,**kwargs)
            else:
                return Response(content=content,**kwargs)
        def get_path(caller_frame,view_path:str="",context:dict={},local2context:bool=True ):
            # caller_file = caller_frame.f_code.co_filename
            # caller_lineno = caller_frame.f_lineno
            caller_function_name = caller_frame.f_code.co_name
            caller_locals = caller_frame.f_locals
            caller_class = caller_locals.get("self", None).__class__
            caller_classname:str = caller_class.__name__
            caller_classname = caller_classname.replace("Controller","").lower()
            #caller_file = os.path.basename(caller.filename) 
            if local2context and not context:
                del caller_locals['self']
                context.update(caller_locals)
            if not view_path:
                if self.__version__:
                    version_path = f"{self.__version__}/"
                else:
                    version_path = ""
                view_path = f"{caller_classname}/{version_path}{caller_function_name}.html" 
            return view_path,context
            
        caller_frame = inspect.currentframe().f_back
        view_path,context = get_path(caller_frame)
        
        if not 'flash' in context:
            context['flash'] = self._request.session['flash']
        template_path = os.path.join(self.__appdir__,"views")
        viewobj = _View(self._request,self._response, tmpl_path=template_path) 
        viewobj._templates.env.globals["url_for"] = url_for 
        return viewobj(view_path,context,**kwargs)
    
    async def getUploadFile(self,file:File):  
        """return the file to saved path and http URL"""
        if config.get("upload"):
            updir = config.get("upload")['dir'] or "uploads"
        else:
            updir = 'uploads'
        
        now = datetime.datetime.now().strftime("%Y%m%d")
        _save_dir = os.path.join(ROOT_PATH,updir,now) 
        if not os.path.exists(_save_dir):
            os.makedirs(_save_dir,exist_ok=True) 
        data = await file.read()
        ext = file.filename.split(".")[-1]
        md5_name = md5(data).hexdigest()
        if ext:
            md5_name+="."+ext
        save_file = os.path.join(_save_dir, md5_name) 
        if not os.path.exists(save_file): 
            f = open(save_file, 'wb') 
            f.write(data)
            f.close()
        if not updir.startswith("/"): 
            updir = updir.lstrip(".")
            if not updir.startswith("/"):
                updir="/"+updir
        url = self.request.url.scheme + "://" + self.request.url.netloc + '/'.join([updir,now,md5_name])
        return save_file,url
    async def _constructor(base_controller_class,request:Request,response:Response):  
   
        
        if not _session_key in request.cookies or not request.cookies[_session_key]:
            request.cookies[_session_key] = str(uuid.uuid4())

         
        base_controller_class._request:Request = request
        base_controller_class._response:Response = response 
        base_controller_class._cookies:Dict[str,str] = request.cookies.copy()
        # base_controller_class._session = await  _sessionManager.initSession(request,response )
        base_controller_class._session = request.session
         
        params = {}
        form_params = {}
        query_params = {}
        json_params = {}
        try:
            form_params =  await  request.form()
        except Exception as e:
            _log.info("while parse form raised:"+str(e.args))
            pass

        
        try:
            json_params =  await  request.json()
        except:
            pass
        query_params = request.query_params
        base_controller_class._form = form_params
        base_controller_class._query = query_params
        base_controller_class._json = json_params
        base_controller_class._params = params
        def __init_flash(request:Request): 
            request.state.keep_flash = False 
            if 'flash' not in request.session:
                request.session['flash'] ='' 
            
        __init_flash(request=request) 
        
    async def _deconstructor(base_controller_class,new_response:Response):  
        
        def process_cookies(response:Response, cookies,old_cookies):
            
            for key in cookies: 
                if   key != _session_key: 
                    response.set_cookie(key,cookies[key])
            for key in old_cookies:
                if not key in cookies and key != _session_key:
                    response.set_cookie(key=key,value="",max_age=0)   
            response.set_cookie(key=_session_key,
                                value=base_controller_class._request.cookies[_session_key],
                                max_age = 14 * 24 * 60 * 60,  # 14 days, in seconds
                                path  = "/",
                                samesite  = "lax",
                                httponly  = False ) 
            
        if new_response:
            process_cookies(new_response,base_controller_class._cookies,base_controller_class._request.cookies)

        def __clear_flash(request:Request):
            if not request.state.keep_flash:
                request.session['flash'] = ''
        __clear_flash(base_controller_class._request)
         

    
        
         