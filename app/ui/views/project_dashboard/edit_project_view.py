import flet as ft

class EditProjectView(ft.Column):
    def init(self):
        super().__init__()
        self.build()

    def build(self):
        name_field = ft.TextField(
            label="Name",
            value="ITL - Gerenciador de Cursos",
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8)
        )
        
        context_field = ft.TextField(
            label="Context",
            multiline=True, 
            min_lines=8, 
            max_lines=8, 
            value="Um projeto para gerenciar cursos...",
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8)
        )

        buttons_row = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=16,
            controls=[
                ft.ElevatedButton(
                    text="Cancel",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor="#2f2f35",
                        color="white"
                    )
                ),
                ft.FilledButton(
                    text="Save",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor="#432070",
                        color="white"
                    )
                )
            ]
        )

        self.controls = [
            ft.Container(
                padding=ft.padding.only(top=25, left=16, right=32, bottom=24),
                expand=True,
                content=ft.Column(
                    expand=True,
                    spacing=20,
                    controls=[
                        ft.Text("Edit Project", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=16, color=ft.Colors.WHITE24),
                        name_field,
                        context_field,
                        # Espaçador para empurrar os botões para baixo
                        ft.Container(expand=True), 
                        buttons_row
                    ]
                )
            )
        ]