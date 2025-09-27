import flet as ft

class EpicsView(ft.Column):
    def init(self):
        super().__init__()
        self.build()

    def build(self):
        mock_epics = [
            {"name": "001 - Autenticação", "overview": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
            {"name": "002 - Gerenciar Cursos", "overview": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
            {"name": "003 - Gerenciar Turmas", "overview": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
        ]

        epics_table = ft.DataTable(
            expand=True,
            border=ft.border.all(1, ft.Colors.WHITE24),
            border_radius=8,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.WHITE24),
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Overview", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(epic["name"])),
                        ft.DataCell(ft.Text(epic["overview"])),
                        ft.DataCell(ft.Text("Open")),
                    ],
                ) for epic in mock_epics
            ],
        )

        epics_table_container = ft.Container(
            expand=True,
            content=ft.Row(
                controls=[
                    epics_table
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
                                ft.Text("Epics", size=24, weight=ft.FontWeight.BOLD),
                                ft.FilledButton(
                                    text="New Epic",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor="#432070",
                                        color="white"
                                    )
                                )
                            ]
                        ),
                        ft.Divider(height=16, color=ft.Colors.WHITE24),
                        epics_table_container,
                    ]
                )
            )
        ]

    def populate_epics(self):
        ...