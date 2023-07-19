from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse
import json

class LoginManager:
    
    def __new__(cls) -> 'LoginManager':
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls)
        return cls.instance
    
    async def validate_user(self, username: str, password: str):
        '''
        ```python
            if not hasattr(self.__class__, 'session'):
                self.__class__.session = AsyncHTTPClient()
            
            data = {
                    'username': username,
                    'password': password
                }
            data_string = json.dumps(data)
            request = HTTPRequest(
                'http://localhost:8080/login', 
                method='POST', 
                body=data_string
            )
            
            response: HTTPResponse = await self.session.fetch(request)
            return json.loads(response.body.decode())['result']
        ```
        '''
        return True
    
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()