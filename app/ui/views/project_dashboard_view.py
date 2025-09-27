import flet as ft
from .project_dashboard.epics_view import EpicsView
from .project_dashboard.context_files_view import ContextFilesView
from .project_dashboard.edit_project_view import EditProjectView

class ProjectDashboardView(ft.View):
    def __init__(self, project_name: str, on_back_callback):
        super().__init__()
        self.bgcolor = "#141414"

        
        self.project_name = project_name
        self.on_back_callback = on_back_callback

        self.nav_panel = self._create_custom_navigation_panel()
        
        self.content_area = ft.Column(expand=True, alignment=ft.MainAxisAlignment.START)

        self.controls = [
            ft.Row(
                [
                    self.nav_panel,
                    ft.VerticalDivider(width=16, color=ft.Colors.WHITE24),
                    self.content_area,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ]


    def _create_custom_navigation_panel(self):
        self.nav_item_epics = self._create_nav_item("Epics", ft.Icons.BOOK_OUTLINED, 0)
        self.nav_item_files = self._create_nav_item("Context Files", ft.Icons.FOLDER_OUTLINED, 1)
        self.nav_item_edit = self._create_nav_item("Edit Project", ft.Icons.EDIT_OUTLINED, 2)

        return ft.Container(
            padding=ft.padding.only(top=24, left=16),
            content=ft.Column(
                width=250,
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.on_back_callback(), icon_color="#ffffff"),
                            ft.Text(self.project_name, size=14, weight=ft.FontWeight.BOLD, expand=True)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(height=24, color=ft.Colors.WHITE24),
                    self.nav_item_epics,
                    self.nav_item_files,
                    self.nav_item_edit,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def _create_nav_item(self, text, icon_name, index):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="#ffffff"),
                    ft.Text(text)
                ],
                spacing=20
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            border_radius=ft.border_radius.all(8),
            on_click=lambda e, idx=index: self._change_view(idx),
            data=index 
        )
    
    def _update_nav_selection(self, selected_index: int):
        for item in [self.nav_item_epics, self.nav_item_files, self.nav_item_edit]:
            if item.data == selected_index:
                item.bgcolor = ft.Colors.WHITE10 
            else:
                item.bgcolor = ft.Colors.TRANSPARENT
        
    def _change_view(self, index):
        self._update_nav_selection(index)

        self.content_area.controls.clear()
        if index == 0:
            self.content_area.controls.append(EpicsView())
        elif index == 1:
            self.content_area.controls.append(ContextFilesView())
        elif index == 2:
            self.content_area.controls.append(EditProjectView())
            
        self.update()