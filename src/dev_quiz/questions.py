import flet as ft
import json
import os

def load_questions():
    file_path = os.path.join(os.path.dirname(__file__), "questions.json")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def show_quiz_screen(page: ft.Page):
    page.clean()
    page.current_question = 0
    page.score = 0

    questions = load_questions()

    animated_question = ft.AnimatedSwitcher(
        content=ft.Text(""),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
        reverse_duration=300
    )

    options_container = ft.Column(spacing=10)

    next_button = ft.ElevatedButton(
        "Próxima",
        visible=False,
        opacity=0,
        animate_opacity=300
    )

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda _: go_back(),
        tooltip="Voltar ao menu"
    )

    header = ft.Container(
        content=ft.Row(
            controls=[
                back_button,
                ft.Icon(name=ft.Icons.PSYCHOLOGY, color=ft.Colors.GREEN_600, size=40),
                ft.Text("Dev Quiz", size=28, weight="bold", color=ft.Colors.GREEN_700),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor=ft.Colors.GREEN_50,
        border_radius=10
    )

    def show_question():
        question = questions[page.current_question]

        animated_question.content = ft.Text(
            question["question"],
            size=24,
            weight="bold",
            color=ft.Colors.PRIMARY,
            key=str(page.current_question),
        )

        animated_question.update()

        options_container.controls.clear()
        for idx, opt in enumerate(question["options"]):
            btn = ft.ElevatedButton(
                text=opt,
                width=500,
                on_click=lambda e, i=idx: on_option_click(i),
                data=idx
            )
            container = ft.Container(
                content=btn,
                bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                border_radius=8,
                padding=5,
                data=idx
            )
            options_container.controls.append(container)

        next_button.visible = False
        next_button.opacity = 0
        next_button.update()
        page.update()

    def on_option_click(selected_idx):
        question = questions[page.current_question]
        correct_idx = question["answer"]

        for container in options_container.controls:
            btn = container.content
            btn.disabled = True
            if container.data == correct_idx:
                container.bgcolor = ft.Colors.GREEN_400
            elif container.data == selected_idx:
                container.bgcolor = ft.Colors.RED_400

        if selected_idx == correct_idx:
            page.score += 1

        next_button.visible = True
        next_button.opacity = 1
        page.update()

    def next_question(e):
        if page.current_question < len(questions) - 1:
            page.current_question += 1
            show_question()
        else:
            show_result()

    def show_result():
        page.clean()
        result_msg = ft.Text(
            f"Você acertou {page.score} de {len(questions)} perguntas!",
            size=30,
            weight="bold",
            color=ft.Colors.BLUE_600
        )
        restart_btn = ft.ElevatedButton("Recomeçar", on_click=lambda e: restart_quiz())
        back_to_menu = ft.TextButton("⬅️ Voltar ao Menu", on_click=lambda _: go_back())
        page.add(header, ft.Divider(), result_msg, restart_btn, back_to_menu)

    def restart_quiz():
        page.current_question = 0
        page.score = 0
        page.clean()
        page.add(
            header,
            ft.Divider(thickness=2),
            animated_question,
            ft.Divider(),
            options_container,
            next_button,
        )
        show_question()

    def go_back():
        import main
        main.main(page)

    next_button.on_click = next_question

    page.add(
        header,
        ft.Divider(thickness=2),
        animated_question,
        ft.Divider(),
        options_container,
        next_button,
    )

    show_question()

