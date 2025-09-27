# app/ui/views/project_dashboard/context_files_view.py
import flet as ft

class ContextFilesView(ft.Column):
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):
        files_table = ft.DataTable(
            expand=True,
            border=ft.border.all(1, ft.Colors.WHITE24),
            border_radius=8,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.WHITE24),
            columns=[
                ft.DataColumn(ft.Text("File Name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("File Size", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Updated", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Need New Index in DB?", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Regras de Negócio - ADM.docx")), ft.DataCell(ft.Text("13.32mb")),
                    ft.DataCell(ft.Text("sep 5, 13:23")), ft.DataCell(ft.Text("YES", color=ft.Colors.ORANGE)),
                    ft.DataCell(ft.Text("Open"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Regras de Negócio - SI.docx")), ft.DataCell(ft.Text("9.45mb")),
                    ft.DataCell(ft.Text("sep 5, 13:23")), ft.DataCell(ft.Text("NO", color=ft.Colors.GREEN)),
                    ft.DataCell(ft.Text("Open"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Histórias de Usuários.txt")), ft.DataCell(ft.Text("3.21mb")),
                    ft.DataCell(ft.Text("sep 5, 13:23")), ft.DataCell(ft.Text("YES", color=ft.Colors.ORANGE)),
                    ft.DataCell(ft.Text("Open"))
                ]),
            ],
        )



        files_table_container = ft.Container(
            expand=True,
            content=ft.Row(
                controls=[
                    files_table
                ]
            )
        )


        self.controls = [
            ft.Container(
                padding=ft.padding.only(top=25, left=16, right=32, bottom=24),
                expand=True,
                content=ft.Column(
                    expand=True,
                    spacing=20,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Context Files", size=24, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton(
                                    "Reload Vector DB",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor="#2f2f35",
                                        color="white"
                                    )
                                )
                            ]
                        ),
                        ft.Divider(height=16, color=ft.Colors.WHITE24),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Indexed Files", weight=ft.FontWeight.BOLD, size=16),
                                ft.FilledButton(
                                    "Add File",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor="#432070",
                                        color="white"
                                    )
                                )
                            ]
                        ),
                        files_table_container
                    ]
                )
            )
        ]




        # self.projects_table = ft.DataTable(
        #     expand=True,
        #     divider_thickness=1,
        #     border_radius=10,
        #     border=ft.border.all(.5, ft.Colors.WHITE70),
        #     columns=[
        #         ft.DataColumn(ft.Text("Project Name", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE70)),
        #         ft.DataColumn(ft.Text("Overview", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE70)),
        #         ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE70)),
        #     ],
        #     rows=[]
        # )


    # def populate_projects(self, projects: List[Project]):
    #     new_rows = []
        
    #     for p in projects:
    #         new_rows.append(
    #             ft.DataRow(
    #                 cells=[
    #                     ft.DataCell(ft.Text(p.name, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)),
    #                     ft.DataCell(ft.Text(p.context, color=ft.Colors.WHITE60, no_wrap=False)), 
    #                     ft.DataCell(
    #                         ft.Text("Open", weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
    #                         on_tap=lambda _, pid=p.id: self.on_open_project_callback(pid)
    #                     )
    #                 ]
    #             )
    #         )

    #     print(f"DEBUG: Conteúdo de new_rows: {new_rows}")
        
    #     self.projects_table.rows = new_rows
