import flet as ft
from app.ui.views.new_project_view import NewProjectView
from app.ui.views.project_dashboard_view import ProjectDashboardView
from app.ui.views.project_view import ProjectView
from app.core.project_manager import ProjectManager
from app.core.workflow_manager import WorkflowManager
from app.ui.views.settings_view import SettingsView

class MainApp:
    def __init__(self, project_manager: ProjectManager, workflow_manager: WorkflowManager):
        self.project_manager = project_manager
        self.workflow_manager = workflow_manager
        self.page = None

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "TARS"
        self.page.window_width = 1200
        self.page.window_height = 800
        
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#141414"
        
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        self.page.go("/")

    def route_change(self, route):
        print(f"UI-MAIN: Mudando para a rota: {self.page.route}")
        
        self.page.views.clear()

        if self.page.route == "/":
            project_view = ProjectView(
                on_new_project_callback=lambda: self.page.go("/project/new"),
                on_open_project_callback=self.handle_open_project,
                on_settings_click_callback=lambda: self.page.go("/settings")
            )
            self.page.views.append(project_view)
            self.page.update()
            self._load_and_display_projects(project_view)


        elif self.page.route == "/settings":
            settings_view = SettingsView(
                on_save_callback=self._handle_save_settings,
                on_cancel_callback=lambda: self.page.go("/"),
                on_refresh_callback=self._handle_refresh_settings
            )
            self.page.views.append(settings_view)
            self.page.update()
            self._handle_refresh_settings(view=settings_view)
        
        
        elif self.page.route == "/project/new":
            new_project_view = NewProjectView(
                on_save_callback=self._handle_create_project,
                on_cancel_callback=lambda: self.page.go("/")
            )

            self.page.views.append(new_project_view)
            self.page.update()
      
        elif self.page.route.startswith("/project/"):
            project_id = int(self.page.route.split("/")[-1])
            self.project_manager.load_project(project_id)
            project = self.project_manager.active_project
            
            if not project:
                self.page.go("/")
                return

            dashboard_view = ProjectDashboardView(
                project_name=project.name,
                on_back_callback=lambda: self.page.go("/")
            )
            
            self.page.views.append(dashboard_view)
      

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    # Route: /

    def _load_and_display_projects(self, project_view: ProjectView):
        print("UI-MAIN: Buscando projetos no banco de dados...")
        all_projects = self.project_manager.get_all_projects()
        
        if not all_projects:
            print("UI-MAIN: Nenhum projeto real encontrado.")

        print(f"UI-MAIN: {len(all_projects)} projeto(s) encontrado(s).")
        
        project_view.populate_projects(all_projects)
        self.page.update()


    def handle_open_project(self, project_id: int):
        print(f"UI-MAIN: Usuário quer abrir o projeto com ID {project_id}.")
        self.page.go(f"/project/{project_id}")

    # Route: /settings

    def _get_initial_settings(self):
        return {
            "OPENAI_API_KEY": self.project_manager.get_setting("OPENAI_API_KEY"),
            "GOOGLE_API_KEY": self.project_manager.get_setting("GOOGLE_API_KEY"),
            "AI_PROVIDER_PREFERENCE": self.project_manager.get_setting("AI_PROVIDER_PREFERENCE"),
        }

    def _handle_refresh_settings(self, e=None, view: SettingsView = None):
        if view:
            print("UI-MAIN: Atualizando valores da tela de Configurações...")
            initial_settings = self._get_initial_settings()
            view.set_initial_values(initial_settings)
            self.page.update()

    def _handle_save_settings(self, settings_data: dict):

        print("UI-MAIN: Salvando configurações...")
        for key, value in settings_data.items():
            if value is not None: 
                self.project_manager.set_setting(key, value)
        print("UI-MAIN: Configurações salvas!")
        self.page.go("/")


    # Route: /project/new

    # def _handle_create_project(self, project_data: dict):
    #     print("UI-MAIN: Recebidos dados do formulário, criando projeto...")

    #     if project_data["name"].strip() is "" or project_data["context"].strip() is "":
    #         return

    #     try:
    #         new_project = self.project_manager.create_project(
    #             name=project_data["name"],
    #             context=project_data["context"],
    #         )
    #         print(f"UI-MAIN: Projeto '{new_project.name}' criado com sucesso.")
    #         self.page.go("/")
    #     except Exception as e:
    #         print(f"UI-MAIN: Erro ao criar projeto: {e}")
    #         # pop-up de erro para o usuário

    def _handle_create_project(self, project_data: dict):
        print("UI-MAIN: Recebidos dados do formulário para criar projeto...")
  
        required_fields = ["name", "context"]
        for field in required_fields:
            if not project_data.get(field, "").strip():
                self._show_snackbar(f"O campo '{field}' é obrigatório.")
                print("Era para mostrar snackbar")
                return 

        try:

            new_project = self.project_manager.create_project(**project_data)
            
            self._show_snackbar(f"Projeto '{new_project.name}' criado com sucesso!", color=ft.Colors.GREEN)
            
            self.page.go("/")

        except Exception as e:
            error_msg = f"Erro ao criar projeto: {e}"
            print(f"UI-MAIN: {error_msg}")
            self._show_error_dialog(error_msg)


    # -------------------------------- Utils ------------------------------


    def _show_snackbar(self, message: str, color: str = ft.Colors.RED):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color
        )
        self.page.open(self.page.snack_bar)


    def _show_error_dialog(self, error_message: str):
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ocorreu um Erro"),
            content=ft.Text(error_message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close(self.page.dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(self.page.dialog)

