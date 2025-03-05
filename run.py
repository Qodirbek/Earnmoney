from flask import Flask
from config import Config
from app.routes import routes
from dotenv import load_dotenv
import os
from app.admin import admin
app.register_blueprint(admin)

# .env dagi o‘zgaruvchilarni yuklash
load_dotenv()

# Flask sozlamalari
API_KEY = os.getenv("SCRAPER_API_KEY")
FLASK_ENV = os.getenv("FLASK_ENV")

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)