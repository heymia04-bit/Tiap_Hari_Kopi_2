import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
col1, col2 = st.columns([1,6])

with col1:
    st.image("images/tiapharilogo.jpg", width=170)

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0; color:white;'>TIAP HARI KOPI </h1>
    """, unsafe_allow_html=True)

# NAVBAR STYLE
st.markdown("""
<div class='navbar'>
🏠 Home &nbsp;&nbsp; | &nbsp;&nbsp; 🍽 Menu &nbsp;&nbsp; | &nbsp;&nbsp; 📅 Reservation &nbsp;&nbsp; | &nbsp;&nbsp; 💬 Feedback &nbsp;&nbsp; | &nbsp;&nbsp; ℹ️ About Us &nbsp;&nbsp; | &nbsp;&nbsp; 🔐 Login
</div>
""", unsafe_allow_html=True)
# Banner Depan

img = Image.open("images/tiapharifront.jpg")

width, height = img.size
cropped_img = img.crop((0, height//2.1, width, height - 200))

st.image(cropped_img, width="stretch")

st.markdown("""
<h2 style='
text-align:center;
color:white;
margin-top:-90px;
text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
'>
Start Your Day With A Cup Of Coffee 
</h2>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(to bottom, #7393B3, #dbe6f1);
}

/* CONTENT WRAPPER (THIS FIXES READABILITY) */
.main {
    background: rgba(255,255,255,0.92);
    padding: 20px;
    border-radius: 20px;
}

/* HEADINGS */
h1, h2, h3 {
    color: #0d3b66;
}

/* NAVBAR */
.navbar {
    text-align:center;
    padding:12px;
    background: linear-gradient(to right, #0047AB, #4169E1);
    border-radius:12px;
    color:white;
    font-weight:bold;
}

/* CARDS */
.card {
    background-color: white;
    padding: 15px;
    border-radius: 20px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    text-align: center;
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.03);
}
.card {
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
/* IMAGE */
img {
    border-radius: 15px;
}
img:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# GALLERY SLIDER (3 images per row)
# ------------------------------------------

st.header("📸 Gallery & Our Story")

images = [
    "images/tiapharibefore.jpg",
    "images/tiaphariopen.jpg",
    "images/tiapharibestdrinks.jpg",
    "images/tiapharipasta.jpg",
    "images/tiapharisnack.jpg",
    "images/tiapharikacangphool.jpg"
]

# Initialize slider index
if "img_index" not in st.session_state:
    st.session_state.img_index = 0

# Buttons
nav1, nav2, nav3 = st.columns([1,6,1])

with nav1:
    if st.button("⬅️"):
        st.session_state.img_index -= 1
        if st.session_state.img_index < 0:
            st.session_state.img_index = 0

with nav3:
    if st.button("➡️"):
        st.session_state.img_index += 1
        if st.session_state.img_index > len(images) - 3:
            st.session_state.img_index = len(images) - 3

# Show 3 images
start = st.session_state.img_index
end = start + 3

cols = st.columns(3)

for i, img_path in enumerate(images[start:end]):
    with cols[i]:
        try:
            st.image(img_path, use_container_width=True)
        except:
            st.image("https://via.placeholder.com/300x200")

st.markdown(f"""
<div style='
    background-color:#0047AB;
    color:white;
    padding:20px;
    border-radius:15px;
    margin-top:15px;
    text-align:center;
    font-size:16px;
'>
    ✨ Our journey started from a small idea and grew into a cozy café loved by many. 
    Every cup of coffee we serve carries passion, comfort, and a little bit of happiness ☕💙
</div>
""", unsafe_allow_html=True)

st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)
# --------------------------------------------------

# MENU SECTION
# --------------------------------------------------
st.markdown("<div style='margin-top:-20px'></div>", unsafe_allow_html=True)
st.header("🍽 Menu Section")

menu_items = [
    {"name": "Matcha Latte", "category": "Beverage", "price": 9, "image": "images/tiapharimatchalatte.jpg"},
    {"name": "Passion Soda", "category": "Beverage", "price": 8, "image": "images/tiapharipassionsoda.jpg"},
    {"name": "Iced Latte", "category": "Beverage", "price": 9, "image": "images/tiaphariicedlatte.jpg"},
    {"name": "Lotus Biscoff Cheese Tart", "category": "Dessert", "price": 12, "image": "images/biscoffcheesetart.jpg"},
    {"name": "Chocolate Cheese Tart", "category": "Dessert", "price": 12, "image": "images/choccheesetart.jpg"},
    {"name": "Chocolate Moise Belanda", "category": "Dessert", "price": 14, "image": "images/chocmoistbelanda.jpg"},
    {"name": "Mini Pavlova", "category": "Dessert", "price": 12, "image": "images/minipavlova.jpg"},
    {"name": "Strawberry Cheese Tart", "category": "Dessert", "price": 12, "image": "images/strawberrycheesetart.jpg"},
    {"name": "Fettucine Bolognese Meatballs", "category": "Western Food", "price": 15, "image": "images/fettucinebolognesemeatballs.jpg"},
    {"name": "Garlic Butter Fettucine", "category": "Western Food", "price": 15, "image": "images/garlicbutterseafoodfettucine.jpg"},
    {"name": "Crispy Veggie Cucur", "category": "Local Food", "price": 9, "image": "images/crispyveggiecucur.jpg"},
    {"name": "Veggie Spring Rolls", "category": "Local Food", "price": 9, "image": "images/veggiespringrolls.jpg"},
    #HIDE FOR NOW 
    #{"name": "", "category": "Local Food", "price": 9, "image": "images/.jpg"},
    #{"name": "Chicken Chop", "category": "Western Food", "price": 15, "image": "images/chicken.jpg"},
]

cols = st.columns(3)

for i, item in enumerate(menu_items):
    with cols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        try:
            st.image(item["image"], use_container_width=True)
        except:
            st.image("https://via.placeholder.com/300x200")
        st.subheader(item["name"])
        st.write(item["category"])
        st.markdown(f"<p class='price'>RM {item['price']}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)

# --------------------------------------------------
# RESERVATION SECTION
# --------------------------------------------------
st.header("📅 Reservation System")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# WHATSAPP
with col1:
    st.markdown("### 💬 Reserve via WhatsApp")
    st.write("Quick table booking with us!")

    st.link_button("📲 Book Now", "https://wa.me/60123456789")

# GRAB
with col2:
    st.markdown("### 🛵 Order via Grab")
    st.write("Fast delivery to your door 💨")
    st.link_button(
        "Order Now on Grab 🚀",
        "https://r.grab.com/g/6-20260415_230213_9ef30256bb924d40bac7573c90142773_MEXMPS-1-C3NTVKDZLZCHTJ"
    )
st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)

    #  ABOUT US 
st.header("ℹ️ About Us")

st.write("""
📍Kubang Kerian, Kelantan  
☕ Established in 2021  
📞012-3456789  
""")

map_data = pd.DataFrame({"lat": [6.095], "lon": [102.275]})

st.markdown("<div style='max-width:400px;'>", unsafe_allow_html=True)
st.map(map_data)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)

# --------------------------------------------------
# CUSTOMER ENGAGEMENT SECTION
# --------------------------------------------------
st.header("💬 Customer Engagement")

st.metric("⭐ Average Rating", "4.5 / 5")

reviews = [
    ("⭐⭐⭐⭐⭐", "Great ambience and coffee!"),
    ("⭐⭐⭐⭐", "Affordable price and friendly staff."),
    ("⭐⭐⭐", "Waiting time a bit long during peak hours."),
    ("⭐⭐⭐⭐⭐", "Perfect place for students!")
]

for r in reviews:
    st.success(f"{r[0]} — {r[1]}")

st.subheader("Leave Feedback")
st.text_input("Your Name")
st.selectbox("Rating", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
st.text_area("Feedback")
st.button("Submit Feedback")

st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOGIN SECTION
# --------------------------------------------------
st.header("🔐 Staff Login System")

st.warning("Demo only - No real authentication")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Login")

with col2:
    st.subheader("Register")
    st.text_input("Full Name")
    st.text_input("Email")
    st.text_input("New Password", type="password")
    st.button("Create Account")

st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)

# --------------------------------------------------
# ANALYTICS DASHBOARD
# --------------------------------------------------
st.header("📊 Analytics Dashboard")

st.caption("Sample dashboard for business reporting")

col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", "1,259")
col2.metric("Positive Sentiment", "72%")
col3.metric("Returning Customers", "48%")

sentiment_df = pd.DataFrame({
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Count": [720, 350, 189]
})

fig1 = px.pie(
    sentiment_df,
    values="Count",
    names="Sentiment",
    title="Customer Sentiment"
)

st.plotly_chart(fig1, use_container_width=True)

engagement_df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Engagement": [200, 320, 280, 400, 450]
})

fig2 = px.bar(
    engagement_df,
    x="Month",
    y="Engagement",
    title="Monthly Engagement"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<hr style="border:1px solid #ccc; margin:40px 0;">
""", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown('<div class="footer">© 2026 Tiap Hari Kopi | Prototype System</div>', unsafe_allow_html=True)