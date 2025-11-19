import reflex as rx
from app.states.quiz_state import QuizState
from app.states.user_state import UserState
from app.states.location_state import LocationState


def answer_stat_card(question: dict, answer_key: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(f"Q: {question['text']}", class_name="text-sm text-gray-400 mb-2"),
        rx.el.p(
            f"You chose: {question['choices'][answer_key]['title']}",
            class_name="text-md text-[#00d4ff] mb-2",
        ),
        rx.el.p(
            f"{QuizState.user_answer_stats[question['id']]}% of nappers agree with you.",
            class_name="text-sm text-[#00ff9f]",
        ),
        class_name="p-4 bg-[#1a1a2e] pixel-border-cyan",
    )


def recommended_location_card(location: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(location["icon"], class_name="h-8 w-8 text-[#00d4ff] mr-4"),
            rx.el.div(
                rx.el.h3(
                    location["name"], class_name="text-lg text-left text-[#00ff9f]"
                ),
                rx.el.p(
                    location["description"],
                    class_name="text-xs text-left text-gray-400 mt-1",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Visit This Spot",
            rx.icon("arrow_right", class_name="ml-2 h-4 w-4"),
            on_click=lambda: LocationState.select_location(location["id"]),
            class_name="mt-4 w-full flex items-center justify-center text-sm bg-transparent text-[#ff00ff] font-bold py-2 px-4 pixel-border-magenta hover:bg-[#ff00ff]/20 transition-all duration-300",
        ),
        class_name="p-4 bg-[#1a1a2e] pixel-border-magenta flex flex-col justify-between",
    )


def results_page() -> rx.Component:
    def get_location_by_id(spot_id: str):
        return rx.foreach(
            LocationState.locations,
            lambda loc: rx.cond(
                loc["id"] == spot_id, recommended_location_card(loc), rx.fragment()
            ),
        )

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    QuizState.personality_details["icon"],
                    class_name="h-12 w-12 md:h-16 md:w-16 text-[#ff00ff] mb-4",
                ),
                rx.el.h2(
                    QuizState.personality_details["title"],
                    class_name="text-2xl md:text-4xl text-[#ff00ff] text-shadow-neon mb-4 text-center",
                ),
                rx.el.p(
                    QuizState.personality_details["description"],
                    class_name="text-center text-gray-300 leading-relaxed mb-8 text-sm md:text-base",
                ),
                class_name="flex flex-col items-center justify-center p-4 md:p-8 mb-4 md:mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Recommended Nap Spots",
                    class_name="text-xl md:text-2xl text-[#00ff9f] text-center mb-6",
                ),
                rx.el.div(
                    rx.foreach(
                        QuizState.personality_details["spots"], get_location_by_id
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-8",
                ),
            ),
            rx.el.div(
                rx.el.h3(
                    "Your Sleep Profile",
                    class_name="text-xl md:text-2xl text-[#00ff9f] text-center mb-6",
                ),
                rx.el.div(
                    rx.foreach(
                        QuizState.questions,
                        lambda question, index: answer_stat_card(
                            question, QuizState.answers[index]
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-8",
                ),
            ),
            rx.el.blockquote(
                rx.el.p(
                    f'"{UserState.random_quote}"',
                    class_name="text-center text-gray-400 italic text-sm md:text-base leading-relaxed p-4 bg-[#1a1a2e] pixel-border-cyan",
                )
            ),
            rx.el.button(
                "Try Again",
                on_click=QuizState.reset_quiz,
                class_name="mt-8 md:mt-12 mx-auto flex items-center justify-center text-base md:text-lg bg-transparent text-white font-bold py-3 px-6 md:py-4 md:px-8 border-2 border-white hover:bg-white/20 hover:scale-105 transition-all duration-300",
            ),
            class_name="w-full",
        ),
        class_name="w-full p-4 md:p-8 pixel-border bg-[#1a1a2e] animate-fade-in",
    )