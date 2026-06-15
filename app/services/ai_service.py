from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_character_response(
    character: str,
    site_name: str,
    story_content: str,
    tourist_name: str,
    language: str = "en"
) -> str:

    language_instruction = {
        "en": "Respond in English.",
        "ar": "تكلم بالعربية الفصحى.",
        "fr": "Répondez en français."
    }.get(language, "Respond in English.")

    prompt = (
        f"You are {character}, an ancient Egyptian deity/figure come to life as a guide.\n"
        f"You are greeting {tourist_name} at {site_name}.\n\n"
        f"Your personality:\n"
        f"- Horus: brave, noble, protector of Egypt\n"
        f"- Thoth: wise, mystical, knower of all secrets\n"
        f"- Nefertari: elegant, warm, beloved queen\n\n"
        f"Use this historical content as your knowledge base:\n"
        f"{story_content}\n\n"
        f"{language_instruction}\n\n"
        f"Greet the tourist personally by name, speak AS the character (not about them), "
        f"keep it under 4 sentences, make it dramatic and immersive like they are truly "
        f"standing before an ancient god."
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text


def chat_with_character(
    character: str,
    site_name: str,
    story_content: str,
    tourist_name: str,
    user_message: str,
    chat_history: list,
    language: str = "en"
) -> str:

    language_instruction = {
        "en": "Respond in English.",
        "ar": "تكلم بالعربية الفصحى.",
        "fr": "Répondez en français."
    }.get(language, "Respond in English.")

    # بنبني تاريخ المحادثة
    history_text = ""
    for msg in chat_history:
        role = "Tourist" if msg["role"] == "user" else character
        history_text += f"{role}: {msg['content']}\n"

    prompt = (
        f"You are {character}, an ancient Egyptian deity/figure.\n"
        f"You are speaking with {tourist_name} at {site_name}.\n\n"
        f"Your personality:\n"
        f"- Horus: brave, noble, protector of Egypt\n"
        f"- Thoth: wise, mystical, knower of all secrets\n"
        f"- Nefertari: elegant, warm, beloved queen\n\n"
        f"Your knowledge base about this site:\n"
        f"{story_content}\n\n"
        f"Conversation so far:\n"
        f"{history_text}\n"
        f"Tourist: {user_message}\n\n"
        f"{language_instruction}\n"
        f"Respond AS {character} in 2-3 sentences. Stay in character always. "
        f"Be dramatic, wise, and immersive."
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text