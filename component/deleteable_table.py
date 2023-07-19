from typing import Sequence
from pywebio.output import (
    use_scope, put_button, remove,
    put_row, put_text, put_scrollable,
    put_scope, put_collapse
)
from functools import partial
from typing import Optional, Callable, Sequence


class DeleteableTable:

    attr: dict = {}
    attr['row']: int = -1
    attr['table_count']: int = 0

    def __new__(cls, *args, **kwargs) -> 'DeleteableTable':
        instance = object.__new__(cls)
        instance.attr = cls.attr
        return instance

    def __init__(
        self, columns: int,
        margin: int = 5, margin_bottom: str = '20px',
        scope: Optional[str] = None,
        scrollable: bool = True,
        scroll_height: int = 400,
        name: str = ''
    ) -> None:
        self.attr['table_count'] += 1
        self.scope = scope
        self.columns = columns
        self.margin = margin
        self.margin_bottom = margin_bottom
        self.table_scope = 'deletable-table-%d' % self.attr['table_count']
        self.row_id: int = 0
        self.row_data = []
        self.name = name
        self.scrollable = scrollable
        self.scroll_height = scroll_height
        self.__put_layout = use_scope('full-%s' % self.table_scope, clear=True)(self.__put_layout)

    @property
    def row(self):
        self.attr['row'] += 1
        return self.attr['row']

    @row.setter
    def row(self):
        raise AttributeError('This attribute of row is read only!')

    @row.deleter
    def row(self):
        raise AttributeError('This attribute of row is read only!')
    
    def __reset_row_number(self) -> None:
        self.attr['row']: int = -1

    def add_row(
        self,
        items: Sequence,
        add_delete_button: bool = True,
        delete_callback: Optional[Callable] = None,
        centered: bool = True
    ):
        items = list(items)
        self.row_id += 1
        self.row_data.append(
            {
                'add_delete_button': add_delete_button,
                'centered': centered,
                'items': items,
                'delete_callback':delete_callback,
                'rendered': False,
                'row_id': self.row_id
            }
        )
    
    def __delete_row(self, row_id: int, row_scope: str, callback: Optional[Callable]):
        target = None
        for each in self.row_data:
            if each['row_id'] == row_id:
                target = each
                break
        if target is not None:
            self.row_data.remove(target)
        remove(row_scope)
        if callback is not None:
            if callable(callback):
                callback()
            elif isinstance(callback, Sequence) and not isinstance(callback, str):
                for func in callback:
                    func()
        

    def __add_row(
        self, items: Sequence,
        add_delete_button: bool = True,
        delete_callback: Optional[Callable] = None,
        centered: bool = True,
        row_id: int = None
    ) -> None:

        if len(items) != self.columns:
            raise ValueError(
                'The number of components must be the same as the columns!')

        content = []
        row_scope: str = '%s-%s' % (self.table_scope, self.row)

        for each in items:
            if isinstance(each, str):
                content += [put_text(each)]
            else:
                content.append(each)
            content.append(None)

        if centered:
            content = [
                each if each is None else each.style('text-align:center')
                for each in content
            ]

        if add_delete_button:
            delete_handler = partial(self.__delete_row, row_id, row_scope, delete_callback)
            content += [
                put_button('删除', delete_handler, color='danger')
            ]
        elif content[-1] is None:
            content.pop()

        num_None = content.count(None)
        margins = num_None * self.margin
        size_per_component = (100 - margins) / (len(content) - num_None)

        size = []
        for each in content:
            if each is None:
                size.append('%s%%' % self.margin)
            else:
                size.append('%s%%' % size_per_component)

        size = ' '.join(size)

        with use_scope(row_scope, clear=True):
            put_row(content=content, size=size).style(
                'margin-bottom: %s' % self.margin_bottom
            )

    def __put_layout(self):
        put_collapse(self.name, [
            put_scrollable(
                [put_scope(self.table_scope)],
                height=self.scroll_height
            )
        ], open=True)
    
    def render(self):
        if not hasattr(self, 'first_render') or self.first_render is True:
            if self.scrollable:
                if self.scope is not None:
                    with use_scope(self.scope):
                        self.__put_layout()
                else:
                    self.__put_layout()
                
            self.__add_row = use_scope(self.table_scope)(self.__add_row)
        
        self.first_render = False
        
        for kwargs in self.row_data:
            if kwargs['rendered']:
                continue
            self.__add_row(
                kwargs['items'], 
                kwargs['add_delete_button'],
                kwargs['delete_callback'],
                kwargs['centered'],
                kwargs['row_id']
            )
            kwargs['rendered'] = True

    def insert_row(
        self, at_row: int,
        items: Sequence,
        add_delete_button: bool = True,
        centered: bool = True,
        
    ):
        self.row_id += 1
        self.row_data.insert(at_row, {
            'add_delete_button': add_delete_button,
            'centered': centered,
            'items': items,
            'rendered': False,
            'row_id': self.row_id
        })