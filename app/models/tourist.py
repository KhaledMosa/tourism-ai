from dataclasses import dataclass, field
from typing import List

@dataclass
class Tourist:
    id: str
    name: str
    nationality: str
    language: str          # "ar", "en", "fr"
    visited_sites: List[str] = field(default_factory=list)

    def add_visit(self, site_id: str):
        if site_id not in self.visited_sites:
            self.visited_sites.append(site_id)

    def has_visited(self, site_id: str) -> bool:
        return site_id in self.visited_sites

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nationality": self.nationality,
            "language": self.language,
            "visited_sites": self.visited_sites
        }