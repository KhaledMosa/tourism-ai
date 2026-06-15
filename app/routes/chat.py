from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Chat"])

LANDMARKS_DATA = {
    "tut_mask": {
        "title_en": "Tutankhamun Golden Mask",
        "title_ar": "قناع الملك توت عنخ آمون الذهبي",
        "character_en": "King Tutankhamun",
        "character_ar": "الملك توت عنخ آمون",
        "system_prompt_en": (
            "You are King Tutankhamun, the Boy King of ancient Egypt. "
            "Speak in English with royal dignity and mystique. "
            "The visitor stands before your golden mask in the Egyptian Museum. "
            "Answer historical questions as if you lived them. Never break character. "
            "Be dramatic, wise, and immersive. Keep responses to 3-4 sentences."
        ),
        "system_prompt_ar": (
            "أنت الملك توت عنخ آمون، ملك مصر الشاب. "
            "تتحدث بالعربية بهيبة الملوك القدامى. "
            "السائح يقف أمام قناعك الذهبي في المتحف المصري. "
            "أجب على أسئلته التاريخية كأنك عشتها. لا تخرج عن الشخصية أبداً. "
            "كن درامياً وحكيماً. اجعل ردودك من 3 إلى 4 جمل."
        ),
        "welcome_en": "Welcome, traveler! I am Tutankhamun, the Boy King of Egypt. You now stand before my golden mask — crafted from solid gold to protect my soul through eternity. Ask me anything about my reign, my tomb, or the secrets of ancient Egypt!",
        "welcome_ar": "مرحباً بك أيها الزائر! أنا الملك توت عنخ آمون. أنت تقف الآن أمام قناعي الذهبي المصنوع من الذهب الخالص ليحمي روحي عبر الأبدية. اسألني ما تشاء عن حكمي أو مقبرتي أو أسرار مصر القديمة!"
    },
    "tut_statue": {
        "title_en": "Tutankhamun Majestic Statue",
        "title_ar": "تمثال الملك توت عنخ آمون الشامخ",
        "character_en": "King Tutankhamun",
        "character_ar": "الملك توت عنخ آمون",
        "system_prompt_en": (
            "You are King Tutankhamun. The visitor stands before your great statue. "
            "Speak in English with royal dignity. Be dramatic and immersive. "
            "Keep responses to 3-4 sentences."
        ),
        "system_prompt_ar": (
            "أنت الملك توت عنخ آمون. السائح يقف أمام تمثالك العظيم. "
            "تحدث بالعربية بهيبة الملك. كن درامياً وجذاباً. "
            "اجعل ردودك من 3 إلى 4 جمل."
        ),
        "welcome_en": "Greetings! I am Tutankhamun. You stand before my eternal form carved in stone. What secrets of my kingdom do you wish to uncover?",
        "welcome_ar": "أهلاً بك! أنا توت عنخ آمون. أنت تقف أمام هيئتي الأبدية المنحوتة في الحجر. ما الأسرار التي تريد اكتشافها؟"
    }
}

class ChatMessage(BaseModel):
    message: str

@router.get("/chat/init")
async def initialize_chat(
    landmark: str = Query(...),
    lang: str = Query("en")
):
    data = LANDMARKS_DATA.get(landmark)
    if not data:
        raise HTTPException(status_code=404, detail="المعلم غير مسجل")

    if lang == "ar":
        return {
            "current_location": data["title_ar"],
            "character": data["character_ar"],
            "initial_message": data["welcome_ar"]
        }
    else:
        return {
            "current_location": data["title_en"],
            "character": data["character_en"],
            "initial_message": data["welcome_en"]
        }

@router.post("/chat/send")
async def send_message(
    landmark: str = Query(...),
    lang: str = Query("en"),
    data: ChatMessage = None
):
    landmark_info = LANDMARKS_DATA.get(landmark)
    if not landmark_info:
        raise HTTPException(status_code=404, detail="المعلم غير مسجل")

    if not data or not data.message:
        raise HTTPException(status_code=400, detail="الرسالة فارغة")

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        api_key = api_key.strip()
    else:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY غير موجود")

    system_prompt = landmark_info["system_prompt_ar"] if lang == "ar" else landmark_info["system_prompt_en"]
    character = landmark_info["character_ar"] if lang == "ar" else landmark_info["character_en"]

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=data.message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
            ),
        )
        return {
            "character": character,
            "response": response.text
        }
    except Exception as e:
        print(f"❌ GEMINI ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))