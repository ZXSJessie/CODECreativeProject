import reflex as rx
from typing import TypedDict, Literal, cast
import random


class Achievement(TypedDict):
    id: str
    title: str
    description: str
    icon: str


class UserState(rx.State):
    achievements: dict[str, Achievement] = {
        "5-star-sleeper": {
            "id": "5-star-sleeper",
            "title": "5-Star Sleeper",
            "description": "Rate a single location with a perfect 5-star score in all categories.",
            "icon": "star",
        },
        "secret-spot-explorer": {
            "id": "secret-spot-explorer",
            "title": "Secret Spot Explorer",
            "description": "Submit ratings for at least 3 different nap spots.",
            "icon": "map-pin",
        },
        "all-area-conqueror": {
            "id": "all-area-conqueror",
            "title": "All-Area Conqueror",
            "description": "Leave your mark by rating all available nap locations.",
            "icon": "crown",
        },
        "nap-legend": {
            "id": "nap-legend",
            "title": "Nap Legend",
            "description": "Complete the personality quiz and rate every single location. A true master of rest.",
            "icon": "shield-check",
        },
    }
    unlocked_achievements: set[str] = set()
    quotes: list[str] = [
        "To sleep, perchance to dream... ay, there's the rub... for in that sleep of death what dreams may come? Or, y'know, just drool on your textbook.",
        "The best bridge between despair and hope is a good night's sleep. Or a really, really good nap in the library.",
        "I think, therefore I am... tired.",
        "I have a dream... that one day I will get 8 full hours of sleep.",
        "Is it a crime to be this tired? Asking for a friend.",
        "My bed is a magical place where I suddenly remember everything I was supposed to do.",
        "They say 'go big or go home' as if going home to nap isn't a big win.",
        "I'm not a morning person or a night owl. I'm some form of permanently exhausted pigeon.",
        "If you love someone, let them sleep.",
        "Sleep is the best meditation. Also, it's a great way to avoid responsibilities.",
        "I've reached that age where my train of thought often leaves the station without me.",
        "Why fall in love when you can fall asleep?",
        "The only thing getting lit this weekend are my scented candles for a pre-nap vibe.",
        "A day without a nap is like... just kidding, I have no idea.",
        "I'm not lazy, I'm on energy-saving mode.",
        "Reality is a construct, and I'm constructing a nap.",
    ]

    @rx.event
    def unlock_achievement(self, achievement_id: str):
        if achievement_id not in self.unlocked_achievements:
            self.unlocked_achievements.add(achievement_id)
            achievement = self.achievements[achievement_id]
            return rx.toast(
                rx.el.div(
                    rx.icon(achievement["icon"], class_name="mr-2"),
                    f"Achievement Unlocked: {achievement['title']}",
                    class_name="flex items-center",
                ),
                duration=5000,
            )

    @rx.var
    def random_quote(self) -> str:
        return random.choice(self.quotes)

    @rx.var
    def unlocked_achievements_list(self) -> list[Achievement]:
        return [self.achievements[id] for id in self.unlocked_achievements]