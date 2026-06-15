from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from data.mock_data import get_tourist, get_site, get_stories_for_site
from app.services.ai_service import chat_with_character

router = APIRouter()

class Message(BaseModel):
    role: str      # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    tourist_id: str
    site_id: str
    message: str
    history: List[Message] = []

@router.post("/chat")
def chat(request: ChatRequest):

    tourist = get_tourist(request.tourist_id)
    if not tourist:
        raise HTTPException(status_code=404, detail="Tourist not found")

    site = get_site(request.site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    stories = get_stories_for_site(request.site_id, tourist.language)
    if not stories:
        stories = get_stories_for_site(request.site_id, "en")

    combined_story = "\n".join([s.content for s in stories])

    history_dicts = [{"role": m.role, "content": m.content} for m in request.history]

    ai_reply = chat_with_character(
        character=site.character,
        site_name=site.name,
        story_content=combined_story,
        tourist_name=tourist.name,
        user_message=request.message,
        chat_history=history_dicts,
        language=tourist.language
    )

    return {
        "character": site.character,
        "reply": ai_reply,
        "tourist": tourist.name
    }