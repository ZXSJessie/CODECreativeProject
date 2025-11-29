import reflex as rx
from app.states.location_state import LocationState as LS


class MapState(rx.State):
    """State for interactive map navigation"""
    selected_building: str = ""  # "library" or "jcit" or ""
    current_floor: str = "G"  # Current floor level
    hovered_icon: str = ""  # Currently hovered location icon
    show_floor_detail: bool = False  # Show detailed floor map
    
    # Building to floor mapping
    building_floors: dict[str, list[str]] = {
        "library": ["G", "1"],
        "jcit": ["P", "11"]
    }
    
    # Location to building/floor mapping
    location_map: dict[str, dict[str, str]] = {
        "cloud-nine-credit": {"building": "library", "floor": "G", "icon": "far", "x": "25%", "y": "35%"},
        "the-spynap-alley": {"building": "library", "floor": "G", "icon": "middle", "x": "45%", "y": "28%"},
        "the-public-isolation": {"building": "library", "floor": "G", "icon": "close", "x": "60%", "y": "45%"},
        "the-urban-zen": {"building": "outdoor", "floor": "outdoor", "icon": "middle", "x": "45%", "y": "55%"},
        "the-shade-throne": {"building": "outdoor", "floor": "outdoor", "icon": "close", "x": "50%", "y": "48%"},
        "the-stonecold-zen": {"building": "outdoor", "floor": "outdoor", "icon": "far", "x": "40%", "y": "60%"},
        "the-bobafueled-snooze": {"building": "jcit", "floor": "11", "icon": "close", "x": "30%", "y": "50%"},
        "the-stairwell-stealth": {"building": "jcit", "floor": "P", "icon": "far", "x": "45%", "y": "65%"},
        "the-curtaincall-nap": {"building": "jcit", "floor": "11", "icon": "middle", "x": "55%", "y": "40%"},
        "the-modular-dream": {"building": "jcit", "floor": "11", "icon": "middle", "x": "65%", "y": "35%"},
    }
    
    @rx.event
    def select_building(self, building: str):
        """Select a building and show its first floor"""
        self.selected_building = building
        self.show_floor_detail = True
        if building in self.building_floors:
            self.current_floor = self.building_floors[building][0]
    
    @rx.event
    def change_floor(self, direction: str):
        """Navigate between floors"""
        if not self.selected_building:
            return
        
        floors = self.building_floors.get(self.selected_building, [])
        if not floors:
            return
        
        try:
            current_index = floors.index(self.current_floor)
            if direction == "up" and current_index > 0:
                self.current_floor = floors[current_index - 1]
            elif direction == "down" and current_index < len(floors) - 1:
                self.current_floor = floors[current_index + 1]
        except ValueError:
            pass
    
    @rx.event
    async def select_location_and_close(self, location_id: str):
        """Select a location and close the floor view"""
        location_state = await self.get_state(LS)
        await location_state.select_location(location_id)
        self.show_floor_detail = False
        self.selected_building = ""
    
    @rx.event
    def close_floor_view(self):
        """Close the detailed floor view"""
        self.show_floor_detail = False
        self.selected_building = ""
    
    @rx.event
    def set_hovered_icon(self, location_id: str):
        """Set the hovered location icon"""
        self.hovered_icon = location_id
    
    @rx.var
    def current_floor_locations(self) -> list[dict]:
        """Get locations for the current floor"""
        if not self.selected_building:
            return []
        
        # Access locations directly from the class
        all_locations = [
            {
                "id": "cloud-nine-credit",
                "location": "Study room on the G floor of the library",
                "name": "Cloud Nine Credit Charge",
                "icon_type": "far",
                "x": "25%",
                "y": "35%"
            },
            {
                "id": "the-spynap-alley",
                "location": "The corridor of bookshelves on the G floor of the library",
                "name": "The Spy-Nap Alley",
                "icon_type": "middle",
                "x": "45%",
                "y": "28%"
            },
            {
                "id": "the-public-isolation",
                "location": "Sofa on the G floor of the library",
                "name": "The Public Isolation Island",
                "icon_type": "close",
                "x": "60%",
                "y": "45%"
            },
            {
                "id": "the-bobafueled-snooze",
                "location": "JCIT Milk Tea Shop",
                "name": "The Boba-Fueled Snooze Booth",
                "icon_type": "close",
                "x": "30%",
                "y": "50%"
            },
            {
                "id": "the-stairwell-stealth",
                "location": "JCIT Stairwell",
                "name": "The Stairwell Stealth Suite",
                "icon_type": "far",
                "x": "45%",
                "y": "65%"
            },
            {
                "id": "the-curtaincall-nap",
                "location": "JCIT Study Room Partition Area",
                "name": "The Curtain-Call Nap Studio",
                "icon_type": "middle",
                "x": "55%",
                "y": "40%"
            },
            {
                "id": "the-modular-dream",
                "location": "JCIT Study Room Sofa",
                "name": "The Modular Dream Fort",
                "icon_type": "middle",
                "x": "65%",
                "y": "35%"
            },
        ]
        
        locations = []
        for loc in all_locations:
            loc_id = loc["id"]
            if loc_id in self.location_map:
                loc_info = self.location_map[loc_id]
                if (loc_info["building"] == self.selected_building and 
                    loc_info["floor"] == self.current_floor):
                    locations.append(loc)
        return locations
    
    def get_floor_locations(self, all_locations: list) -> list[dict]:
        """Get locations for the current floor (unused, kept for compatibility)"""
        return []
    
    @rx.var
    def can_go_up(self) -> bool:
        """Check if can navigate up"""
        if not self.selected_building:
            return False
        floors = self.building_floors.get(self.selected_building, [])
        try:
            return floors.index(self.current_floor) > 0
        except ValueError:
            return False
    
    @rx.var
    def can_go_down(self) -> bool:
        """Check if can navigate down"""
        if not self.selected_building:
            return False
        floors = self.building_floors.get(self.selected_building, [])
        try:
            return floors.index(self.current_floor) < len(floors) - 1
        except ValueError:
            return False
    
    @rx.var
    def floor_map_image(self) -> str:
        """Get the floor map image path"""
        if not self.selected_building or not self.current_floor:
            return ""
        
        if self.selected_building == "library":
            if self.current_floor == "G":
                return "/map images/Pao Yue-kong Library G Floor.png"
            elif self.current_floor == "1":
                return "/map images/Pao Yue-kong Library floor 1.png"
        elif self.selected_building == "jcit":
            if self.current_floor == "P":
                return "/map images/Jockey Club Innovation Tower P.png"
            elif self.current_floor == "11":
                return "/map images/Jockey Club Innovation Tower 11F.png"
        
        return ""
    
    @rx.var
    def building_display_name(self) -> str:
        """Get display name for building"""
        if self.selected_building == "library":
            return "图书馆"  # Library in Chinese as shown in image
        elif self.selected_building == "jcit":
            return "图书馆"  # Should be JCIT but using the text from image
        return ""


def floor_location_icon(location: rx.Var[dict]) -> rx.Component:
    """Interactive location icon on floor map"""
    
    return rx.el.div(
        # Icon
        rx.icon(
            tag="locate-fixed",
            size=32,
            color="#00ff9f",
            class_name="cursor-pointer transition-all duration-300",
            style={
                "filter": "drop-shadow(0 0 4px #00ff9f)",
                "_hover": {
                    "filter": "drop-shadow(0 0 12px #00ff9f)"
                }
            }
        ),
        # Popup on hover
        rx.cond(
            MapState.hovered_icon == location.id,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        location.name,
                        class_name="text-xs font-bold text-white mb-1"
                    ),
                    rx.text(
                        location.location,
                        class_name="text-[10px] text-gray-300"
                    ),
                    class_name="bg-[#1a1a2e] border-2 border-[#00ff9f] p-2 rounded shadow-lg"
                ),
                class_name="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 whitespace-nowrap z-50"
            ),
            rx.el.div()
        ),
        on_mouse_enter=MapState.set_hovered_icon(location.id),
        on_mouse_leave=MapState.set_hovered_icon(""),
        on_click=MapState.select_location_and_close(location.id),
        class_name="absolute cursor-pointer z-40",
        # Position based on location data
        style={
            "top": location.y,
            "left": location.x,
            "transform": "translate(-50%, -100%)"  # Center the icon horizontally and position bottom at coordinate
        }
    )


def floor_detail_view() -> rx.Component:
    """Detailed floor map view with navigation"""
    return rx.el.div(
        # Overlay background
        rx.el.div(
            class_name="fixed inset-0 bg-black/80 z-40",
            on_click=MapState.close_floor_view
        ),
        
        # Floor map container
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        MapState.building_display_name, MapState.current_floor, "层",
                        class_name="text-xl font-bold text-[#00ff9f] tracking-wider"
                    ),
                    class_name="flex-1"
                ),
                rx.el.button(
                    rx.image(
                        src="/map images/icon/close.png",
                        class_name="w-6 h-6"
                    ),
                    on_click=MapState.close_floor_view,
                    class_name="p-2 hover:bg-gray-800 rounded transition-colors"
                ),
                class_name="flex items-center justify-between mb-4 px-6 pt-6"
            ),
            
            # Map and navigation container
            rx.el.div(
                # Floor map
                rx.el.div(
                    rx.image(
                        src=MapState.floor_map_image,
                        class_name="w-full h-auto"
                    ),
                    # Location icons overlaid on map
                    rx.foreach(
                        MapState.current_floor_locations,
                        floor_location_icon
                    ),
                    class_name="relative flex-1"
                ),
                
                # Floor navigation arrows
                rx.el.div(
                    # Up arrow
                    rx.cond(
                        MapState.can_go_up,
                        rx.el.button(
                            rx.image(
                                src="/map images/icon/icon-up.png",
                                class_name="w-12 h-12"
                            ),
                            on_click=MapState.change_floor("up"),
                            class_name="p-2 hover:opacity-80 transition-opacity"
                        ),
                        rx.el.div(class_name="w-12 h-12")
                    ),
                    # Down arrow
                    rx.cond(
                        MapState.can_go_down,
                        rx.el.button(
                            rx.image(
                                src="/map images/icon/icon-down.png",
                                class_name="w-12 h-12"
                            ),
                            on_click=MapState.change_floor("down"),
                            class_name="p-2 hover:opacity-80 transition-opacity"
                        ),
                        rx.el.div(class_name="w-12 h-12")
                    ),
                    class_name="flex flex-col items-center justify-center gap-4 px-4"
                ),
                
                class_name="flex items-center gap-4 px-6 pb-6"
            ),
            
            class_name="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#0a0a0f] border-2 border-[#00ff9f] max-w-6xl w-full max-h-[90vh] overflow-auto z-50 shadow-2xl"
        ),
        
        class_name=rx.cond(MapState.show_floor_detail, "", "hidden")
    )


def outdoor_location_icon(location_id: str, location_name: str, x: str, y: str, icon_type: str) -> rx.Component:
    """Individual outdoor location icon on main campus map"""
    
    return rx.el.div(
        # Clickable icon
        rx.el.div(
            rx.icon(
                tag="locate-fixed",
                size=32,
                color="#00ff9f",
                class_name="cursor-pointer transition-all duration-300",
                style={
                    "filter": "drop-shadow(0 0 4px #00ff9f)",
                    "_hover": {
                        "filter": "drop-shadow(0 0 12px #00ff9f)"
                    }
                }
            ),
            on_click=LS.select_location(location_id),
            class_name="relative z-30"
        ),
        
        # Hover popup showing location name
        rx.cond(
            MapState.hovered_icon == location_id,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        location_name,
                        class_name="text-sm font-bold text-[#00ff9f] mb-1"
                    ),
                    rx.text(
                        "Click to view details",
                        class_name="text-xs text-gray-300"
                    ),
                    class_name="bg-[#1a1a2e] border-2 border-[#00ff9f] p-3 rounded shadow-xl"
                ),
                class_name="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 whitespace-nowrap z-50"
            ),
            rx.el.div()
        ),
        
        on_mouse_enter=MapState.set_hovered_icon(location_id),
        on_mouse_leave=MapState.set_hovered_icon(""),
        
        class_name="absolute cursor-pointer",
        style={
            "top": y,
            "left": x,
            "transform": "translate(-50%, -100%)"
        }
    )


def building_icon_on_main_map(building: str, x: str, y: str) -> rx.Component:
    """Interactive building icon on main campus map"""
    
    return rx.el.div(
        # Clickable icon
        rx.el.div(
            rx.icon(
                tag="locate-fixed",
                size=32,
                color="#00ff9f",
                class_name="cursor-pointer transition-all duration-300",
                style={
                    "filter": "drop-shadow(0 0 4px #00ff9f)",
                    "_hover": {
                        "filter": "drop-shadow(0 0 12px #00ff9f)"
                    }
                }
            ),
            on_click=MapState.select_building(building),
            class_name="relative z-30"
        ),
        
        # Hover popup showing building name
        rx.cond(
            MapState.hovered_icon == building,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        "Pao Yue-kong Library" if building == "library" else "Jockey Club Innovation Tower",
                        class_name="text-sm font-bold text-[#00ff9f] mb-1"
                    ),
                    rx.text(
                        "Click to explore",
                        class_name="text-xs text-gray-300"
                    ),
                    class_name="bg-[#1a1a2e] border-2 border-[#00ff9f] p-3 rounded shadow-xl"
                ),
                class_name="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 whitespace-nowrap z-50"
            ),
            rx.el.div()
        ),
        
        on_mouse_enter=MapState.set_hovered_icon(building),
        on_mouse_leave=MapState.set_hovered_icon(""),
        
        class_name="absolute cursor-pointer",
        style={
            "top": y,
            "left": x
        }
    )


def interactive_campus_map() -> rx.Component:
    """Main interactive campus map"""
    return rx.el.div(
        # Map container
        rx.el.div(
            rx.el.h3(
                "[ CAMPUS MAP ]",
                class_name="text-[#00ff9f] font-bold mb-3 text-center tracking-widest text-sm"
            ),
            rx.el.div(
                # Campus map image
                rx.image(
                    src="/map images/POLYU MAP.png",
                    class_name="w-full h-auto"
                ),
                
                # Building icons overlay - positions based on Main map reference images
                # Pao Yue-kong Library (right side of campus)
                building_icon_on_main_map("library", "68%", "52%"),
                
                # Jockey Club Innovation Tower (left side of campus)
                building_icon_on_main_map("jcit", "28%", "23%"),
                
                # Outdoor locations - direct location icons
                outdoor_location_icon("the-urban-zen", "The Urban Zen Bench", "45%", "55%", "middle"),
                outdoor_location_icon("the-shade-throne", "The Shade Throne", "50%", "48%", "close"),
                outdoor_location_icon("the-stonecold-zen", "The Stone-Cold Zen Zone", "40%", "60%", "far"),
                
                class_name="relative w-full"
            ),
            class_name="w-full border-2 border-[#00ff9f] bg-[#0a0a0f] p-4"
        ),
        
        # Floor detail modal
        floor_detail_view(),
        
        class_name="w-full mb-8"
    )
