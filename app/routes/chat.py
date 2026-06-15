from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import os

router = APIRouter(tags=["Chat"])

LANDMARKS_DATA = {
    "tut_mask": {
        "title": "قناع الملك توت عنخ آمون الذهبي",
        "character_name": "الملك توت عنخ آمون",
        "system_prompt": (
            "أنت الآن تتقمص تماماً وبشكل صارم شخصية الملك الشاب توت عنخ آمون، حاكم مصر القديمة العظيم. "
            "تتحدث باللغة العربية بأسلوب ترحيبي ولطيف ممتزج بهيبة الملوك وفخر الحضارة المصرية القديمة. "
            "أنت واقف مع السائح حالياً في المتحف وهو ينظر إلى 'قناعك الذهبي الشهير'. "
            "أجب عن أسئلته التاريخية بدقة وصحح له أي معلومة مغلوطة كأنك عشت هذه الأحداث بنفسك وبدون الخروج عن الشخصية."
        ),
        "welcome_msg": "مرحباً بك أيها الزائر العظيم في حضرة التاريخ! أنا الملك توت عنخ آمون، وأنت تقف الآن تتأمل قناعي الذهبي الذي صنع ليحميني في رحلتي عبر الزمن. اسألني ما تشاء عن أسراري وحياتي!"
    },
    "tut_statue": {
        "title": "تمثال الملك توت عنخ آمون الشامخ",
        "character_name": "الملك توت عنخ آمون",
        "system_prompt": (
            "أنت الآن تتقمص شخصية الملك توت عنخ آمون العظيم. تتحدث مع السائح الذي يقف حالياً أمام 'تمثالك المنحوت العظيم'. "
            "تتحدث بهيبة الملوك القدامى وترحب بالزائر الذي جاء ليتأمل أثرك الشامخ."
        ),
        "welcome_msg": "أهلاً بك يا صديقي! يسعدني أنك تقف اليوم لتتأمل تمثالي الشامخ. كيف يمكنني مساعدتك في استكشاف تاريخي وأسرار مقبرتي اليوم؟"
    }
}

class ChatMessage(BaseModel):
    message: str

@router.get("/chat/init")
async def initialize_chat(landmark: str = Query(..., description="رمز المعلم الأثري")):
    data = LANDMARKS_DATA.get(landmark)
    if not data:
        raise HTTPException(status_code=404, detail="المعلم غير مسجل")
    return {
        "current_location": data["title"],
        "character": data["character_name"],
        "initial_message": data["welcome_msg"]
    }

@router.post("/chat/send")
async def send_message(landmark: str = Query(...), data: ChatMessage = None):
    landmark_info = LANDMARKS_DATA.get(landmark)
    if not landmark_info:
        raise HTTPException(status_code=404, detail="المعلم غير مسجل")
    
    if not data or not data.message:
        raise HTTPException(status_code=400, detail="الرسالة فارغة")
    
    # سحب المفتاح الصافي من الـ Environment وتأكيده
    api_key = os.getenv("GEMINI_API_KEY")
    
    # حماية إضافية: تنظيف الـ Key من أي مسافات أو حروف غريبة قد تسبب خطأ الـ ascii
    if api_key:
        api_key = api_key.strip()
    else:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set or not loaded correctly.")
    
    try:
        # تهيئة الـ Client بمفتاح نقي ومضمون
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=data.message,
            config=types.GenerateContentConfig(
                system_instruction=landmark_info["system_prompt"],
                temperature=0.7,
            ),
        )
        
        return {
            "character": landmark_info["character_name"],
            "response": response.text
        }
    except Exception as e:
        print("\n❌❌❌ GEMINI API ERROR REPORT ❌❌❌")
        print(f"Details: {str(e)}")
        print("❌❌❌ END OF REPORT ❌❌❌\n")
        raise HTTPException(status_code=500, detail=str(e))