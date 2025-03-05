from flask import Flask
from config import Config

def create_app():
    """Flask ilovasini yaratish va sozlash."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Blueprintlarni import qilish
    from app.routes import routes  
    
    # 🔹 Admin panel kerak bo‘lsa, import qiling
    try:
        from app.admin import admin
        app.register_blueprint(admin, url_prefix='/admin')
    except ImportError:
        print("⚠ Admin panel topilmadi, lekin davom etamiz.")

    # ✅ Blueprintlarni ro‘yxatdan o‘tkazish
    app.register_blueprint(routes, url_prefix='/')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)