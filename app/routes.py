import requests
import hashlib
import time
import json
from flask import Blueprint, render_template, request, jsonify, redirect
from bs4 import BeautifulSoup
from config import Config

routes = Blueprint("routes", __name__)

# ✅ **AliExpress sahifasini yuklash**
def fetch_data(api_url):
    """AliExpress sahifasidan mahsulotlarni yuklash (xatolik bo‘lsa, 3 marta urinish)."""
    for _ in range(3):
        try:
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            time.sleep(5)
    return None

# ✅ **Bosh sahifa - Eng mashhur mahsulotlar**
@routes.route("/")
def home():
    """Bosh sahifada eng mashhur mahsulotlarni ko‘rsatish."""
    page = int(request.args.get("page", 1))
    api_url = f"https://api.scraperapi.com/?api_key={Config.SCRAPER_API_KEY}&url=https://www.aliexpress.com/category/100003109/best-selling.html&page={page}"

    response = fetch_data(api_url)
    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        products = extract_products(soup)
        return render_template("index.html", products=products, page=page)

    return "API xatosi: So‘rov bajarilmadi.", 500

# ✅ **AliExpress mahsulotlarini ajratib olish**
def extract_products(soup):
    """AliExpress sahifasidan mahsulotlarni chiqarish."""
    product_list = []
    product_cards = soup.find_all("div", class_=["search-item-card-wrapper-gallery", "card-out-wrapper"])
    
    seen_titles = set()
    
    # 🚫 **18+ mahsulotlarni bloklash**
    blocked_keywords = ["sex", "adult", "vibrator", "lingerie", "condom", "erotic", "sexy", "dildo", "porn"]

    for card in product_cards:
        try:
            title_tag = card.find("h3") or card.find("span", class_="title")
            title = title_tag.text.strip() if title_tag else "Noma’lum mahsulot"

            if any(word in title.lower() for word in blocked_keywords):
                continue  

            if title in seen_titles:
                continue
            seen_titles.add(title)

            short_title = title[:50] + "..." if len(title) > 50 else title

            price_tag = card.find("span", class_="price") or card.find("span", class_="manhattan--price-sale")
            original_price = float(price_tag.text.strip().replace("$", "")) if price_tag else 0.0

            final_price = round(original_price * 1.3, 2)  # ✅ **30% foyda qo‘shamiz**

            image_tag = card.find("img")
            image_url = image_tag["src"] if image_tag else None

            link_tag = card.find("a", href=True)
            product_url = "https:" + link_tag["href"] if link_tag else "#"

            product_list.append({
                "id": product_url.split("/")[-1],  
                "title": short_title,
                "full_title": title,
                "original_price": original_price,
                "final_price": final_price,
                "image_url": image_url,
                "product_url": product_url
            })
        except AttributeError:
            continue  

    return product_list

# ✅ **Mahsulot sahifasi**
@routes.route("/product/<product_id>")
def product_page(product_id):
    """Maxsulot haqidagi to‘liq ma’lumotlarni ko‘rsatish."""
    product_url = f"https://www.aliexpress.com/item/{product_id}.html"
    api_url = f"https://api.scraperapi.com/?api_key={Config.SCRAPER_API_KEY}&url={product_url}"

    response = fetch_data(api_url)
    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        product = extract_product_details(soup, product_id)
        return render_template("product.html", product=product)

    return "API xatosi: Mahsulot yuklanmadi.", 500

# ✅ **Mahsulot sahifasidan ma’lumot ajratish**
def extract_product_details(soup, product_id):
    """AliExpress mahsulot sahifasidan batafsil ma’lumotlarni olish."""
    try:
        title = soup.find("h1").text.strip()
        price_tag = soup.find("span", class_="product-price-value")
        price = float(price_tag.text.strip().replace("$", "")) if price_tag else 0.0
        final_price = round(price * 1.3, 2)

        image_tag = soup.find("img")
        image_url = image_tag["src"] if image_tag else None

        description = soup.find("div", class_="product-description").text.strip() if soup.find("div", class_="product-description") else "Tavsif mavjud emas"

        return {
            "id": product_id,
            "title": title,
            "original_price": price,
            "final_price": final_price,
            "image_url": image_url,
            "description": description
        }
    except AttributeError:
        return {}

# ✅ **Savatcha sahifasi**
@routes.route("/cart")
def cart_page():
    return render_template("cart.html")

# ✅ **Payeer orqali to‘lov**
@routes.route("/checkout", methods=["POST"])
def checkout():
    """Foydalanuvchi mahsulot sotib olayotganda to‘lovni amalga oshirish."""
    product_title = request.form.get("title")
    amount = request.form.get("price")  
    order_id = str(int(time.time()))

    if not amount or float(amount) <= 0:
        return "Xatolik: Narx aniqlanmagan!", 400

    # ✅ Payeer API ma'lumotlari
    merchant_id = Config.PAYEER_MERCHANT_ID
    currency = "USD"
    description = f"Mahsulot: {product_title}"

    success_url = f"{Config.BASE_URL}/success"
    fail_url = f"{Config.BASE_URL}/fail"
    status_url = f"{Config.BASE_URL}/status"

    # ✅ Hash yaratish
    hash_string = f"{merchant_id}:{amount}:{currency}:{description}:{order_id}:{Config.PAYEER_SECRET_KEY}"
    sign = hashlib.sha256(hash_string.encode()).hexdigest().upper()

    # ✅ To‘lov sahifasiga yo‘naltirish
    payeer_url = f"https://payeer.com/merchant/?m={merchant_id}&oa={amount}&currency={currency}&desc={description}&order={order_id}&sign={sign}&success_url={success_url}&fail_url={fail_url}&status_url={status_url}"
    
    return redirect(payeer_url)

# ✅ **To‘lov muvaffaqiyatli amalga oshdi**
@routes.route("/success")
def payment_success():
    return "To‘lov muvaffaqiyatli amalga oshirildi!"

# ✅ **To‘lov bekor qilindi**
@routes.route("/fail")
def payment_fail():
    return "To‘lov bekor qilindi yoki xatolik yuz berdi."

# ✅ **To‘lov statusini tekshirish**
@routes.route("/status", methods=["POST"])
def payment_status():
    order_id = request.form.get("order_id")
    status = request.form.get("status")

    if status == "success":
        return jsonify({"message": "To‘lov tasdiqlandi!", "order_id": order_id})
    return jsonify({"error": "To‘lov amalga oshmadi!"}), 400