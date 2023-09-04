import flet as ft
from datetime import datetime

class FileItem(ft.ListTile):
    def __init__(self, remove_item, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.trailing=ft.IconButton(icon=ft.icons.REMOVE, on_click=self.delete)
        self.remove_item = remove_item

    def delete(self, e):
        self.remove_item(self)

class FileList(ft.UserControl):
    def __init__(self, height, click_item):
        super().__init__()
        self.height = height
        self.lv = ft.ListView(expand=True)
        self.click_item = click_item
    
    def _add(self, _):
        def remove(item):
            self.lv.controls.remove(item)
            self.update()

        def add_files(event):
            for file in event.files:
                self.lv.controls.append(FileItem(
                    title=ft.Text(file.name, size=16),
                    subtitle=ft.Row(controls=[
                        # ft.Text(file.path),
                        ft.Text(f'{round(file.size/1000, 2)} Kb', size=12)
                    ]),
                    data=file.path,
                    on_click=self.click_item,
                    remove_item=remove
                ))
            self.update()

        file_picker = ft.FilePicker(on_result=add_files)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=True)
    
    def _clear(self, _):
        self.lv.controls.clear()
        self.update()
        

    def build(self):
        return ft.Container(
            height=self.height,
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.IconButton(icon=ft.icons.ADD, on_click=self._add),
                            ft.IconButton(icon=ft.icons.CLEAR_ALL, on_click=self._clear),
                        ],
                    ),
                    self.lv,
                ]

        ))
    

def main(page: ft.Page):
    page.add(FileList(height=800))
    

if __name__ == '__main__':
    ft.app(target=main)