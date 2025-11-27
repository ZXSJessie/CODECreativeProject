import reflex as rx
from app.states.user_state import UserState
from app.states.quiz_state import QuizState


def achievement_card(achievement_id: str, achievement_data: dict, unlocked: bool) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                achievement_data["icon"],
                class_name=rx.cond(
                    unlocked,
                    "w-8 h-8 mb-2 text-[#ffd700]",
                    "w-8 h-8 mb-2 text-gray-600",
                ),
            ),
            rx.el.h3(
                achievement_data["title"],
                class_name=rx.cond(
                    unlocked,
                    "text-sm md:text-base font-bold mb-1 text-[#ffd700]",
                    "text-sm md:text-base font-bold mb-1 text-gray-500",
                ),
            ),
            rx.el.p(
                rx.cond(
                    unlocked,
                    achievement_data["description"],
                    "??? (Keep exploring to unlock)",
                ),
                class_name="text-xs text-gray-400 text-center",
            ),
            class_name="flex flex-col items-center justify-center h-full",
        ),
        class_name=rx.cond(
            unlocked,
            "p-4 relative overflow-hidden transition-all duration-300 pixel-border-yellow bg-[#ffd700]/10 hover:scale-105",
            "p-4 relative overflow-hidden transition-all duration-300 pixel-border bg-[#1a1a2e] opacity-70 grayscale hover:scale-105",
        ),
    )


def achievements_page() -> rx.Component:
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.button(
                "◀ BACK",
                on_click=lambda: QuizState.set_page("home"),
                class_name="text-[#00ff9f] hover:text-white font-bold text-sm mb-4 self-start",
            ),
            rx.el.h2(
                "TROPHY ROOM",
                class_name="text-3xl md:text-4xl text-[#ffd700] text-shadow-neon text-center mb-2",
            ),
            rx.el.p(
                "Collect them all to become the ultimate Nap Master.",
                class_name="text-gray-400 text-center text-xs md:text-sm mb-8 font-mono",
            ),
            class_name="flex flex-col items-center w-full",
        ),

        # Achievements Grid
        rx.el.div(
            rx.foreach(
                UserState.achievements,
                lambda item: achievement_card(
                    item[0],
                    item[1],
                    UserState.unlocked_achievements.contains(item[0]),
                ),
            ),
            class_name="grid grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-4xl",
        ),

        class_name="w-full p-4 md:p-8 flex flex-col items-center animate-fade-in min-h-screen",
    )
