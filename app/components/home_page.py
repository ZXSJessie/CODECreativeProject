import reflex as rx
from app.states.quiz_state import QuizState
from app.states.user_state import UserState


def home_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "The Ultimate Nap Quest",
                class_name="text-3xl md:text-4xl text-[#00d4ff] text-shadow-neon text-center mb-4",
            ),
            rx.el.p(
                "Discover your sleep persona. Uncover the best nap spots on campus. Your quest begins now.",
                class_name="text-center text-gray-300 max-w-2xl mx-auto text-sm md:text-base leading-relaxed mb-6",
            ),
            rx.el.blockquote(
                rx.el.p(
                    f'"{UserState.random_quote}"',
                    class_name="text-center text-gray-400 italic text-sm md:text-base leading-relaxed mb-12 pixel-border-magenta p-4 bg-[#1a1a2e]",
                )
            ),
            rx.el.div(
                rx.el.button(
                    "Start The Quiz",
                    rx.icon("arrow_right", class_name="ml-2 h-5 w-5"),
                    on_click=lambda: QuizState.set_page("quiz"),
                    class_name="flex items-center justify-center text-base md:text-lg bg-transparent text-[#ff00ff] font-bold py-3 px-6 md:py-4 md:px-8 pixel-border-magenta hover:bg-[#ff00ff]/20 hover:scale-105 transition-all duration-300 w-full max-w-xs",
                ),
                rx.el.button(
                    "Browse Locations",
                    rx.icon("map", class_name="ml-2 h-5 w-5"),
                    on_click=lambda: QuizState.set_page("locations"),
                    class_name="mt-6 flex items-center justify-center text-base md:text-lg bg-transparent text-[#00d4ff] font-bold py-3 px-6 md:py-4 md:px-8 pixel-border-cyan hover:bg-[#00d4ff]/20 hover:scale-105 transition-all duration-300 w-full max-w-xs",
                ),
                class_name="flex flex-col items-center",
            ),
            class_name="flex flex-col items-center justify-center",
        ),
        class_name="w-full p-4 md:p-8 pixel-border bg-[#1a1a2e] animate-fade-in",
    )