import flet as ft
from typing import Callable, Dict

class NewProjectView(ft.View):
    def __init__(
        self,
        on_save_callback: Callable[[Dict[str, str]], None],
        on_cancel_callback: Callable
    ):
        super().__init__()
        
        self.on_save_callback = on_save_callback
        self.on_cancel_callback = on_cancel_callback

        self.bgcolor = "#141414"
        self.route = "/project/new"

        self.build()

    def build(self):
        self.name_field = ft.TextField(
            label="Name",
            hint_text="Enter your Project Name",
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8)
        )
        
        self.context_field = ft.TextField(
            label="Context",
            multiline=True, 
            min_lines=8, 
            max_lines=8, 
            hint_text="Enter your Project Context",
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8)
        )

        # --- Botões ---
        buttons_row = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=16,
            controls=[
                ft.ElevatedButton(
                    text="Cancel",
                    on_click=lambda _: self.on_cancel_callback(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor="#2f2f35",
                        color="white"
                    )
                ),
                ft.FilledButton(
                    text="Confirm", 
                    on_click=self._handle_save,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor="#432070",
                        color="white"
                    )
                    
                )
            ]
        )
        
        # --- Montagem da Tela ---
        self.controls = [
            ft.Container(
                padding=ft.padding.symmetric(horizontal=192, vertical=48),
                expand=True,
                content=ft.Column( 
                    controls=[
                        # --- LINHA DO TÍTULO COM O BOTÃO DE REFRESH ---
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("New Project", size=32, weight=ft.FontWeight.BOLD),
                            ]
                        ),
                        ft.Text(
                            "Create a new project.",
                            color=ft.Colors.WHITE60
                        ),
                        ft.Divider(height=16, color=ft.Colors.WHITE24),
                        self.name_field,
                        ft.Container(height=12),
                        self.context_field,
                        ft.Container(height=48), 
                        buttons_row
                    ]
                ),
            ),
        ]

    def _handle_save(self, e):
        project_data = {
            "name": self.name_field.value,
            "context": self.context_field.value,
        }
        self.on_save_callback(project_data)

