import os
from dotenv import load_dotenv

# `.env` fayldagi ma'lumotlarni yuklash
load_dotenv()

class Config:
    # ✅ ScraperAPI konfiguratsiyasi
    SCRAPER_API_KEY = os.getenv("API_KEY")
    SCRAPER_API_URL = "https://api.scraperapi.com/"

    # ✅ Payeer to‘lov konfiguratsiyasi
    PAYEER_MERCHANT_ID = os.getenv("PAYEER_MERCHANT_ID")
    PAYEER_ACCOUNT = os.getenv("PAYEER_ACCOUNT")
    PAYEER_SECRET_KEY = os.getenv("PAYEER_SECRET_KEY")
    PAYEER_API_URL = "https://payeer.com/api/merchant/"

    # ✅ Sayt konfiguratsiyasi
    BASE_URL = os.getenv("BASE_URL")
    DEBUG = os.getenv("DEBUG", True)

    # ✅ Admin paroli (o‘zgartirish tavsiya etiladi!)
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Qodirbek_2007")