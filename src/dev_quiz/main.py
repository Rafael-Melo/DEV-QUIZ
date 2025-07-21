import flet as ft

questions = [
    {
        "question": "What does HTML stand for?",
        "options": [
            "Hyperlinks and Text Markup Language",
            "Home Tool Markup Language",
            "HyperText Markup Language"
        ],
        "answer": 2
    },
    {
        "question": "Which Python keyword is used to define a function?",
        "options": ["def", "function", "define"],
        "answer": 0
    },
    {
        "question": "Which one is a frontend framework?",
        "options": ["Django", "Flask", "React"],
        "answer": 2
    }
]

def main(page: ft.Page):
    page.title = "Dev Quiz"
    page.padding = 20
    page.current_question = 0
    page.score = 0

    question_text = ft.Text(size=24, weight="bold")
    options_container = ft.Column(spacing=10)
    next_button = ft.ElevatedButton("Próxima", visible=False)

    header = ft.Row(
        controls=[
            ft.Icon(name=ft.Icons.PSYCHOLOGY, color=ft.Colors.GREEN_600, size=40),
            ft.Text("Dev Quiz", size=32, weight="bold", color=ft.Colors.GREEN_700),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )


    def show_question():
        question = questions[page.current_question]
        question_text.value = question["question"]
        options_container.controls.clear()

        for idx, opt in enumerate(question["options"]):
            btn = ft.ElevatedButton(
                text=opt,
                width=500,
                on_click=lambda e, i=idx: on_option_click(i),
                data=idx
            )
            options_container.controls.append(btn)

        next_button.visible = False
        page.update()

    # Lógica ao clicar em uma opção
    def on_option_click(selected_idx):
        question = questions[page.current_question]
        correct_idx = question["answer"]

        for btn in options_container.controls:
            btn.disabled = True
            if btn.data == correct_idx:
                btn.bgcolor = ft.Colors.GREEN_400
            elif btn.data == selected_idx:
                btn.bgcolor = ft.Colors.RED_400

        # Marca ponto se acertar
        if selected_idx == correct_idx:
            page.score += 1

        next_button.visible = True
        page.update()

    # Avança para próxima pergunta ou finaliza quiz
    def next_question(e):
        if page.current_question < len(questions) - 1:
            page.current_question += 1
            show_question()
        else:
            show_result()

    # Mostra o resultado final
    def show_result():
        page.clean()
        msg = ft.Text(
            f"Você acertou {page.score} de {len(questions)} perguntas!",
            size=30,
            weight="bold",
            color=ft.Colors.BLUE_600
        )
        page.add(msg)

    next_button.on_click = next_question

    page.add(
        header,
        ft.Divider(thickness=2),
        question_text,
        ft.Divider(),
        options_container,
        next_button,
    )

    show_question()

ft.app(target=main)