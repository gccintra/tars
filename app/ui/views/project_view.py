# app/ui/views/project_view.py
import flet as ft
from typing import List, Callable
from app.database.models import Project

class ProjectView(ft.View):
    def __init__(
        self,
        on_new_project_callback: Callable,
        on_open_project_callback: Callable,
        on_settings_click_callback: Callable
    ):
        super().__init__()

        self.bgcolor = "#141414"
        self.route = "/"
        
        self.on_new_project_callback = on_new_project_callback
        self.on_open_project_callback = on_open_project_callback
        self.on_settings_click_callback = on_settings_click_callback


        self.build()

    def build(self):

        action_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("TARS", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.SETTINGS_OUTLINED, 
                            icon_color=ft.Colors.WHITE54,
                            on_click=lambda _: self.on_settings_click_callback()
                        ),
                        ft.IconButton(icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED, icon_color=ft.Colors.WHITE54),
                    ]
                )
            ]
        )

        header =  ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Projects", size=32, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    text="New Project",
                    on_click=lambda _: self.on_new_project_callback(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor="#2f2f35",
                        color="white"
                    )
                )
            ]
        )

        self.projects_table = ft.DataTable(
            expand=True,
            border=ft.border.all(1, ft.Colors.WHITE24),
            border_radius=8,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.WHITE24),
            columns=[
                ft.DataColumn(ft.Text("Project Name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Overview", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ],
            rows=[]
        )

        action_bar_container = ft.Container(
            content=action_bar,
            padding=ft.padding.symmetric(horizontal=32, vertical=16),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.WHITE12))
        )

        table_container = ft.Container(
            expand=True,
            content=ft.Row( 
                controls=[
                    self.projects_table 
                ]
            )
        )

        main_content_container = ft.Container(
            padding=ft.padding.symmetric(horizontal=96, vertical=48),
            content=ft.Column(
                spacing=24,
                controls=[
                    header,
                    table_container 
                ]
            )
        )

        self.controls = [
            action_bar_container,
            main_content_container    
        ]

    def populate_projects(self, projects: List[Project]):
        new_rows = []
        
        for p in projects:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.name, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(p.context, color=ft.Colors.WHITE60, no_wrap=False)), 
                        ft.DataCell(
                            ft.Text("Open", weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                            on_tap=lambda _, pid=p.id: self.on_open_project_callback(pid)
                        )
                    ]
                )
            )

        print(f"DEBUG: Conteúdo de new_rows: {new_rows}")
        
        self.projects_table.rows = new_rows
