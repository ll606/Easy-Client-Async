from typing import Optional, Dict, List
from pywebio.utils import random_str
from pywebio.output import put_widget, put_image
from dominate import tags
import base64

class Carousel:
    
    def __init__(
        self, 
        contents: List[Dict],
        name: Optional[str]=None,
    ) -> None:
        if name is None:
            name = random_str()
        self.name = name 
        self.contents = contents
    
    @staticmethod
    def _put_carousel_img(
        img: bytes, 
        header: Optional[str]=None, 
        subheader: Optional[str]=None,
        interval: int = 10,
        active: bool=False
    ):
        tpl = '''
<div class="carousel-item%s" data-bs-interval="%s">
    <img src="data:;base64, %s" class="d-block w-100" />
    <div class="carousel-caption d-none d-md-block">
        <h5>%s</h5>
        <p>%s</p>
    </div>
</div>
''' % (
    ' active' if active else '',
    interval*1000,
    base64.b64encode(img).decode('utf8'),
    header,
    subheader
)
        return put_widget(tpl, {})
    
    def put_carousel(self):
        def gen_buttons():
            text = ''
            for i in range(1, len(self.contents)+1):
                text += tags.button(
                    type="button",
                    data_bs_target='#%s' % self.name,
                    data_bs_slide_to='%s' % i,
                    cls='active' if i==1 else None,
                    aria_current='true' if i==1 else None,
                    aria_label='Slide %s' % i
                ).render() + '\n'
            return text
        
        tpl = '''
            <div id="%s" class="carousel slide" data-ride="carousel">
                <div class="carousel-indicators">%s</div>
                <div class="carousel-inner">
                    {{#contents}}
                        {{& pywebio_output_parse}}
                    {{/contents}}
                </div>
                <button class="carousel-control-prev" type="button" data-target="#%s" data-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-target="#%s" data-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                </button>
            </div>
            ''' % (
                self.name, gen_buttons(),
                self.name, self.name
        )
        contents = [
            self._put_carousel_img(**each)
            for each in self.contents
        ]
        return put_widget(tpl, {'contents':contents})


def main():
    with open(r'D:\project\Easy-Client-Async\static\background\00001-599503593.jpg', 'rb') as f:
        data = f.read()
    Carousel(
        [
            {'img': data, 'header': 'test', 'subheader': 'test'}
        ]
    ).put_carousel()

if __name__ == '__main__':
    main()