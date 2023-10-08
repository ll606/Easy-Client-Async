import os
from pywebio.output import put_html
from base64 import b64encode
from random import choice
from PIL import Image
from io import BytesIO


class StaticFileLoader:

    load_path: str = 'static\\'
    prefixmap: dict[str, str] = {
        'css': '<style rel="stylesheet">%s</style>',
        'js': '<script>%s</script>',
        'html': '%s'
    }

    @classmethod
    def load_background(cls):
        files = [os.path.join('static', each) for each in os.listdir('static')]
        background = [
            each for each in files 
            if each.split('.')[0].endswith('background') 
            and os.path.isfile(each)
        ]
        
        if len(background) >= 1:
            background = background[0]
        else:
            path = 'static\\background'
            if not os.path.isdir(path):
                return
            files = os.listdir(path)
            if len(files) > 0:
                background = os.path.join(path, choice(os.listdir(path)))
            else:
                return 
        
        if any(background.endswith(postfix) for postfix in ('.png', '.jpg')):
            img = Image.open(background)
            ratio = 0.3
            width, height = round(img.width*ratio), round(img.height*ratio)
            img = img.resize((width, height))
            data = BytesIO()
            img.save(data, format='jpeg')
            data = data.getvalue()
            data = b64encode(data).decode('utf8')
            background_style = {
                'overflow': 'scroll',
                'position': 'relative',
                'margin': '0px', 
                'z-index': '-99',
                'background-size': '1920px 108px',
                'background': 'url(data:image/jpeg;base64,%s)' % data
            }
            
            background_style = ';'.join('%s:%s' % (k,v) for k,v in background_style.items())
            background_style = 'body {%s}' % background_style
            
            put_html(cls.prefixmap['css'] % background_style)
    
    @classmethod
    def scan(cls) -> None:
        cls.load_background()
        for root, _, files in os.walk(cls.load_path):
            if '__pycache__' in root:
                continue
            for file in files:
                cls.load_file(os.path.join(root, file))

    @classmethod
    def load_file(cls, file: str) -> None:
        file_type: str = file.split('.')[-1]
        if file_type in {'css', 'js', 'html'}:
            prefix = cls.prefixmap.get(file_type)
            with open(file, 'r', encoding='utf8') as f:
                content = f.read()
            put_html(prefix % content)
