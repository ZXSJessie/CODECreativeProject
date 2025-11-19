import reflex as rx
from app.states.quiz_state import QuizState, Personality
from app.states.location_state import LocationState
from app.states.user_state import UserState, Achievement


def stat_card(title: str, value: rx.Var, icon: str, border_color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-8 w-8 text-[#00d4ff]"),
            rx.el.p(title, class_name="text-sm text-gray-400"),
            class_name="flex items-center gap-4 mb-2",
        ),
        rx.el.p(value, class_name="text-3xl font-bold text-white"),
        class_name=f"p-6 bg-[#1a1a2e] {border_color}",
    )


def achievement_card(achievement: Achievement) -> rx.Component:
    is_unlocked = UserState.unlocked_achievements.contains(achievement["id"])
    return rx.el.div(
        rx.icon(
            achievement["icon"],
            class_name=rx.cond(
                is_unlocked, "h-10 w-10 text-[#ffc700]", "h-10 w-10 text-gray-600"
            ),
        ),
        rx.el.div(
            rx.el.h3(
                achievement["title"],
                class_name=rx.cond(
                    is_unlocked, "text-lg text-[#00ff9f]", "text-lg text-gray-500"
                ),
            ),
            rx.el.p(
                achievement["description"],
                class_name=rx.cond(
                    is_unlocked,
                    "text-xs text-gray-300 mt-1",
                    "text-xs text-gray-600 mt-1",
                ),
            ),
            class_name="ml-4",
        ),
        class_name=rx.cond(
            is_unlocked,
            "flex items-center p-4 bg-[#1a1a2e] pixel-border-cyan transition-all duration-300",
            "flex items-center p-4 bg-[#0f0f18] border-2 border-dashed border-gray-700",
        ),
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Your Napper Profile",
                    class_name="text-3xl md:text-4xl text-[#00d4ff] text-shadow-neon text-center mb-4",
                ),
                rx.el.p(
                    f"Sleep Persona: {QuizState.personality_details['title']}",
                    class_name="text-center text-md md:text-lg text-[#ff00ff] mb-8 md:mb-12",
                ),
            ),
            rx.el.div(
                rx.el.h3(
                    "Sleep Stats",
                    class_name="text-xl md:text-2xl text-white text-center mb-6",
                ),
                rx.el.div(
                    stat_card(
                        "Total Ratings",
                        LocationState.total_ratings_submitted,
                        "list-checks",
                        "pixel-border-cyan",
                    ),
                    stat_card(
                        "Favorite Spot",
                        LocationState.favorite_location,
                        "heart",
                        "pixel-border-magenta",
                    ),
                    stat_card(
                        "Avg. Rating Given",
                        LocationState.average_rating_given,
                        "bar-chart",
                        "pixel-border-cyan",
                    ),
                    stat_card(
                        "Completion",
                        f"{LocationState.completion_percentage}%",
                        "flag",
                        "pixel-border-magenta",
                    ),
                    class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-8 mb-8 md:mb-12",
                ),
            ),
            rx.el.div(
                rx.el.h3(
                    "Achievements Unlocked",
                    class_name="text-xl md:text-2xl text-white text-center mb-6",
                ),
                rx.el.div(
                    rx.foreach(UserState.achievements.values(), achievement_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6",
                ),
            ),
            class_name="flex flex-col items-center justify-center",
        ),
        class_name="w-full p-4 md:p-8 pixel-border bg-[#1a1a2e] animate-fade-in",
    )