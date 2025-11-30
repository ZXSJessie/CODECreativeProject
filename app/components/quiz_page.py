import reflex as rx
from app.states.quiz_state import QuizState


def choice_button(
    question_index: int, choice_key: str, choice_data: dict
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.span(choice_data["emoji"], class_name="text-xl mr-3"),
            rx.el.h3(
                choice_data["title"], class_name="text-sm md:text-base text-gray-200 font-mono text-left"
            ),
            class_name="flex items-center",
        ),
        on_click=lambda: QuizState.handle_answer(question_index, choice_key),
        class_name="w-full p-4 bg-[#1a1a2e]/80 border-4 border-gray-700 hover:border-[#00ff9f] hover:bg-[#00ff9f]/10 transition-all duration-200 flex justify-start items-center mb-3 group",
    )


def quiz_question(question: dict, index: int) -> rx.Component:
    choices = question["choices"].entries()
    return rx.el.div(
        # Question Header
        rx.el.div(
            rx.text(f">> {question['text']} <<", class_name="text-[#00ff9f] font-bold tracking-wider text-center mb-8 font-mono"),
            class_name="w-full"
        ),
        
        # Choices
        rx.el.div(
            rx.foreach(
                choices,
                lambda choice: choice_button(index, choice[0], choice[1]),
            ),
            class_name="flex flex-col w-full max-w-2xl mx-auto",
        ),
        
        # Navigation Buttons
        rx.el.div(
            rx.el.button(
                "← BACK",
                # Logic for back button could be added to QuizState if needed, for now it's visual or could reset
                class_name="px-6 py-2 border-4 border-[#ff00ff] text-[#ff00ff] font-bold text-xs hover:bg-[#ff00ff] hover:text-black transition-colors font-mono"
            ),
            rx.el.button(
                "NEXT →",
                # Next is handled by clicking an option in the current design, but we can keep this for visual consistency or future manual navigation
                class_name="px-6 py-2 bg-[#00ff9f] text-black font-bold text-xs hover:bg-[#00ff9f]/80 transition-colors font-mono"
            ),
            class_name="flex justify-between w-full max-w-2xl mx-auto mt-8"
        ),
        
        # Tip Footer
        rx.el.div(
            rx.text("[TIP: Choose wisely. Your build determines your playstyle.]", class_name="text-[10px] text-gray-500 font-mono text-center mt-8"),
            class_name="w-full"
        ),
        
        class_name="w-full animate-fade-in flex flex-col items-center",
    )


def progress_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            style={"width": QuizState.progress_percent},
            class_name="h-full bg-gradient-to-r from-[#00ff9f] to-[#bd00ff] transition-all duration-500",
        ),
        class_name="w-full h-2 bg-[#1a1a2e] border-b-4 border-gray-800 relative overflow-hidden mb-8",
    )


def quiz_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            QuizState.quiz_finished,
            rx.el.div(
                rx.el.p(
                    "Calculating your sleep persona...",
                    class_name="text-2xl text-center text-[#00ff9f] font-mono animate-pulse",
                ),
                class_name="flex items-center justify-center h-screen bg-[#050510]",
            ),
            rx.el.div(
                # Header
                rx.el.div(
                    rx.el.h1("CHARACTER CREATION", class_name="text-xl font-bold text-[#00ff9f] tracking-widest text-shadow-neon-green text-center mb-2"),
                    rx.el.div(
                        rx.text("STAGE ", class_name="text-xs text-[#bd00ff] font-mono"),
                        rx.text(QuizState.current_question_index + 1, class_name="text-xs text-[#bd00ff] font-mono"),
                        rx.text(" / ", class_name="text-xs text-gray-500 font-mono"),
                        rx.text(QuizState.questions.length(), class_name="text-xs text-gray-500 font-mono"),
                        class_name="flex justify-center gap-1 mb-2"
                    ),
                    # Progress Squares (Visual only for now, could be dynamic)
                    rx.el.div(
                        rx.foreach(
                            QuizState.questions,
                            lambda _, i: rx.el.div(
                                class_name=rx.cond(
                                    i <= QuizState.current_question_index,
                                    "w-2 h-2 bg-[#00ff9f] mx-0.5",
                                    "w-2 h-2 bg-[#1a1a2e] border border-gray-700 mx-0.5"
                                )
                            )
                        ),
                        class_name="flex justify-center mb-4"
                    ),
                    class_name="w-full pixel-border p-4 bg-[#00ff9f]/5 mb-0 max-w-2xl mx-auto"
                ),
                
                progress_bar(),
                
                rx.el.div(
                    quiz_question(
                        QuizState.current_question, QuizState.current_question_index
                    ),
                    class_name="w-full max-w-4xl mx-auto p-4 pixel-border-purple bg-[#1a1a2e]/50 min-h-[400px] flex flex-col justify-center",
                ),
                class_name="w-full max-w-4xl mx-auto",
            ),
        ),
        class_name="min-h-screen bg-[#050510] p-4 md:p-8 font-mono flex flex-col items-center justify-center",
    )