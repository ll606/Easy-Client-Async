from pywebio.output import put_html
from dominate import tags


def put_html_scope(name: str, **kwargs):
    put_html(tags.div(id="pywebio-scope-%s" % name, **kwargs).render())
    