import flet as ft
import os


# class FileItem(ft.UserControl):
#     def __init__(self, children, data, callback):
#         self.children = children
#         self.data = data
#         self.callback = callback

#     def build(self):
#         return ft.ListTile(
#                     title=ft.Text(file.name),
#                     subtitle=ft.Row(controls=[
#                         ft.Text(file.path),
#                         ft.Text(f'{round(file.size/1000, 2)} Kb')
#                     ]),
#                     data=file.path,
#                     trailing=ft.IconButton(icon=ft.icons.REMOVE, on_click=remove),
#                     on_click= lambda e: print(e.control.data)
#                 )

class FileList(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.lv = ft.ListView(height=600)
    
    def _add(self, _):
        def remove(event):
            self.lv.controls.remove(event.control)
            self.update()

        def add_files(event):
            for file in event.files:
                # print(file.name)
                self.lv.controls.append(ft.ListTile(
                    title=ft.Text(file.name),
                    subtitle=ft.Row(controls=[
                        ft.Text(file.path),
                        ft.Text(f'{round(file.size/1000, 2)} Kb')
                    ]),
                    data=file.path,
                    # trailing=ft.IconButton(icon=ft.icons.REMOVE, on_click=remove),
                    on_click= lambda e: print(e.control.data),
                    on_long_press= remove
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
            content=ft.Column(
                controls=[
                    self.lv,
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.ADD, on_click=self._add),
                            ft.IconButton(icon=ft.icons.CLEAR_ALL, on_click=self._clear),
                        ],
                    ),
                    
                ]

        ))
    

def main(page: ft.Page):
    page.add(FileList())
    

if __name__ == '__main__':
    ft.app(target=main)