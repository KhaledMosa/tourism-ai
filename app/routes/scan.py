from fastapi import APIRouter, HTTPException
from data.mock_data import get_tourist, get_site, get_stories_for_site
from app.services.ai_service import generate_character_response

router = APIRouter()

@router.get("/scan/{tourist_id}/{site_id}")
def scan_qr(tourist_id: str, site_id: str):

    tourist = get_tourist(tourist_id)
    if not tourist:
        raise HTTPException(status_code=404, detail="Tourist not found")

    site = get_site(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    stories = get_stories_for_site(site_id, tourist.language)
    if not stories:
        stories = get_stories_for_site(site_id, "en")

    tourist.add_visit(site_id)

    combined_story = "\n".join([s.content for s in stories])

    ai_response = generate_character_response(
        character=site.character,
        site_name=site.name,
        story_content=combined_story,
        tourist_name=tourist.name,
        language=tourist.language
    )

    return {
        "tourist": tourist.to_dict(),
        "site": site.to_dict(),
        "character": site.character,
        "ai_greeting": ai_response,
        "stories": [s.to_dict() for s in stories]
    }