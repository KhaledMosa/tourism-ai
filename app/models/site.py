from dataclasses import dataclass, field
from typing import List

@dataclass
class Site:
    id: str
    name: str
    location: str
    era: str               # "Ancient Kingdom", "New Kingdom"...
    character: str         # الشخصية اللي هتتكلم عن الموقع ده
    story_ids: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "era": self.era,
            "character": self.character,
            "story_ids": self.story_ids
        }