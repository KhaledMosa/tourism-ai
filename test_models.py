from data.mock_data import get_tourist, get_site, get_stories_for_site

# جرب السائح
tourist = get_tourist("T002")
print(tourist.name)           # John Smith
print(tourist.has_visited("SITE001"))  # True

# جرب الموقع
site = get_site("SITE001")
print(site.name)              # Great Pyramid of Giza
print(site.character)         # Thoth

# جرب القصص
stories = get_stories_for_site("SITE001", "en")
for s in stories:
    print(s.title)