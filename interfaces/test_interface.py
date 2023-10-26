from core.interfaces import BaseInterface, InterfaceRegister


@InterfaceRegister(r'/test')
class TestInterface(BaseInterface):
    
    async def get(self):
        pass