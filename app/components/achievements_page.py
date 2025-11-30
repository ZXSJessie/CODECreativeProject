import reflex as rx
from app.states.user_state import UserState
from app.states.quiz_state import QuizState


def achievement_card(achievement_id: str, achievement_data: dict, unlocked: bool) -> rx.Component:
    return rx.el.div(
        # Icon Container
        rx.el.div(
            rx.icon(
                rx.cond(unlocked, achievement_data["icon"], "lock"),
                class_name=rx.cond(
                    unlocked,
                    "w-8 h-8 text-[#00ff9f]",
                    "w-8 h-8 text-gray-600",
                ),
            ),
            class_name="mr-4 flex-shrink-0 flex items-center justify-center w-12",
        ),
        # Content Container
        rx.el.div(
            rx.el.h3(
                achievement_data["title"],
                class_name="text-sm font-bold text-gray-200 uppercase tracking-wider mb-1",
            ),
            rx.el.p(
                achievement_data["description"],
                class_name="text-xs text-gray-400 mb-3 leading-relaxed",
            ),
            # Status Line
            rx.el.div(
                rx.icon(
                    rx.cond(unlocked, "check-circle", "lock"),
                    size=12,
                    class_name="mr-1"
                ),
                rx.text(rx.cond(unlocked, "UNLOCKED", "LOCKED")),
                class_name=rx.cond(
                    unlocked,
                    "text-[10px] font-bold flex items-center text-[#00ff9f] tracking-widest",
                    "text-[10px] font-bold flex items-center text-gray-600 tracking-widest",
                )
            ),
            class_name="flex flex-col flex-grow",
        ),
        class_name=rx.cond(
            unlocked,
            "flex items-start p-4 bg-[#1a1a2e]/40 backdrop-blur-sm border border-[#00ff9f]/30 hover:border-[#00ff9f] transition-all duration-300",
            "flex items-start p-4 bg-[#1a1a2e]/40 backdrop-blur-sm border border-gray-800 hover:border-gray-700 transition-all duration-300",
        ),
    )


def achievements_page() -> rx.Component:
    return rx.el.div(
        # Main Container
        rx.el.div(
            # Header Section (Green)
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left", size=16),
                        on_click=lambda: QuizState.set_page("home"),
                        class_name="p-1 border border-[#00ff9f] text-[#00ff9f] hover:bg-[#00ff9f] hover:text-black transition-colors mr-4",
                    ),
                    rx.el.div(
                        rx.el.h1("ACHIEVEMENTS", class_name="text-2xl font-bold text-[#00ff9f] tracking-widest text-shadow-neon-green"),
                        rx.el.p(
                            rx.text(UserState.unlocked_achievements_count, " / ", UserState.total_achievements_count, " UNLOCKED"),
                            class_name="text-xs text-gray-400 font-mono mt-1"
                        ),
                        class_name="flex flex-col"
                    ),
                    class_name="flex items-center"
                ),
                rx.icon("trophy", class_name="text-[#ffd700] w-8 h-8"),
                class_name="w-full border-2 border-[#00ff9f] p-4 flex justify-between items-center bg-[#1a1a2e]/40 backdrop-blur-sm mb-6"
            ),

            # Progress Section (Purple)
            rx.el.div(
                rx.el.div(
                    rx.text("COMPLETION RATE", class_name="text-xs font-bold text-gray-400 tracking-wider"),
                    rx.text(UserState.completion_percentage, "%", class_name="text-xs font-bold text-[#00ff9f]"),
                    class_name="flex justify-between mb-2"
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-full bg-[#00ff9f] transition-all duration-500",
                        style={"width": f"{UserState.completion_percentage}%"}
                    ),
                    class_name="w-full h-4 border border-[#bd00ff] bg-[#bd00ff]/10 p-0.5"
                ),
                class_name="w-full border border-[#bd00ff] p-4 bg-[#1a1a2e]/40 backdrop-blur-sm mb-8"
            ),

            # Grid
            rx.el.div(
                rx.foreach(
                    UserState.achievements,
                    lambda item: achievement_card(
                        item[0],
                        item[1],
                        UserState.unlocked_achievements.contains(item[0]),
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
            ),

            # Footer
            rx.el.div(
                rx.text("Keep grinding! ", UserState.remaining_achievements_count, " achievements remaining."),
                class_name="w-full border border-[#bd00ff] p-3 mt-8 text-center text-gray-300 text-sm font-mono bg-[#1a1a2e]/40 backdrop-blur-sm"
            ),

            class_name="max-w-4xl mx-auto w-full"
        ),
        class_name="min-h-screen retro-bg p-4 md:p-8 font-mono"
    )
