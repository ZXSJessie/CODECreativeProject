import reflex as rx
from typing import TypedDict, cast
import qrcode
import io
import base64
from collections import Counter


class Rating(TypedDict):
    comfort: int
    quietness: int
    accessibility: int
    vibe_check: int
    danger: int


class Location(TypedDict):
    id: str
    name: str
    description: str
    icon: str
    model_id: str
    rarity: str
    is_secret: bool


class LocationState(rx.State):
    checked_in_locations: set[str] = set()
    
    locations: list[Location] = [
        {
            "id": "cdm-sofa-paradise",
            "name": "Study room on the G floor of the library",
            "description": "Your demand for comfort rivals that of a five-star hotel sleep tester. Here, the sofa is a cloud, the power outlet is a magical spring. With stable Wi-Fi, you might even dream of being rewarded with credit hours.",
            "icon": "sofa",
            "model_id": "b67d3200015b48db9546fc8e2afd6168",
            "rarity": "LEGENDARY",
            "is_secret": False,
        },
        {
            "id": "ldp-lecture-phantom",
            "name": "The corridor of bookshelves on the G floor of the library",
            "description": "Your sleep here is like a footnote in a thesis—precise, brief, yet indispensable. Each time you close your eyes, it's like activating 'Deep Recovery Mode,' restoring 80% energy in 5 minutes. But, sleeping here... is this bookshelf about to fall over...?",
            "icon": "zap",
            "model_id": "d682b1a9ea2f4683914f9e6384dcb845",
            "rarity": "EPIC",
            "is_secret": False,
        },
        {
            "id": "cdm-ergonomic-island",
            "name": "Sofa on the G floor of the library",
            "description": "This isn't a sofa; it's your 'Ergonomic Island.' People passing by? They're just the sightseers in your dream's bullet comments. You recharge your energy and your inspiration—waking up fully charged, with inspiration unlocked in a new skin.",
            "icon": "sofa",
            "model_id": "5d549bf015bf49f8add67eb74e86ad26",
            "rarity": "LEGENDARY",
            "is_secret": False,
        },
        {
            "id": "pms-urban-sleeper",
            "name": "Outdoor wooden chair",
            "description": "You sleep on the city's pulse. The subway vibrations are white noise, the passing shadows are your dynamic screensaver. You're not napping outdoors; you're starring in a live performance of 'Urban Sleep Log.'",
            "icon": "compass",
            "model_id": "932a64b422a94be9bec6899d36c6f6ea",
            "rarity": "UNCOMMON",
            "is_secret": False,
        },
        {
            "id": "pms-umbrella-universe",
            "name": "Outdoor dining chair",
            "description": "Under the sunshade umbrella, you are your own shopkeeper. Occasionally someone studying? They're just extras in your dream~",
            "icon": "compass",
            "model_id": "0201608218144d65892e4f63647774d0",
            "rarity": "UNCOMMON",
            "is_secret": False,
        },
        {
            "id": "pms-stone-zen",
            "name": "Outdoor stone chair",
            "description": "A four-person stone bench, you occupy one corner, the greenery is your screen. An occasional passerby? They're just forest spirits in your dream~",
            "icon": "compass",
            "model_id": "d33020d326bb4e6bbcf6043f6f5dfb1b",
            "rarity": "UNCOMMON",
            "is_secret": False,
        },
        {
            "id": "pnp-milk-tea-dreams",
            "name": "JCIT Milk Tea Shop",
            "description": "Fall asleep to the scent of milk tea, wake up at the round table. I will strategically choose the 'off-peak hours'!",
            "icon": "clock",
            "model_id": "6c59d214f3224a6b9fa9f135937ff3ff",
            "rarity": "RARE",
            "is_secret": False,
        },
        {
            "id": "ldp-stealth-stairs",
            "name": "JCIT Stairwell",
            "description": "The stench is your barrier, the emptiness is your dojo. No people, right? That's called 'Stealth Skill Activated'!",
            "icon": "zap",
            "model_id": "f0ca0a25820646bf9575d7e075aefae2",
            "rarity": "EPIC",
            "is_secret": False,
        },
        {
            "id": "cdm-curtain-instance",
            "name": "JCIT Study Room Partition Area",
            "description": "Curtain drawn, reclining on the small chair, game console on standby~ The people around are just the audience of your sleep livestream!",
            "icon": "sofa",
            "model_id": "b1c28102ab3a4a7193e7b89a2130a19f",
            "rarity": "LEGENDARY",
            "is_secret": False,
        },
        {
            "id": "cdm-modular-dreams",
            "name": "JCIT Study Room Sofa",
            "description": "Modular sofas for you to arrange, the view outside for you to enjoy~ Just love the 'shared sleep experience'!",
            "icon": "sofa",
            "model_id": "85aa52c8637b42d18d7fb082bd11d265",
            "rarity": "LEGENDARY",
            "is_secret": False,
        },
    ]
    ratings: dict[str, list[Rating]] = {}
    selected_location_id: str | None = None
    new_rating: Rating = {
        "comfort": 3,
        "quietness": 3,
        "accessibility": 3,
        "vibe_check": 3,
        "danger": 3,
    }

    @rx.event
    async def check_in_location(self, location_id: str):
        from app.states.user_state import UserState
        
        if location_id not in self.checked_in_locations:
            self.checked_in_locations.add(location_id)
            user_state = await self.get_state(UserState)
            
            # Find location details
            location = next((loc for loc in self.locations if loc["id"] == location_id), None)
            
            if location:
                yield rx.toast(f"CHECKED IN: {location['name']}", duration=3000)
                
                if location["is_secret"]:
                    yield user_state.unlock_achievement("secret-spot-explorer")
                    yield user_state.unlock_achievement("secret-boss-defeated")
                
                # XP Gain
                user_state.xp += 100
                yield rx.toast("+100 XP", duration=2000)

    @rx.var
    def missions_count(self) -> int:
        return len(self.ratings)

    @rx.var
    def explored_count(self) -> int:
        return len(self.checked_in_locations)

    @rx.var
    def s_rank_count(self) -> int:
        count = 0
        for ratings in self.ratings.values():
            for r in ratings:
                if all(v == 5 for v in r.values()):
                    count += 1
        return count

    @rx.var
    def secrets_found_count(self) -> int:
        count = 0
        for loc_id in self.checked_in_locations:
            loc = next((l for l in self.locations if l["id"] == loc_id), None)
            if loc and loc["is_secret"]:
                count += 1
        return count

    @rx.event
    async def select_location(self, location_id: str):
        from app.states.quiz_state import QuizState

        self.selected_location_id = location_id
        quiz_state = await self.get_state(QuizState)
        quiz_state.current_page = "location_detail"

    @rx.event
    def set_new_rating_value(self, category: str, value: str):
        self.new_rating[category] = int(value)

    @rx.event
    async def submit_rating(self):
        if self.selected_location_id:
            from app.states.user_state import UserState
            from app.states.quiz_state import QuizState

            if self.selected_location_id not in self.ratings:
                self.ratings[self.selected_location_id] = []
            self.ratings[self.selected_location_id].append(self.new_rating.copy())
            user_state = await self.get_state(UserState)
            if all((v == 5 for v in self.new_rating.values())):
                yield user_state.unlock_achievement("5-star-sleeper")
            
            # New Achievements Logic
            if self.new_rating["danger"] == 5:
                yield user_state.unlock_achievement("living-on-the-edge")
            
            if self.new_rating["quietness"] == 5:
                yield user_state.unlock_achievement("zen-master")
            
            if self.new_rating["quietness"] == 1 and self.new_rating["vibe_check"] == 5:
                yield user_state.unlock_achievement("social-sleeper")

            if len(self.ratings) >= 3:
                yield user_state.unlock_achievement("secret-spot-explorer")
            if len(self.ratings) == len(self.locations):
                yield user_state.unlock_achievement("all-area-conqueror")
                quiz_state = await self.get_state(QuizState)
                if quiz_state.quiz_finished:
                    yield user_state.unlock_achievement("nap-legend")
            self.new_rating = {
                "comfort": 3,
                "quietness": 3,
                "accessibility": 3,
                "vibe_check": 3,
                "danger": 3,
            }
            yield rx.toast(
                "Rating submitted! Thanks for your contribution to the nap archives.",
                duration=3000,
            )
            return

    @rx.var
    def selected_location(self) -> Location | None:
        if self.selected_location_id:
            return next(
                (
                    loc
                    for loc in self.locations
                    if loc["id"] == self.selected_location_id
                ),
                None,
            )
        return None

    def _generate_qr_code(self, data: str) -> str:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#00ff9f", back_color="#0a0a0f")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    @rx.var
    def selected_location_qr_code(self) -> str:
        if self.selected_location:
            qr_data = f"sleep-scan-repeat://location/{self.selected_location['id']}"
            return self._generate_qr_code(qr_data)
        return self._generate_qr_code("error")

    def _calculate_average(self, ratings: list[int]) -> float:
        if not ratings:
            return 0.0
        return sum(ratings) / len(ratings)

    @rx.var
    def average_ratings(self) -> dict[str, dict[str, float]]:
        avg_ratings = {}
        for loc_id, rating_list in self.ratings.items():
            if not rating_list:
                avg_ratings[loc_id] = {
                    "comfort": 0,
                    "quietness": 0,
                    "accessibility": 0,
                    "vibe_check": 0,
                    "danger": 0,
                    "overall": 0,
                }
                continue
            comfort_avg = self._calculate_average([r["comfort"] for r in rating_list])
            quietness_avg = self._calculate_average(
                [r["quietness"] for r in rating_list]
            )
            accessibility_avg = self._calculate_average(
                [r["accessibility"] for r in rating_list]
            )
            vibe_avg = self._calculate_average([r["vibe_check"] for r in rating_list])
            danger_avg = self._calculate_average([r["danger"] for r in rating_list])
            overall = self._calculate_average(
                [comfort_avg, quietness_avg, accessibility_avg, vibe_avg, danger_avg]
            )
            avg_ratings[loc_id] = {
                "comfort": round(comfort_avg, 1),
                "quietness": round(quietness_avg, 1),
                "accessibility": round(accessibility_avg, 1),
                "vibe_check": round(vibe_avg, 1),
                "danger": round(danger_avg, 1),
                "overall": round(overall, 1),
            }
        return avg_ratings

    @rx.var
    def total_ratings_submitted(self) -> int:
        return sum((len(r) for r in self.ratings.values()))

    @rx.var
    def favorite_location(self) -> str:
        if not self.ratings:
            return "Not enough data"
        loc_counts = {loc_id: len(ratings) for loc_id, ratings in self.ratings.items()}
        if not loc_counts:
            return "Not enough data"
        most_rated_id = max(loc_counts, key=loc_counts.get)
        fav_location = next(
            (loc for loc in self.locations if loc["id"] == most_rated_id), None
        )
        return fav_location["name"] if fav_location else "Unknown"

    @rx.var
    def average_rating_given(self) -> float:
        all_user_ratings = []
        for rating_list in self.ratings.values():
            for rating in rating_list:
                all_user_ratings.extend(rating.values())
        if not all_user_ratings:
            return 0.0
        return round(sum(all_user_ratings) / len(all_user_ratings), 1)

    @rx.var
    def completion_percentage(self) -> int:
        rated_count = len(self.ratings)
        total_locations = len(self.locations)
        if total_locations == 0:
            return 0
        return int(rated_count / total_locations * 100)