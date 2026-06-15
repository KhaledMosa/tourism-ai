from app.models.tourist import Tourist
from app.models.site import Site
from app.models.story import Story

TOURISTS = {
    "T001": Tourist(id="T001", name="Ahmed Hassan", nationality="Egyptian", language="ar", visited_sites=[]),
    "T002": Tourist(id="T002", name="John Smith", nationality="American", language="en", visited_sites=["SITE001"]),
    "T003": Tourist(id="T003", name="Visitor", nationality="Unknown", language="en", visited_sites=[]),
}

SITES = {
    "SITE001": Site(id="SITE001", name="Great Pyramid of Giza", location="Giza", era="Old Kingdom", character="Thoth", story_ids=["S001", "S002"]),
    "SITE002": Site(id="SITE002", name="Karnak Temple", location="Luxor", era="New Kingdom", character="Nefertari", story_ids=["S003"]),
    "SITE003": Site(
        id="SITE003",
        name="Tutankhamun Golden Mask",
        location="Egyptian Museum, Cairo",
        era="New Kingdom — 18th Dynasty",
        character="Tutankhamun",
        story_ids=["S004"]
    ),
}

STORIES = {
    "S001": Story(id="S001", site_id="SITE001", character="Thoth", title="The Great Pyramid's Secret", content="I am Thoth, god of wisdom and writing. Welcome to the Great Pyramid of Khufu, built over 4,500 years ago. This pyramid stood as the tallest structure on Earth for 3,800 years. Inside these ancient stones lie secrets of mathematics, astronomy, and divine power.", language="en"),
    "S002": Story(id="S002", site_id="SITE001", character="Thoth", title="سر الهرم الأكبر", content="أنا تحوت، إله الحكمة والكتابة. أهلاً بك في هرم خوفو العظيم، الذي بُني منذ أكثر من 4500 عام. ظل هذا الهرم أطول مبنى في العالم لمدة 3800 سنة.", language="ar"),
    "S003": Story(id="S003", site_id="SITE002", character="Nefertari", title="Temple of the Gods", content="I am Nefertari, beloved wife of Ramesses the Great. Welcome to Karnak, the largest temple complex ever built. For over 2,000 years, pharaohs added their mark to this sacred place.", language="en"),
    "S004": Story(
        id="S004",
        site_id="SITE003",
        character="Tutankhamun",
        title="The Golden Face of the Boy King",
        content="""I am Tutankhamun, the Boy King, who ascended the throne of Egypt at just nine years of age.
        This golden mask you gaze upon is my eternal face — crafted from 10 kilograms of solid gold, inlaid with lapis lazuli, quartz, and obsidian.
        I ruled Egypt during the 18th Dynasty around 1332 BC, restoring the old gods after my father Akhenaten's revolution.
        My tomb in the Valley of the Kings was discovered by Howard Carter in 1922, virtually intact after 3,000 years.
        The golden mask was placed over my mummified face to protect my soul on its journey to the afterlife.
        I died at approximately 19 years of age — my cause of death still debated by scholars to this day.
        Yet here I stand before you, immortal in gold.""",
        language="en"
    ),
}

def get_tourist(tourist_id: str) -> Tourist:
    return TOURISTS.get(tourist_id)

def get_site(site_id: str) -> Site:
    return SITES.get(site_id)

def get_story(story_id: str) -> Story:
    return STORIES.get(story_id)

def get_stories_for_site(site_id: str, language: str = "en") -> list:
    return [s for s in STORIES.values() if s.site_id == site_id and s.language == language]