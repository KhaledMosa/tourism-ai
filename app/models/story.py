from dataclasses import dataclass

@dataclass
class Story:
    id: str
    site_id: str
    character: str         # "Horus", "Nefertari", "Thoth"
    title: str
    content: str           # النص اللي الـ AI هيقوله
    language: str          # "en", "ar", "fr"

    def to_dict(self):
        return {
            "id": self.id,
            "site_id": self.site_id,
            "character": self.character,
            "title": self.title,
            "content": self.content,
            "language": self.language
        }