from component.absctract_form_handler import BaseFormHandler
from component.put_input import put_input
from .login_manager import LoginManager
from pywebio.pin import pin
from pywebio.output import put_error, put_success, use_scope


class LoginViewHandler(BaseFormHandler):
    
    def __init__(self) -> None:
        self.title = '登录'
        self.style = {
            'margin-top': '100px', 
            'margin-left': '27.5%',
            'margin-right': '27.5%',
            'width': '45%'
        }
        
    async def all_inputs_valid(self):
        return await LoginManager().validate_user(
            await pin['username'], await pin['password'])
    
    def error_reminder(self):
        with use_scope('head-message', clear=True):
            put_error('用户或密码错误！', closable=True)
            
    async def result(self) -> str:
        username = await pin['username']
        
        with use_scope('head-message', clear=True):
            put_success('欢迎回来! %s.' % username, closable=True)
        
        return username
    
    def __call__(self) -> None:
        put_input(
            name='username', 
            label='用户名',
        )
        
        put_input(
            name='password',
            label='密码',
            type='password'
        )
        
        return False