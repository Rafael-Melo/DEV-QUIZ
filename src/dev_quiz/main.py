import flet as ft
import questions  # Importa o arquivo do quiz

def main(page: ft.Page):
    page.title = "Dev Quiz"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 540
    page.window.height = 720
    page.padding = 20

    from questions import load_questions

    questions = load_questions()

    def start_game(e):
        page.clean()
        questions.quiz_page(page)  # chama a função do jogo

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        page.update()

    def exit_app(e):
        page.window.destroy()

    logo = ft.Text("🧠 Dev Quiz", size=40, weight="bold", color=ft.Colors.GREEN_600)

    start_button = ft.ElevatedButton("Iniciar Jogo", on_click=start_game, width=300)
    theme_button = ft.ElevatedButton("Alterar Tema", on_click=toggle_theme, width=300)
    exit_button = ft.ElevatedButton("Sair", on_click=exit_app, width=300)

    controls = ft.Column(
        [
            logo,
            ft.Divider(height=30, color="transparent"),
            start_button,
            theme_button,
            exit_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(controls)

ft.app(target=main)
