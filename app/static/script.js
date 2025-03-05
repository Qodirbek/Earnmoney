document.addEventListener("DOMContentLoaded", function() {
    updateCart();
});

// ✅ Mahsulotni savatchaga qo‘shish
function addToCart(id, title, price, image) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    let existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, title, price, image, quantity: 1 });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    showNotification("🛒 Mahsulot savatchaga qo‘shildi!");
    updateCart();
}

// ✅ Savatchani yangilash
function updateCart() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let cartItems = document.getElementById("cart-items");
    let cartCount = document.getElementById("cart-count");
    let totalPrice = document.getElementById("total-price");

    if (cartCount) {
        cartCount.innerText = cart.length;
    }

    if (cartItems) {
        cartItems.innerHTML = "";
        let total = 0;

        if (cart.length === 0) {
            cartItems.innerHTML = "<p>Savatcha bo‘sh! 🛒</p>";
        } else {
            cart.forEach((item, index) => {
                let itemTotal = item.price * item.quantity;
                total += itemTotal;
                cartItems.innerHTML += `
                    <div class="cart-item">
                        <img src="${item.image}" class="cart-img" alt="${item.title}">
                        <div class="cart-info">
                            <p>${item.title}</p>
                            <p><strong>$${item.price.toFixed(2)}</strong> x ${item.quantity}</p>
                        </div>
                        <div class="quantity-controls">
                            <button onclick="updateQuantity(${index}, -1)">➖</button>
                            <span>${item.quantity}</span>
                            <button onclick="updateQuantity(${index}, 1)">➕</button>
                        </div>
                        <button class="remove-btn" onclick="removeFromCart(${index})">❌</button>
                    </div>
                `;
            });
        }

        if (totalPrice) {
            totalPrice.innerText = total.toFixed(2);
        }

        localStorage.setItem("cart", JSON.stringify(cart));
    }
}

// ✅ Mahsulot miqdorini oshirish / kamaytirish
function updateQuantity(index, change) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart[index].quantity += change;

    if (cart[index].quantity <= 0) {
        cart.splice(index, 1);
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    updateCart();
}

// ✅ Mahsulotni savatchadan o‘chirish
function removeFromCart(index) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.splice(index, 1);
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCart();
}

// ✅ Buyurtma berish (To‘lov sahifasiga o‘tish)
function checkout() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        showNotification("❌ Savatcha bo‘sh! Mahsulot qo‘shing.");
        return;
    }

    localStorage.setItem("checkoutCart", JSON.stringify(cart));
    window.location.href = "/checkout";
}

// ✅ Modal bildirishnoma ko‘rsatish
function showNotification(message) {
    let notification = document.createElement("div");
    notification.className = "notification";
    notification.innerText = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000);
}

// ✅ Boshlang‘ich holatda savatchani yangilash
updateCart();