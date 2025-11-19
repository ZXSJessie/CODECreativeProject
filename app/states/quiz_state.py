import reflex as rx
from typing import TypedDict, Literal, cast
from app.states.user_state import UserState
from app.states.location_state import LocationState


class Choice(TypedDict):
    title: str
    emoji: str
    points: dict[str, int]


class Question(TypedDict):
    id: str
    part: str
    text: str
    choices: dict[str, Choice]
    layout: str | None = "row"


class Personality(TypedDict):
    title: str
    description: str
    icon: str
    spots: list[str]


class QuizState(rx.State):
    current_page: Literal[
        "home", "quiz", "results", "locations", "location_detail", "profile"
    ] = "home"
    mobile_menu_open: bool = False
    current_question_index: int = 0
    answers: list[str] = []
    scores: dict[str, int] = {"S": 0, "C": 0, "R": 0, "A": 0}
    quiz_finished: bool = False
    questions: list[Question] = [
        {
            "id": "q1",
            "part": "Part 1: The Spark",
            "text": "A perfect nap requires...",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Absolute Silence",
                    "emoji": "🤫",
                    "points": {"S": 0, "R": 2},
                },
                "B": {
                    "title": "Gentle Background Noise",
                    "emoji": "📺",
                    "points": {"S": 2},
                },
                "C": {
                    "title": "The distant sounds of chaos",
                    "emoji": "🔥",
                    "points": {"S": 1, "A": 1},
                },
            },
        },
        {
            "id": "q2",
            "part": "Part 1: The Spark",
            "text": "Your ideal napping light level?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Pitch Black Void",
                    "emoji": "🌑",
                    "points": {"S": 0, "R": 2},
                },
                "B": {
                    "title": "A Little Ambient Light",
                    "emoji": "🌤️",
                    "points": {"S": 2},
                },
                "C": {
                    "title": "Direct, Blazing Sunlight",
                    "emoji": "☀️",
                    "points": {"S": 1, "A": 2},
                },
            },
        },
        {
            "id": "q3",
            "part": "Part 1: The Spark",
            "text": "When it comes to being woken up...",
            "choices": {
                "A": {
                    "title": "I'm a deep sleeper",
                    "emoji": "😴",
                    "points": {"S": 0, "A": 2},
                },
                "B": {
                    "title": "A feather could wake me",
                    "emoji": "🌬️",
                    "points": {"S": 2},
                },
            },
        },
        {
            "id": "q4",
            "part": "Part 2: The Cocoon",
            "text": "Your nap surface should feel like...",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "A firm, supportive plank",
                    "emoji": "🪵",
                    "points": {"C": 0, "A": 1},
                },
                "B": {
                    "title": "A fluffy, sinking cloud",
                    "emoji": "☁️",
                    "points": {"C": 2},
                },
                "C": {
                    "title": "A pile of cool rocks",
                    "emoji": "🪨",
                    "points": {"C": 1, "A": 1},
                },
            },
        },
        {
            "id": "q5",
            "part": "Part 2: The Cocoon",
            "text": "The perfect temperature is...",
            "choices": {
                "A": {
                    "title": "An ice cave",
                    "emoji": "🥶",
                    "points": {"C": 2, "R": 1},
                },
                "B": {"title": "A toasty haven", "emoji": "🥵", "points": {"C": 1}},
            },
        },
        {
            "id": "q6",
            "part": "Part 2: The Cocoon",
            "text": "How many blankets are too many?",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "The limit does not exist",
                    "emoji": "📚",
                    "points": {"C": 2},
                },
                "B": {
                    "title": "One is plenty",
                    "emoji": "☝️",
                    "points": {"C": 0, "A": 1},
                },
                "C": {
                    "title": "Blankets are a prison",
                    "emoji": "⛓️",
                    "points": {"C": 0, "A": 2},
                },
            },
        },
        {
            "id": "q7",
            "part": "Part 3: The Routine",
            "text": "A nap is...",
            "choices": {
                "A": {"title": "A scheduled event", "emoji": "📅", "points": {"R": 2}},
                "B": {
                    "title": "A spontaneous joy",
                    "emoji": "🎉",
                    "points": {"R": 0, "A": 2},
                },
            },
        },
        {
            "id": "q8",
            "part": "Part 3: The Routine",
            "text": "Do you use a sleep mask or earplugs?",
            "choices": {
                "A": {
                    "title": "Always, it's essential",
                    "emoji": "🥽",
                    "points": {"R": 2},
                },
                "B": {
                    "title": "Nah, too much effort",
                    "emoji": "🤷",
                    "points": {"R": 0, "A": 1},
                },
            },
        },
        {
            "id": "q9",
            "part": "Part 3: The Routine",
            "text": "You have a specific 'nap outfit'. Yes or no?",
            "choices": {
                "A": {"title": "Of course I do", "emoji": "👕", "points": {"R": 2}},
                "B": {
                    "title": "I nap in my street clothes",
                    "emoji": "👖",
                    "points": {"R": 0, "A": 2},
                },
            },
        },
        {
            "id": "q10",
            "part": "Part 4: The Chameleon",
            "text": "Napping in public?",
            "layout": "grid",
            "choices": {
                "A": {"title": "A big no from me", "emoji": "🙅", "points": {"A": 0}},
                "B": {
                    "title": "Anywhere is a good spot",
                    "emoji": "😎",
                    "points": {"A": 2},
                },
                "C": {
                    "title": "Only if I am desperate",
                    "emoji": "😥",
                    "points": {"A": 1, "R": 1},
                },
            },
        },
        {
            "id": "q11",
            "part": "Part 4: The Chameleon",
            "text": "You wake up and don't know what year it is. You feel...",
            "choices": {
                "A": {
                    "title": "Panicked and confused",
                    "emoji": "😱",
                    "points": {"A": 0, "R": 1},
                },
                "B": {
                    "title": "Rested and accomplished",
                    "emoji": "😌",
                    "points": {"A": 2},
                },
            },
        },
        {
            "id": "q12",
            "part": "Part 4: The Chameleon",
            "text": "Someone is sitting in your favorite nap spot. You...",
            "layout": "grid",
            "choices": {
                "A": {
                    "title": "Silently rage and leave",
                    "emoji": "😠",
                    "points": {"A": 0, "R": 2},
                },
                "B": {
                    "title": "Find a new, better spot",
                    "emoji": "🗺️",
                    "points": {"A": 2},
                },
                "C": {
                    "title": "Stare at them until they move",
                    "emoji": "👀",
                    "points": {"A": 1, "R": 1},
                },
            },
        },
        {
            "id": "q13",
            "part": "Part 4: The Chameleon",
            "text": "Is a 10-minute power nap worth it?",
            "choices": {
                "A": {
                    "title": "No, I need at least an hour",
                    "emoji": "⏳",
                    "points": {"A": 0, "C": 1},
                },
                "B": {
                    "title": "Yes, it's a perfect refresh",
                    "emoji": "⚡",
                    "points": {"A": 2},
                },
            },
        },
    ]
    answer_stats: dict[str, dict[str, int]] = {
        "q1": {"A": 35, "B": 65},
        "q2": {"A": 40, "B": 60},
        "q3": {"A": 70, "B": 30},
        "q4": {"A": 25, "B": 75},
        "q5": {"A": 80, "B": 20},
        "q6": {"A": 60, "B": 40},
        "q7": {"A": 55, "B": 45},
        "q8": {"A": 30, "B": 70},
        "q9": {"A": 20, "B": 80},
        "q10": {"A": 15, "B": 85},
        "q11": {"A": 50, "B": 50},
        "q12": {"A": 40, "B": 60},
        "q13": {"A": 25, "B": 75},
    }
    personalities: dict[str, Personality] = {
        "LDP": {
            "title": "Lecture Hall Phantom (LDP)",
            "description": "You thrive on the low hum of activity, turning lecture halls and busy cafes into unlikely sanctuaries. Your ability to nap is triggered by stimulation, not the lack of it.",
            "icon": "ghost",
            "spots": ["union-sofa", "library-alcove"],
        },
        "CDM": {
            "title": "Couch Daydreamer (CDM)",
            "description": "Your primary quest is for maximum coziness. You are a connoisseur of cushions, a baron of blankets, and a master of the plush arts.",
            "icon": "couch",
            "spots": ["union-sofa", "basement-lounge"],
        },
        "PNP": {
            "title": "Precision Napper (PNP)",
            "description": "For you, napping is a science. You have a designated time, a perfect spot, and a full pre-sleep checklist. Your naps are efficient, calculated, and deeply satisfying.",
            "icon": "alarm-clock-check",
            "spots": ["library-alcove", "basement-lounge"],
        },
        "WSD": {
            "title": "Wandering Sleep Deity (WSD)",
            "description": "The world is your oyster, and any part of it can be your bed. You can nap on a park bench, a noisy bus, or a pile of rocks. Your adaptability is legendary.",
            "icon": "earth",
            "spots": ["quad-tree", "union-sofa"],
        },
        "LHP": {
            "title": "Library Slacker (LHP)",
            "description": "You need a quiet, predictable environment but also the faint, stimulating rustle of activity. The library is your temple, a perfect blend of ritual and subtle distraction.",
            "icon": "book-user",
            "spots": ["library-alcove", "quad-tree"],
        },
        "Default": {
            "title": "Calculating Persona...",
            "description": "Your unique sleep profile is being analyzed by our highly-trained digital gnomes.",
            "icon": "loader",
            "spots": ["Please wait..."],
        },
    }

    @rx.event
    def set_page(self, page_name: str):
        self.current_page = cast(
            Literal[
                "home", "quiz", "results", "locations", "location_detail", "profile"
            ],
            page_name,
        )
        self.mobile_menu_open = False
        if page_name == "quiz":
            yield QuizState.reset_quiz

    @rx.event
    async def handle_answer(self, question_index: int, answer: str):
        self.answers.append(answer)
        question = self.questions[question_index]
        points_to_add = question["choices"][answer]["points"]
        for dimension, value in points_to_add.items():
            self.scores[dimension] += value
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
        else:
            self.quiz_finished = True
            user_state = await self.get_state(UserState)
            location_state = await self.get_state(LocationState)
            rated_all = len(location_state.ratings) == len(location_state.locations)
            if rated_all:
                yield user_state.unlock_achievement("nap-legend")
            yield QuizState.set_page("results")

    @rx.event
    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    @rx.event
    def reset_quiz(self):
        self.current_question_index = 0
        self.answers = []
        self.scores = {"S": 0, "C": 0, "R": 0, "A": 0}
        self.quiz_finished = False
        self.current_page = "quiz"

    @rx.var
    def current_question(self) -> Question | None:
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    @rx.var
    def progress_percent(self) -> str:
        progress = self.current_question_index / len(self.questions) * 100
        return f"{progress:.0f}%"

    @rx.var
    def personality_type(self) -> str:
        if not self.quiz_finished:
            return "Default"
        if self.scores["S"] > 0 and self.scores["S"] == self.scores["R"]:
            if (
                self.scores["S"] >= self.scores["C"]
                and self.scores["S"] >= self.scores["A"]
            ):
                return "LHP"
        dominant_trait = max(self.scores, key=self.scores.get)
        if dominant_trait == "S":
            return "LDP"
        elif dominant_trait == "C":
            return "CDM"
        elif dominant_trait == "R":
            return "PNP"
        elif dominant_trait == "A":
            return "WSD"
        else:
            return "Default"

    @rx.var
    def personality_details(self) -> Personality:
        return self.personalities.get(
            self.personality_type, self.personalities["Default"]
        )

    @rx.var
    def user_answer_stats(self) -> dict[str, int]:
        stats = {}
        if not self.answers:
            return {}
        for i, question in enumerate(self.questions):
            if i < len(self.answers):
                user_answer = self.answers[i]
                question_id = question["id"]
                stats[question_id] = self.answer_stats[question_id][user_answer]
        return stats