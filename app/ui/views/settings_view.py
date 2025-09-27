import flet as ft
from typing import Callable, Dict

class SettingsView(ft.View):
    def __init__(
        self,
        on_save_callback: Callable[[Dict[str, str]], None],
        on_cancel_callback: Callable,
        on_refresh_callback: Callable  

    ):
        super().__init__()

        self.bgcolor = "#141414"
        self.route = "/settings"
        
        self.on_save_callback = on_save_callback
        self.on_cancel_callback = on_cancel_callback
        self.on_refresh_callback = on_refresh_callback 


        self.build()

    def build(self):
        # --- Campos de Texto ---
        self.openai_key_field = ft.TextField(
            label="OpenAI API Key",
            hint_text="Enter your OpenAI API key",
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8)
        )
        self.gemini_key_field = ft.TextField(
            label="Gemini API Key",
            hint_text="Enter your Gemini API key",
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8)
        )

        # --- Dropdown ---
        self.model_dropdown = ft.Dropdown(
            label="Preferred AI Model",
            expand=True,
            border_color=ft.Colors.WHITE24,
            border_radius=ft.border_radius.all(8),
            options=[
                ft.dropdown.Option("OpenAI"),
                ft.dropdown.Option("Gemini"),
            ]
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
                    text="Save Settings", 
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
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    tooltip="Refresh values from database (I'm Just Testing)",
                                    on_click=lambda _: self.on_refresh_callback()
                                )
                            ]
                        ),
                        ft.Text(
                            "Configure your application settings, including API keys for AI services.",
                            color=ft.Colors.WHITE60
                        ),
                        ft.Divider(height=16, color=ft.Colors.WHITE24),
                        ft.Text("AI Configuration", size=20, weight=ft.FontWeight.W_500),
                        ft.Container(height=12),
                        self.openai_key_field,
                        ft.Container(height=12),
                        self.gemini_key_field,
                        ft.Container(height=12),
                        self.model_dropdown,
                        ft.Container(height=48), 
                        buttons_row
                    ]
                ),
            ),
        ]

    def _handle_save(self, e):
        settings_data = {
            "OPENAI_API_KEY": self.openai_key_field.value,
            "GOOGLE_API_KEY": self.gemini_key_field.value,
            "AI_PROVIDER_PREFERENCE": self.model_dropdown.value,
        }
        self.on_save_callback(settings_data)

    def set_initial_values(self, settings: Dict[str, str]):
        
        self.openai_key_field.value = settings.get("OPENAI_API_KEY", "")
        self.gemini_key_field.value = settings.get("GOOGLE_API_KEY", "")
        self.model_dropdown.value = settings.get("AI_PROVIDER_PREFERENCE", None)

        print(f"Setting Initial Values: {settings.get("OPENAI_API_KEY", "")}, {settings.get("GOOGLE_API_KEY", "")}, {settings.get("AI_PROVIDER_PREFERENCE", None)}")