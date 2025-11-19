import reflex as rx
from app.states.quiz_state import QuizState


def choice_button(
    question_index: int, choice_key: str, choice_data: dict
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.span(choice_data["emoji"], class_name="text-2xl mr-4"),
            rx.el.h3(
                choice_data["title"], class_name="text-md md:text-lg text-[#00ff9f]"
            ),
            class_name="flex items-center",
        ),
        on_click=lambda: QuizState.handle_answer(question_index, choice_key),
        class_name="w-full p-4 md:p-6 bg-[#1a1a2e] pixel-border-cyan hover:bg-[#00d4ff]/20 hover:scale-105 transition-all duration-300 text-white flex justify-start items-center",
    )


def quiz_question(question: dict, index: int) -> rx.Component:
    choices = question["choices"].entries()
    layout = question.get("layout", "row")
    return rx.el.div(
        rx.el.div(
            rx.el.p(question["part"], class_name="text-sm text-[#00d4ff] mb-2"),
            rx.el.h2(
                question["text"],
                class_name="text-lg md:text-2xl text-center text-white",
            ),
            class_name="text-center mb-8",
        ),
        rx.match(
            layout,
            (
                "row",
                rx.el.div(
                    choice_button(index, "A", question["choices"]["A"]),
                    rx.el.p(
                        "VS",
                        class_name="text-2xl text-[#ff00ff] font-bold hidden md:block",
                    ),
                    choice_button(index, "B", question["choices"]["B"]),
                    class_name="flex flex-col md:flex-row items-center justify-between gap-6 md:gap-8",
                ),
            ),
            (
                "grid",
                rx.el.div(
                    rx.foreach(
                        choices,
                        lambda choice: choice_button(index, choice[0], choice[1]),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6",
                ),
            ),
            rx.el.div(),
        ),
        class_name="w-full animate-fade-in",
    )


def progress_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            style={"width": QuizState.progress_percent},
            class_name="h-full bg-[#00ff9f] transition-all duration-500",
        ),
        rx.el.div(
            QuizState.progress_percent,
            class_name="absolute inset-0 flex items-center justify-center text-xs text-black font-bold",
        ),
        class_name="w-full h-6 bg-[#1a1a2e] pixel-border-magenta relative overflow-hidden",
    )


def quiz_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            QuizState.quiz_finished,
            rx.el.div(
                rx.el.p(
                    "Calculating your sleep persona...",
                    class_name="text-2xl text-center text-[#00ff9f]",
                ),
                class_name="flex items-center justify-center h-64",
            ),
            rx.el.div(
                progress_bar(),
                rx.el.div(
                    quiz_question(
                        QuizState.current_question, QuizState.current_question_index
                    ),
                    class_name="mt-8",
                ),
                class_name="w-full",
            ),
        ),
        class_name="w-full animate-fade-in",
    )