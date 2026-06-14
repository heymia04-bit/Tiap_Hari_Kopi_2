import streamlit as st
import pandas as pd
import plotly.express as px
import PIL
import base64
import os
import requests
import re

# --------------------------------------------------
# 1. SET PAGE CONFIG & TIAP HARI KOPI THEME CSS
# --------------------------------------------------
st.set_page_config(page_title="Tiap Hari Kopi", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'menu_index' not in st.session_state:
    st.session_state['menu_index'] = 0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght=300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Montserrat', sans-serif;
    background-color: #0b131f !important;
    scroll-behavior: smooth !important; /* Smooth scroll behavior on global frame targets */
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
    max-width: 1200px !important;
}

/* NAVBAR STYLE */
.nk-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid #1a2636;
    margin-bottom: 40px;
}
.nk-logo {
    color: #ffffff;
    font-weight: 800;
    font-size: 26px;
    letter-spacing: 2px;
}
.nk-logo span {
    color: #004481; /* Branded Logo Blue */
}
.nk-nav {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #92a4b8;
}

/* CLEAN MODERN NAV LINK LINKS */
.nk-nav-link {
    color: #92a4b8 !important;
    text-decoration: none !important;
    transition: color 0.2s ease, border-color 0.2s ease;
    padding-bottom: 6px;
    border-bottom: 2px solid transparent;
}
.nk-nav-link:hover {
    color: #ffffff !important;
}
.nk-nav-link.active {
    color: #ffffff !important;
    border-bottom: 2px solid #004481 !important; /* Elegant bottom accent line like Starbucks */
}

/* HERO BANNER TEXT */
.nk-hero-title {
    color: #ffffff;
    font-size: 46px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: -1px;
}
.nk-hero-subtitle {
    color: #004481; /* Branded Logo Blue */
    font-size: 18px;
    font-weight: 600;
    text-transform: uppercase;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 50px;
}

/* CARDS */
.nk-card {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    height: 100%;
}

/* MENU COMPONENT STYLING */
.nk-menu-title {
    font-size: 18px;
    font-weight: 700;
    color: #111111;
    margin-top: 15px;
}
.nk-menu-cat {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    color: #888888;
    letter-spacing: 1px;
    margin-bottom: 10px;
}
.nk-menu-price {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff; 
    background-color: #004481; /* Branded Logo Blue */
    display: inline-block;
    padding: 2px 12px;
    border-radius: 4px;
}

/* TAB ADJUSTMENTS */
.stTabs [data-baseweb="tab-list"] {
    background-color: #121e2e;
    padding: 8px;
    border-radius: 8px;
}
.stTabs [data-baseweb="tab"] {
    color: #ffffff !important;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    color: #ffffff !important; 
    background-color: #004481; /* Branded Logo Blue */
    border-radius: 4px;
}

div.stButton > button {
    background-color: #004481 !important; /* Branded Logo Blue */
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 28px !important;
    font-weight: 700 !important;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #003361 !important;
}

/* GOOGLE REVIEWS INTERFACE STYLING */
.google-review-card {
    background-color: #121e2e;
    border: 1px solid #1a2636;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    font-family: Roboto, Helvetica, Arial, sans-serif;
    color: #e8eaed;
    text-align: left;
}
.gr-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.gr-profile {
    display: flex;
    align-items: center;
    gap: 12px;
}
.gr-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}
.gr-user-info {
    display: flex;
    flex-direction: column;
}
.gr-name {
    font-weight: 500;
    font-size: 14px;
    color: #e8eaed;
}
.gr-meta {
    font-size: 12px;
    color: #9aa0a6;
}
.gr-more-btn {
    color: #9aa0a6;
    font-size: 18px;
}
.gr-stars-row {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 8px;
}
.gr-stars {
    color: #fbbc05; 
    font-size: 14px;
}
.gr-time {
    font-size: 12px;
    color: #9aa0a6;
    margin-left: 4px;
}
.gr-badge {
    background-color: #1a2636;
    color: #e8eaed;
    font-size: 10px;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 4px;
    margin-left: 8px;
}
.gr-text {
    font-size: 14px;
    line-height: 1.46;
    color: #bdc1c6;
    margin-bottom: 12px;
}
.gr-images-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 12px;
    margin-bottom: 12px;
}
.gr-img {
    width: 100%;
    height: 70px;
    object-fit: cover;
    border-radius: 6px;
}
.gr-aspects {
    background-color: #0b131f;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    color: #bdc1c6;
    margin-top: 8px;
    border: 1px solid #1a2636;
}
.gr-footer {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 12px;
    padding-top: 8px;
    border-top: 1px solid #1a2636;
    color: #9aa0a6;
    font-size: 13px;
}
.local-review-card {
    background-color: #162a45;
    border: 1px solid #1d3b61;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    color: #8ab4f8;
    text-align: left;
}

/* MOBILE APP MOCKUP BRANDING CSS */
.phone-mockup {
    width: 100%;
    max-width: 360px;
    height: 640px;
    background-color: #000000;
    border: 8px solid #2a2a2a;
    border-radius: 36px;
    margin: 0 auto;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 40px rgba(0,0,0,0.7);
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.phone-link-wrapper {
    text-decoration: none !important;
    display: block;
    cursor: pointer;
}
.phone-header {
    padding: 15px 15px 10px 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: bold;
    border-bottom: 1px solid #121212;
}
.phone-profile-section {
    padding: 15px;
}
.phone-stats-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}
.mock-avatar {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #222;
    padding: 2px;
}
.stat-box {
    text-align: center;
    flex: 1;
}
.stat-num {
    font-weight: 700;
    font-size: 16px;
    display: block;
    color: #ffffff;
}
.stat-label {
    font-size: 11px;
    color: #a8a8a8;
}
.bio-section {
    font-size: 13px;
    line-height: 1.4;
    padding: 0 15px 15px 15px;
}
.bio-name {
    font-weight: 700;
}
.bio-text {
    color: #f5f5f5;
    white-space: pre-line;
}
.action-buttons {
    display: flex;
    gap: 6px;
    padding: 0 15px 15px 15px;
}
.mock-btn {
    flex: 1;
    background-color: #1a1a1a;
    color: white;
    text-align: center;
    padding: 6px 0;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
}
.mock-btn-blue {
    background-color: #0095f6;
}
.scrollable-feed {
    flex: 1;
    overflow-y: auto;
    padding: 2px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2px;
}
.scrollable-feed::-webkit-scrollbar {
    width: 4px;
}
.scrollable-feed::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 2px;
}
.feed-img {
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    background-color: #152233;
}

/* STARBUCKS PROMOTIONS INTERFACE STYLE */
.sb-promo-container {
    display: flex;
    background-color: #0e382c;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 25px;
    min-height: 380px;
}
.sb-promo-img-side {
    flex: 1;
    min-width: 50%;
    background-size: cover;
    background-position: center;
}
.sb-promo-text-side {
    flex: 1;
    padding: 45px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: #1e3932;
}
.sb-promo-title {
    font-size: 32px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 15px;
    letter-spacing: 0.5px;
}
.sb-promo-desc {
    font-size: 16px;
    font-weight: 500;
    line-height: 1.5;
    margin-bottom: 25px;
}
.sb-promo-btn {
    display: inline-block;
    padding: 8px 18px;
    border: 1px solid;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none !important;
    transition: background-color 0.2s;
}

/* STARBUCKS ASYMMETRIC IMAGE GRID STYLE */
.sb-grid-layout {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 16px;
    width: 100%;
    margin-top: 20px;
}
.sb-grid-left-featured {
    width: 100%;
    height: 100%;
    border-radius: 6px;
    overflow: hidden;
}
.sb-grid-left-featured img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.sb-grid-right-stack {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.sb-grid-item {
    border-radius: 6px;
    overflow: hidden;
    width: 100%;
}
.sb-grid-item img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
}

/* NATIVE COMPLIANT IMMUTABLE FIXED BOTTOM-RIGHT GO TO TOP FLOATER */
.scroll-wrapper-global {
    position: fixed;
    bottom: 40px;
    right: 40px;
    z-index: 99999;
}
.scroll-top-link {
    text-decoration: none !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    cursor: pointer;
    background: none;
    border: none;
    padding: 0;
}
.scroll-top-link .arrow-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    background-color: #004481; /* Branded Logo Blue */
    color: white !important;
    border-radius: 50%;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
    transition: background-color 0.2s ease, transform 0.2s ease;
}
.scroll-top-link .btn-text {
    font-family: 'Montserrat', sans-serif;
    color: #92a4b8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    transition: color 0.2s ease;
}
.scroll-top-link:hover .arrow-icon {
    background-color: #003361;
    transform: scale(1.1);
}
.scroll-top-link:hover .btn-text {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTION: BASE64 ENCODING ---
def get_b64_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            ext = img_path.split(".")[-1]
            return f"data:image/{ext};base64,{encoded}"
    return "https://via.placeholder.com/600x450"

# --- INITIALIZE STATE ARRAYS ---
if "total_reviews" not in st.session_state:
    st.session_state.total_reviews = 1259

if "customer_metrics" not in st.session_state:
    st.session_state.customer_metrics = {
        "First-Time Customer": 655,
        "Repeat Customer": 604
    }

# --- TRACK ACTIVE NAVIGATION ROUTE ---
current_params = st.query_params
selected_route = current_params.get("page", "HOME")
if isinstance(selected_route, list):
    selected_route = selected_route[0] if len(selected_route) > 0 else "HOME"

# Helper to easily inject the active line style class directly onto the active link element
def get_active_class(route_name):
    return "nk-nav-link active" if selected_route == route_name else "nk-nav-link"

# --- BRAND NAVIGATION HEADER (WITH TOP-ANCHOR DESTINATION INCLUDED) ---
st.markdown(f"""
<div id="top-anchor" style="position: relative; scroll-margin-top: 100px;"></div>
<div class="nk-header">
    <div class="nk-logo">TIAP HARI <span>KOPI</span></div>
    <div class="nk-nav">
        <a class="{get_active_class('HOME')}" href="?page=HOME" target="_self">HOME</a> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
        <a class="{get_active_class('MENU')}" href="?page=MENU" target="_self">MENU</a> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
        <a class="{get_active_class('RESERVATIONS')}" href="?page=RESERVATIONS" target="_self">RESERVATIONS</a> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
        <a class="{get_active_class('FEEDBACK')}" href="?page=FEEDBACK" target="_self">FEEDBACK</a> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
        <a class="{get_active_class('ABOUT US')}" href="?page=ABOUT US" target="_self">ABOUT US</a> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
        <a class="{get_active_class('LOG IN')}" href="?page=LOG IN" target="_self">LOG IN</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# CONDITIONAL RENDERING FRAMEWORK
# ==================================================

if selected_route == "HOME":
    st.markdown('<div class="nk-hero-title">Local Coffee, Premium Vibes.</div>', unsafe_allow_html=True)
    st.markdown('<div class="nk-hero-subtitle">Every Single Day Perfection</div>', unsafe_allow_html=True)

    # 1. Fetch targeted sliding graphics for Home hero banner
    home_images = [
        "images/tiapharibefore.jpg",
        "images/tiapharifront.jpg",
        "images/tiapharigrab.jpg",
        "images/tiapharibestdrinks.jpg"
    ]
    h_b64 = [get_b64_image(p) for p in home_images]

    # 2. Infinite Loop pure CSS Slider
    home_slider_html = f"""
    <style>
        .home-slider-wrapper {{
            width: 100%;
            max-width: 850px;
            margin: 0 auto 40px auto;
            overflow: hidden;
            border-radius: 16px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            background-color: #121e2e;
        }}
        .home-slider-track {{
            display: flex;
            width: 400%;
            animation: homeSlideLoop 6s cubic-bezier(0.85, 0, 0.15, 1) infinite;
        }}
        .home-slider-track img {{
            width: 25%;
            height: 480px;
            object-fit: cover;
        }}
        @keyframes homeSlideLoop {{
            0%, 20%   {{ transform: translateX(0); }}
            25%, 45%  {{ transform: translateX(-25%); }}
            50%, 70%  {{ transform: translateX(-50%); }}
            75%, 95%  {{ transform: translateX(-75%); }}
            100%      {{ transform: translateX(0); }}
        }}
    </style>
    <div class="home-slider-wrapper">
        <div class="home-slider-track">
            <img src="{h_b64[0]}">
            <img src="{h_b64[1]}">
            <img src="{h_b64[2]}">
            <img src="{h_b64[3]}">
        </div>
    </div>
    """
    st.components.v1.html(home_slider_html, height=500)

    st.markdown("<hr style='border-color: #1a2636; margin: 50px 0;'>", unsafe_allow_html=True)

    # --------------------------------------------------
    # PROMOTIONS AND ANNOUNCEMENT SECTION (STARBUCKS DESIGN)
    # --------------------------------------------------
    st.markdown("<h2 style='color:#ffffff; font-weight:800; text-align:center; margin-bottom: 35px;'>Promotions & Announcement</h2>", unsafe_allow_html=True)
    
    promo_b64_left = get_b64_image("images/waktuoperasi.jpg")
    promo_b64_right = get_b64_image("images/feedbackpic.jpg")
    
    promo_col1, promo_col2 = st.columns(2, gap="large")
    
    with promo_col1:
        st.markdown(f"""
        <div class="sb-promo-container" style="background-color: #d4e9e2;">
            <div class="sb-promo-img-side" style="background-image: url('{promo_b64_left}');"></div>
            <div class="sb-promo-text-side">
                <div class="sb-promo-title">Reserve your seat now!</div>
                <div class="sb-promo-desc">Share your favorites with someone special this coffee season.</div>
                <a class="sb-promo-btn" style="color: #1e3932; border-color: #1e3932;" href="?page=RESERVATIONS" target="_self"> &nbsp;&nbsp;Reserve a Seat</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with promo_col2:
        st.markdown(f"""
        <div class="sb-promo-container" style="background-color: #f9f9fa; background: #f2d1ca;">
            <div class="sb-promo-text-side">
                <div class="sb-promo-title">Leave us a review</div>
                <div class="sb-promo-desc">Share your experience with us and help us improve.</div>
                <a class="sb-promo-btn" style="color: #1e3932; border-color: #1e3932;" href="?page=FEEDBACK" target="_self"> &nbsp;&nbsp;Leave Feedback</a>
            </div>
            <div class="sb-promo-img-side" style="background-image: url('{promo_b64_right}');"></div>
        </div>
        """, unsafe_allow_html=True)

    # ASYMMETRIC IMAGE GRID IN PROMOS SECTION (WITH REDIRECT HYPERLINKS ACTIVATED)
    grid_img_main = get_b64_image("images/promo1.jpg")
    grid_img_sub1 = get_b64_image("images/promo6.jpg")
    grid_img_sub2 = get_b64_image("images/promo3.jpg")
    grid_img_sub3 = get_b64_image("images/promo2.jpg")
    grid_img_sub4 = get_b64_image("images/promo5.jpg")

    st.markdown(f"""
    <div class="sb-grid-layout">
        <div class="sb-grid-left-featured">
            <a href="https://wa.me/60134944337" target="_blank">
                <img src="{grid_img_main}" alt="Monthly Promotions" style="cursor: pointer;">
            </a>
        </div>
        <div class="sb-grid-right-stack">
            <div class="sb-grid-item">
                <a href="https://www.instagram.com/TiapHariKopi" target="_blank">
                    <img src="{grid_img_sub1}" style="cursor: pointer;">
                </a>
            </div>
            <div class="sb-grid-item">
                <a href="https://r.grab.com/g/6-20260612_211256_9ef30256bb924d40bac7573c90142773_MEXMPS-1-C3NTVKDZLZCHTJ" target="_blank">
                    <img src="{grid_img_sub2}" style="cursor: pointer;">
                </a>
            </div>
            <div class="sb-grid-item">
                <a href="?page=MENU" target="_self">
                    <img src="{grid_img_sub3}" style="cursor: pointer;">
                </a>
            </div>
            <div class="sb-grid-item">
                <a href="?page=MENU" target="_self">
                    <img src="{grid_img_sub4}" style="cursor: pointer;">
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif selected_route == "MENU":
    # --------------------------------------------------
    # ISOLATED MENU COMPONENT PAGE
    # --------------------------------------------------
    st.markdown("<h2 style='color:#ffffff; font-weight:800; text-align:center;'>Explore Our Signature Menu</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#92a4b8; margin-bottom:30px;'>Crafted to give you the perfect boost</p>", unsafe_allow_html=True)

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
    ]

    filter_col1, filter_col2, filter_col3 = st.columns([1, 1.5, 1])
    with filter_col2:
        selected_category = st.selectbox("✨ Select Category to Explore:", options=["All Items", "Beverage", "Dessert", "Western Food", "Local Food"], index=0)

    filtered_items = menu_items if selected_category == "All Items" else [item for item in menu_items if item["category"] == selected_category]

    m_cols = st.columns(3, gap="large")
    for idx, item in enumerate(filtered_items):
        with m_cols[idx % 3]:
            try:
                st.image(item["image"], width=320)
            except Exception:
                st.image("https://via.placeholder.com/300x220", width=320)
                
            st.markdown(f"""
            <div class="nk-card" style="margin-top: -10px; border-top-left-radius: 0px; border-top-right-radius: 0px; margin-bottom: 30px;">
                <div class="nk-menu-cat">{item['category']}</div>
                <div class="nk-menu-title" style="margin-top: 5px; font-size:16px; color:#111111;">{item['name']}</div>
                <div style="margin-top: 15px;">
                    <div class="nk-menu-price">RM {item['price']:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif selected_route == "RESERVATIONS":
    st.markdown("<h3 style='color:#ffffff; font-weight:700; margin-bottom:20px;'>Secure Orders & Bookings</h3>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2, gap="large")
    with b_col1:
        st.markdown("""
        <div class="nk-card">
            <h4 style="color:#111111; font-weight:700;">📲 Reserve via WhatsApp</h4>
            <p style="color:#555555; font-size:14px;">Skip the queue! Book your table session seamlessly with our baristas online.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Book Table via WhatsApp", "https://wa.me/60134944337")
    with b_col2:
        st.markdown("""
        <div class="nk-card">
            <h4 style="color:#111111; font-weight:700;">🛵 Instant Grab Delivery</h4>
            <p style="color:#555555; font-size:14px;">Craving our local snacks or main courses? Hit the button below to buy on GrabFood.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Find Us On GrabFood", "https://r.grab.com/g/6-20260612_211256_9ef30256bb924d40bac7573c90142773_MEXMPS-1-C3NTVKDZLZCHTJ")

# --------------------------------------------------
    # FIXED GOOGLE MAP COMPONENT RIGHT HERE 
    # --------------------------------------------------
    st.markdown("<h3 style='color:#ffffff; font-weight:700; margin-top:25px; margin-bottom:1.5px;'>Or come find us here!</h3>", unsafe_allow_html=True)
    
    # Updated embed block targeted exactly to Tiap Hari Kopi's specific CID / place token with internal zoom fixed
    map_iframe_html = """
    <div style="width: 100%; border-radius: 14px; overflow: hidden; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); border: 1px solid #1a2636;">
        <iframe 
            src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d3000.0!2d102.2779677!3d6.0939054!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31b6b11d04d558df%3A0xa8946be7fee39ef5!2sTiap%20Hari%20Kopi!5e0!3m2!1sen!2smy!4v1718220000000!5m2!1sen!2smy" 
            width="100%" 
            height="480" 
            style="border:0;" 
            allowfullscreen="" 
            loading="lazy" 
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
    </div>
    """
    st.components.v1.html(map_iframe_html, height=500)

elif selected_route == "FEEDBACK":
    st.markdown("<h2 style='color: white;'>💬 Customer Feedback Portal</h2>", unsafe_allow_html=True)
    st.write("We would love to hear your thoughts about our coffee and service!")
    
    # 1. PECAHKAN KEPADA 2 KOLUM BERSEBELAHAN (Kiri dan Kanan)
    col1, col2 = st.columns([1.2, 1])
    
    # KOLUM KIRI: Tempat customer isi form feedback
    with col1:
        st.markdown("<h4 style='color: white;'>Submit Your Feedback</h4>", unsafe_allow_html=True)
        with st.form(key='feedback_form', clear_on_submit=True):
            name = st.text_input("Name")
            email = st.text_input("Email")
            
            customer_type = st.radio(
                "Customer Type",
                options=["First-time Customer", "Repeat Customer"],
                horizontal=True
            )
            
            rating = st.slider("Rating", 1, 5, 5)
            comments = st.text_area("Your Feedback", height=120)
            
            submit_button = st.form_submit_button(label="Submit Feedback", use_container_width=True)
            
            if submit_button:
                if name and comments:
                    # Proses Analisis Sentiment secara automatik
                    from textblob import TextBlob
                    polarity = TextBlob(str(comments)).sentiment.polarity
                    if polarity > 0.05: 
                        sentiment = 'Positive'
                    elif polarity < -0.05: 
                        sentiment = 'Negative'
                    else: 
                        sentiment = 'Neutral'
                    
                    # Format Waktu Malaysia/Asia
                    from datetime import datetime, timedelta
                    my_time = datetime.utcnow() + timedelta(hours=8)
                    date_str = my_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    import os
                    db_file = 'reviews_database.csv'
                    
                    # Susun aturan data mengikut lajur yang betul (Review dahulu, baru Customer Type)
                    new_row = pd.DataFrame({
                        "Date": [date_str],
                        "Platform": ["Web Portal"],
                        "Review": [comments],
                        "Customer Type": [customer_type],
                        "Sentiment": [sentiment]
                    })
                    
                    # Simpan secara selamat mengekalkan susunan nama lajur (pd.concat)
                    if os.path.exists(db_file) and os.path.getsize(db_file) > 0:
                        df_existing = pd.read_csv(db_file)
                        df_combined = pd.concat([df_existing, new_row], ignore_index=True)
                        df_combined.to_csv(db_file, index=False)
                    else:
                        new_row.to_csv(db_file, index=False)
                    
                    st.success(f"Thank you {name}! Your feedback has been recorded successfully.")
                    import time
                    time.sleep(1)
                    st.rerun() # Refresh app auto untuk tunjuk data baru di kolum kanan
                else:
                    st.error("Please fill in your Name and Feedback comments.")

    # KOLUM KANAN: Paparan rekod review sedia ada (Live View terus dari CSV)
    with col2:
        st.markdown("<h4 style='color: white;'>Recent Reviews</h4>", unsafe_allow_html=True)
        import os
        db_file = 'reviews_database.csv'
        
        if os.path.exists(db_file) and os.path.getsize(db_file) > 0:
            df_reviews = pd.read_csv(db_file)
            if not df_reviews.empty:
                # Susun senarai lajur yang hendak dipaparkan di skrin customer
                display_cols = ["Date", "Review", "Customer Type", "Sentiment"]
                existing_cols = [col for col in display_cols if col in df_reviews.columns]
                
                # Sediakan jadual dengan data terbaru berada di kedudukan paling atas (.iloc[::-1])
                st.dataframe(
                    df_reviews[existing_cols].iloc[::-1].head(8), 
                    use_container_width=True, 
                    hide_index=True
                )
            else:
                st.info("No customer reviews recorded yet.")
        else:
            st.info("No customer reviews recorded yet.")

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown('<h3 style="color: white; margin-bottom: 20px;">What they say about us (Google Reviews)</h3>', unsafe_allow_html=True)
        
        # Base64 Conversions for NurZetty Sofia review assets
        zetty_avatar = get_b64_image("images/zettypic.png")
        zetty_b64_1 = get_b64_image("images/zetty1.jpg")
        zetty_b64_2 = get_b64_image("images/zetty2.jpg")
        zetty_b64_3 = get_b64_image("images/zetty3.jpg")
        zetty_b64_4 = get_b64_image("images/zetty4.jpg")
        
        # Base64 placeholders for Isabella Anne and generic review assets
        isabella_avatar = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100"
        ken_avatar = get_b64_image("images/kenpic.png")
        khairul_avatar = "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100"
        
        ken_thumb_1 = get_b64_image("images/ken1.jpg")
        ken_thumb_2 = get_b64_image("images/ken2.jpg")
        ken_thumb_3 = get_b64_image("images/ken3.jpg")

        # Global Destination URL Link to Tiap Hari Kopi's Google Reviews
        google_review_url = "https://www.google.com/search?sca_esv=53e31815f719979f&sxsrf=ANbL-n7zs_790y4jCVUkOo1b70jlyeE_nw:1781322130917&q=tiap+hari+kopi&si=AL3DRZEsmMGCryMMFSHJ3StBhOdZ2-6yYkXd_doETEE1OR-qOZQOnwwztQwO3wTDCaDKWaqaSyvu4yV2m6x06uINzOpws4CyOToEV3OrYAkC5mcrndY21kiEjpNkzgiPnb1DqiBpkJtY&sa=X&ved=2ahUKEwju0d-GpoOVAxXtwjgGHUpbEVYQrrQLegQIIhAA&biw=1280&bih=585&dpr=1.5"

        # Open the scrolling viewport container wrapper
        st.markdown('<div class="reviews-scroll-container">', unsafe_allow_html=True)
        
        # --- REVIEW 1: NurZetty Sofia ---
        st.markdown(f"""
        <a href="{google_review_url}" target="_blank" class="gr-link-wrapper">
            <div class="google-review-card">
                <div class="gr-header">
                    <div class="gr-profile">
                        <img class="gr-avatar" src="{zetty_avatar}" alt="Avatar">
                        <div class="gr-user-info">
                            <span class="gr-name">NurZetty Sofia</span>
                            <span class="gr-meta">6 ulasan • 6 foto</span>
                        </div>
                    </div>
                    <div class="gr-more-btn">⋮</div>
                </div>
                <div class="gr-stars-row">
                    <span class="gr-stars">★★★★★</span>
                    <span class="gr-time">3 minggu yang lalu</span>
                    <span class="gr-badge" style="background-color:#1a2636; color:#e8eaed; font-size:9px; padding:2px 5px; border-radius:3px;">BAHARU</span>
                </div>
                <div class="gr-text">
                    Saya kenal TiapHari ni semenjak 2022. Speciality mmg Nisse Latte dan Kacang Phool. Walaupun KB ni byk kedai kopi, tp tak boleh lagi lawan Nisse latte TiapHari (ice/hot dua2 sedap) dan takde tempat lain nak cari kacang phool. Bukan tak ... <span style="color:#8ab4f8;">Lagi</span>
                </div>
                <div class="gr-images-grid">
                    <img class="gr-img" src="{zetty_b64_1}">
                    <img class="gr-img" src="{zetty_b64_2}">
                    <img class="gr-img" src="{zetty_b64_3}">
                    <img class="gr-img" src="{zetty_b64_4}">
                </div>
                <div class="gr-footer">
                    <div style="display:flex; align-items:center; gap:4px;">❤️ <span>1</span></div>
                    <div style="display:flex; align-items:center; gap:4px;">🙏 <span>2</span></div>
                    <div>🔗</div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

        # --- REVIEW 2: Farhana (Website Feedback) ---
        st.markdown("""
        <div class="local-review-card">
            <div style="display: flex; gap: 4px; margin-bottom: 4px; color: #fbbc05; font-size:13px;">★★★★★</div>
            <span style="font-weight: bold; color: #8ab4f8; font-size:14px;">Farhana</span> 
            <div style="color: #bdc1c6; font-size:13px; margin-top:4px; line-height:1.4;">
                — Super friendly service. Perfect environment to chill out or focus on remote work. (Verified Website Feedback)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- REVIEW 3: Isabella Anne ---
        st.markdown(f"""
        <a href="{google_review_url}" target="_blank" class="gr-link-wrapper">
            <div class="google-review-card">
                <div class="gr-header">
                    <div class="gr-profile">
                        <img class="gr-avatar" src="{isabella_avatar}" alt="Avatar">
                        <div class="gr-user-info">
                            <span class="gr-name">Isabella Anne</span>
                            <span class="gr-meta">Jurupandu Tempatan • 36 ulasan • 23 foto</span>
                        </div>
                    </div>
                    <div class="gr-more-btn">⋮</div>
                </div>
                <div class="gr-stars-row">
                    <span class="gr-stars">★★★★★</span>
                    <span class="gr-time">4 bulan yang lalu</span>
                </div>
                <div class="gr-text">
                    Good food , just parking abit hard
                    <div style="background-color: #17202a; padding: 8px 12px; border-radius: 6px; margin-top: 8px; font-size: 12px; color: #bdc1c6;">
                        <b>Makanan:</b> 5/5  |  <b>Perkhidmatan:</b> 5/5  |  <b>Suasana:</b> 5/5
                    </div>
                    <span style="font-size:12px; color:#8ab4f8; margin-top:8px; display:inline-block;">Lihat terjemahan (Melayu)</span>
                </div>
                <div class="gr-footer">
                    <div style="display:flex; align-items:center; gap:4px;">❤️ <span>1</span></div>
                    <div>🔗</div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

        # --- REVIEW 4: Koyoraka Ken (Google Review matching image_124948.jpg layout) ---
        st.markdown(f"""
        <a href="{google_review_url}" target="_blank" class="gr-link-wrapper">
            <div class="google-review-card">
                <div class="gr-header">
                    <div class="gr-profile">
                        <img class="gr-avatar" src="{ken_avatar}" alt="Avatar">
                        <div class="gr-user-info">
                            <span class="gr-name">Koyoraka Ken</span>
                            <span class="gr-meta">Jurupandu Tempatan • 794 ulasan • 4241 foto</span>
                        </div>
                    </div>
                    <div class="gr-more-btn">⋮</div>
                </div>
                <div class="gr-stars-row">
                    <span class="gr-stars">★★★★☆</span>
                    <span class="gr-time">Diedit setahun yang lalu</span>
                </div>
                <div class="gr-text" style="color: #9aa0a6; font-size: 12.5px; margin-bottom: 6px;">
                    Makan di kedai | Lain-lain
                </div>
                <div class="gr-text">
                    Kopi di sini sedap dan tidak terlalu mahal cuma kurang ekslusif daripada segi bekas yang digunakan untuk makan di situ. Sekiranya digunakan gelas kaca untuk makan dengan logo pasti lebih menarik&nbsp;dan kena dengan harga.......
                </div>
                <div class="gr-images-grid">
                    <img class="gr-img" src="{ken_thumb_1}">
                    <img class="gr-img" src="{ken_thumb_2}">
                    <img class="gr-img" src="{ken_thumb_3}">
                </div>
                <div class="gr-footer">
                    <div style="display:flex; align-items:center; gap:4px;">❤️</div>
                    <div style="display:flex; align-items:center; gap:4px;">🙏 <span>3</span></div>
                    <div>🔗</div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

        # --- REVIEW 5: Khairul Amrin (Google Review) ---
        st.markdown(f"""
        <a href="{google_review_url}" target="_blank" class="gr-link-wrapper">
            <div class="google-review-card">
                <div class="gr-header">
                    <div class="gr-profile">
                        <img class="gr-avatar" src="{khairul_avatar}" alt="Avatar">
                        <div class="gr-user-info">
                            <span class="gr-name">Khairul Amrin</span>
                            <span class="gr-meta">12 ulasan</span>
                        </div>
                    </div>
                    <div class="gr-more-btn">⋮</div>
                </div>
                <div class="gr-stars-row">
                    <span class="gr-stars">★★★★★</span>
                    <span class="gr-time">2 bulan yang lalu</span>
                </div>
                <div class="gr-text">
                    Pasta dia portion padu & harga berbaloi sangat area Kubang Kerian ni. Nisse Latte icing tak manis potong kaki, just nice berkrim. Memang port lepak tetap lepas balik kerja.
                </div>
                <div class="gr-footer">
                    <div style="display:flex; align-items:center; gap:4px;">❤️ <span>2</span></div>
                    <div>🔗</div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

        # --- REVIEW 6: Sarah M. (Verified Website Feedback) ---
        st.markdown("""
        <div class="local-review-card" style="border-left-color: #00g5f6;">
            <div style="display: flex; gap: 4px; margin-bottom: 4px; color: #fbbc05; font-size:13px;">★★★★★</div>
            <span style="font-weight: bold; color: #8ab4f8; font-size:14px;">Sarah M.</span> 
            <div style="color: #bdc1c6; font-size:13px; margin-top:4px; line-height:1.4;">
                — Ordered via the web interface for pickup. The food was hot, packed clean, and the staff even walked it out to my car because parking was full. Outstanding hospitality! (Verified Website Feedback)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- REVIEW 7: Bryan T. (Verified Website Feedback) ---
        st.markdown("""
        <div class="local-review-card" style="border-left-color: #00g5f6;">
            <div style="display: flex; gap: 4px; margin-bottom: 4px; color: #fbbc05; font-size:13px;">★★★★☆</div>
            <span style="font-weight: bold; color: #8ab4f8; font-size:14px;">Bryan T.</span> 
            <div style="color: #bdc1c6; font-size:13px; margin-top:4px; line-height:1.4;">
                — The Kacang Phool is authentic and complex. A rare find in Kota Bharu cafés. Docked one star just because seating fills up so quickly on weekends! (Verified Website Feedback)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Close the scrolling viewport container wrapper safely
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h2 style='color: white;'>💬 Share Your Feedback</h2>", unsafe_allow_html=True)
    st.write("We would love to hear your thoughts about our coffee and service!")
    
    with st.form(key='feedback_form', clear_on_submit=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        
        #Penambahan Input Radio bagi Jenis Pelanggan
        customer_type = st.radio(
            "Customer Type",
            options=["First-time Customer", "Repeat Customer"],
            horizontal=True
        )
        
        rating = st.slider("Rating", 1, 5, 5)
        comments = st.text_area("Your Feedback")
        
        submit_button = st.form_submit_button(label="Submit Feedback")
        
        if submit_button:
            if name and comments:
                Proses Analisis Sentiment (Positive/Negative/Neutral)
                from textblob import TextBlob
                polarity = TextBlob(str(comments)).sentiment.polarity
                if polarity > 0.05: 
                    sentiment = 'Positive'
                elif polarity < -0.05: 
                    sentiment = 'Negative'
                else: 
                    sentiment = 'Neutral'
                
                # Format Masa Semasa
                from datetime import datetime, timedelta
                my_time = datetime.utcnow() + timedelta(hours=8)
                date_str = my_time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Simpan Data ke dalam CSV (Sama dengan database app.py)
                import os
                db_file = 'reviews_database.csv'
                
                new_row = pd.DataFrame({
                    "Date": [date_str],
                    "Platform": ["Web Portal"],
                    "Customer Type": [customer_type],
                    "Review": [comments],
                    "Sentiment": [sentiment]
                })
                
                if os.path.exists(db_file):
                    new_row.to_csv(db_file, mode='a', header=False, index=False)
                else:
                    new_row.to_csv(db_file, index=False)
                
                st.success(f"Thank you {name}! Your feedback as a '{customer_type}' has been saved to our database.")
            else:
                st.error("Please fill in your Name and Feedback comments.")

elif selected_route == "ABOUT US":
    st.markdown("<h2 style='color:#ffffff; font-weight:700; margin-bottom:5px;'>About Us</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#b0b3b8; font-size:16px; margin-bottom:25px;'>Get to know the story behind Tiap Hari Kopi.</p>", unsafe_allow_html=True)
    
    # ------------------------------------------------------------------
    # 1. VISUAL GALLERY & STORY HIGHLIGHT (Moved Up to Capture Interest First)
    # ------------------------------------------------------------------
    st.markdown("### 📸 Gallery and Our Story")

    slider_images = [
        "images/tiapharibefore.jpg",
        "images/tiapharifront.jpg",
        "images/tiapharigrab.jpg",
        "images/tiapharibestdrinks.jpg",
        "images/tiapharipasta.jpg",
        "images/tiapharisnack.jpg",
        "images/tiapharikacangphool.jpg",
        "images/veggiespringrolls.jpg",      
        "images/crispyveggiecucur.jpg"       
    ]

    b64_srcs = [get_b64_image(p) for p in slider_images]

    slider_html = f"""
    <style>
        .slider-container {{
            width: 100%;
            overflow: hidden;
            border-radius: 12px;
            background-color: #0b131f;
            padding: 15px 0;
        }}
        .slider-track {{
            display: flex;
            width: 300%; 
            gap: 16px;
            padding-left: 8px;
            padding-right: 8px;
            box-sizing: border-box;
            animation: slide-9-images 6s ease-in-out infinite; 
        }}
        .slider-track:hover {{
            animation-play-state: paused;
        }}
        .slider-track img {{
            width: calc(33.333vw - 22px); 
            height: 280px;
            object-fit: cover;
            border-radius: 8px;
            flex-shrink: 0;
        }}
        @keyframes slide-9-images {{
            0%, 25% {{ transform: translateX(0); }}
            33%, 58% {{ transform: translateX(calc(-100vw + 8px)); }}
            66%, 91% {{ transform: translateX(calc(-200vw + 16px)); }}
            100% {{ transform: translateX(0); }}
        }}
    </style>
    <div class="slider-container">
        <div class="slider-track">
            <img src="{b64_srcs[0]}">
            <img src="{b64_srcs[1]}">
            <img src="{b64_srcs[2]}">
            
            <img src="{b64_srcs[3]}">
            <img src="{b64_srcs[4]}">
            <img src="{b64_srcs[5]}">
            
            <img src="{b64_srcs[6]}">
            <img src="{b64_srcs[7]}">
            <img src="{b64_srcs[8]}">
        </div>
    </div>
    """
    st.components.v1.html(slider_html, height=315)

    st.markdown("""
    <div style='background-color:#004481; color:#ffffff; padding:20px; border-radius:15px; margin-top:15px; margin-bottom:30px; text-align:center; font-size:16px; font-weight:600;'>
        ✨ Our journey started from a small idea and grew into a cozy café loved by many. <br>
        Every cup of coffee we serve carries passion, comfort and a little bit of happiness ☕💛
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # 2. CORE VALUE PROPOSITION CARD
    # ------------------------------------------------------------------
    with st.container(border=True):
        st.markdown("### ☕ Welcome to Tiap Hari Kopi")
        st.write(
            "Established in 2021, Tiap Hari Kopi is your go-to local cafe in **Kubang Kerian**. "
            "We pride ourselves on creating a warm, vibrant space where community, comfort and great food come together."
        )
        
        st.write("---") 
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📍 Strategic Location")
            st.write(
                "Conveniently situated near McDonald's Kubang Kerian, "
                "USM colleges and student hostels—making us the perfect neighborhood spot."
            )
            
            st.markdown("#### 🌐 Study & Discussion Friendly")
            st.write("Equipped with high-speed **Free Wi-Fi** we offers a comfortable and productive space for students and professionals alike.")
            
        with col2:
            st.markdown("#### 🍳 Fusion Menu")
            st.write("Enjoy a unique culinary experience featuring a delightful combination of **Eastern & Western food** alongside premium coffee beverages.")
            
            st.markdown("#### 👥 Welcoming Everyone")
            st.write("While our main heartbeat is to serve the vibrant student community, our doors are open to all age groups from children to the elderly.")

    # ------------------------------------------------------------------
    # 3. INTERACTIVE DIGITAL BRANDING HUBS
    # ------------------------------------------------------------------
    st.markdown("<hr style='border-color: #1a2636; margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#ffffff; font-weight:800; text-align:center; margin-bottom:10px;'>📲 Social Media Hub</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#92a4b8; margin-bottom:40px;'>Experience our daily live updates on phone views. Click to redirect to our official profiles.</p>", unsafe_allow_html=True)

    placeholder_img = b64_srcs[1] 

    ig_srcs = [get_b64_image(f"images/ig{i}.jpg") for i in range(1, 10)]
    fb_srcs = [get_b64_image(f"images/fb{i}.jpg") for i in range(1, 10)]

    social_col1, social_col2 = st.columns(2)

    with social_col1:
        st.markdown("<h4 style='text-align:center; color:#ffffff; font-weight:700; margin-bottom:15px;'>Our Instagram</h4>", unsafe_allow_html=True)
        instagram_mock_html = f"""
        <style>
            .phone-link-wrapper {{
                text-decoration: none !important;
                color: inherit !important;
                display: block;
                cursor: pointer;
            }}
            .phone-link-wrapper * {{
                text-decoration: none !important;
            }}
            .phone-mockup {{
                width: 100%;
                max-width: 350px;
                height: 600px;
                background-color: #000000;
                border: 8px solid #2a2a2a;
                border-radius: 36px;
                margin: 0 auto;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                box-shadow: 0 20px 40px rgba(0,0,0,0.7);
                color: #ffffff;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            .phone-header {{
                padding: 12px 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: #000000;
                z-index: 10;
            }}
            .phone-header-left {{
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 16px;
                font-weight: 700;
            }}
            .phone-content-scroll {{
                flex: 1;
                overflow-y: auto;
                padding-right: 2px;
            }}
            .phone-content-scroll::-webkit-scrollbar {{
                width: 5px;
            }}
            .phone-content-scroll::-webkit-scrollbar-track {{
                background: #000000;
            }}
            .phone-content-scroll::-webkit-scrollbar-thumb {{
                background: #333333;
                border-radius: 10px;
            }}
            .phone-profile-section {{
                padding: 5px 15px 10px 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 15px;
            }}
            .mock-avatar-container {{
                flex-shrink: 0;
            }}
            .mock-avatar {{
                width: 76px;
                height: 76px;
                border-radius: 50%;
                object-fit: cover;
                border: 2px solid #000000;
                box-shadow: 0 0 0 2px #262626;
            }}
            .phone-stats-container {{
                display: flex;
                flex: 1;
                justify-content: space-around;
                text-align: center;
            }}
            .stat-box {{
                display: flex;
                flex-direction: column;
            }}
            .stat-num {{
                font-weight: 700;
                font-size: 15px;
                color: #ffffff;
            }}
            .stat-label {{
                font-size: 12px;
                color: #f5f5f5;
            }}
            .bio-section {{
                font-size: 13px;
                line-height: 1.4;
                padding: 0 15px 10px 15px;
            }}
            .bio-name {{
                font-weight: 700;
                color: #ffffff;
                font-size: 14px;
                margin-bottom: 2px;
            }}
            .bio-category {{
                color: #a8a8a8;
                font-size: 13px;
                margin-bottom: 2px;
            }}
            .bio-text {{
                color: #ffffff;
            }}
            .bio-link {{
                color: #c1d1f0;
                font-weight: 500;
                margin-top: 2px;
            }}
            .bio-badges {{
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 8px;
            }}
            .bio-badge {{
                background-color: #121212;
                border: 1px solid #262626;
                padding: 4px 10px;
                border-radius: 15px;
                font-size: 11px;
                color: #ffffff;
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .action-buttons {{
                display: flex;
                gap: 6px;
                padding: 5px 15px 15px 15px;
            }}
            .mock-btn {{
                flex: 1;
                background-color: #262626;
                color: white !important;
                text-align: center;
                padding: 7px 0;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }}
            .mock-btn-blue {{
                background-color: #0095f6;
            }}
            .mock-btn-arrow {{
                flex: 0 0 35px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .grid-feed {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2px;
                background: #000;
                padding: 2px 0 20px 0;
            }}
            .feed-img {{
                width: 100%;
                aspect-ratio: 1 / 1;
                object-fit: cover;
            }}
        </style>
        <a class="phone-link-wrapper" href="https://www.instagram.com/tiapharikopi/?hl=ms" target="_blank">
            <div class="phone-mockup">
                <div class="phone-header">
                    <div class="phone-header-left">
                        <span>⟨</span>
                        <span>tiapharikopi</span>
                    </div>
                    <span style="font-size:16px; color:#fff; display: flex; gap: 15px;"><span>🔔</span><span>⋮</span></span>
                </div>
                <div class="phone-content-scroll">
                    <div class="phone-profile-section">
                        <div class="mock-avatar-container">
                            <img class="mock-avatar" src="{placeholder_img}">
                        </div>
                        <div class="phone-stats-container">
                            <div class="stat-box"><span class="stat-num">112</span><span class="stat-label">posts</span></div>
                            <div class="stat-box"><span class="stat-num">3,331</span><span class="stat-label">followers</span></div>
                            <div class="stat-box"><span class="stat-num">84</span><span class="stat-label">following</span></div>
                        </div>
                    </div>
                    <div class="bio-section">
                        <div class="bio-name">TiapHari Kopi</div>
                        <div class="bio-category">Coffee shop</div>
                        <div class="bio-text">
                            📍 Kubang Kerian, Kelantan<br>
                            Open Daily 3PM – 11PM<br>
                            Kitchen last order @ 10PM<br>
                            ❌ Closed on W... <span style="color:#a8a8a8;">more</span>
                        </div>
                        <div class="bio-link">🔗 linktr.ee/tiapharikopi</div>
                        <div class="bio-badges">
                            <div class="bio-badge">🌀 tiapharikopi</div>
                            <div class="bio-badge">👤 Facebook profile</div>
                            <div class="bio-badge">👤 TiapHari Kopi</div>
                        </div>
                    </div>
                    <div class="action-buttons">
                        <div class="mock-btn mock-btn-blue">Follow</div>
                        <div class="mock-btn">Message</div>
                        <div class="mock-btn">Contact</div>
                        <div class="mock-btn mock-btn-arrow">∨</div>
                    </div>
                    <div class="grid-feed">
                        <img class="feed-img" src="{ig_srcs[0]}">
                        <img class="feed-img" src="{ig_srcs[1]}">
                        <img class="feed-img" src="{ig_srcs[2]}">
                        <img class="feed-img" src="{ig_srcs[3]}">
                        <img class="feed-img" src="{ig_srcs[4]}">
                        <img class="feed-img" src="{ig_srcs[5]}">
                        <img class="feed-img" src="{ig_srcs[6]}">
                        <img class="feed-img" src="{ig_srcs[7]}">
                        <img class="feed-img" src="{ig_srcs[8]}">
                        <img class="feed-img" src="{placeholder_img}">
                        <img class="feed-img" src="{b64_srcs[3]}">
                        <img class="feed-img" src="{b64_srcs[5]}">
                        <img class="feed-img" src="{b64_srcs[6]}">
                        <img class="feed-img" src="{b64_srcs[7]}">
                        <img class="feed-img" src="{b64_srcs[4]}">
                    </div>
                </div>
            </div>
        </a>
        """
        st.components.v1.html(instagram_mock_html, height=660)

    with social_col2:
        st.markdown("<h4 style='text-align:center; color:#ffffff; font-weight:700; margin-bottom:15px;'>Our Facebook</h4>", unsafe_allow_html=True)
        facebook_mock_html = f"""
        <style>
            .phone-link-wrapper {{
                text-decoration: none !important;
                color: inherit !important;
                display: block;
                cursor: pointer;
            }}
            .phone-link-wrapper * {{
                text-decoration: none !important;
            }}
            .phone-mockup {{
                width: 100%;
                max-width: 350px;
                height: 600px;
                background-color: #18191a;
                border: 8px solid #2a2a2a;
                border-radius: 36px;
                margin: 0 auto;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                box-shadow: 0 20px 40px rgba(0,0,0,0.7);
                color: #ffffff;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            .phone-header {{
                padding: 15px 15px 10px 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-weight: bold;
                background-color: #242526;
                border-bottom: 1px solid #3a3b3c;
                z-index: 10;
            }}
            .phone-content-scroll {{
                flex: 1;
                overflow-y: auto;
                padding-right: 2px;
            }}
            .phone-content-scroll::-webkit-scrollbar {{
                width: 5px;
            }}
            .phone-content-scroll::-webkit-scrollbar-track {{
                background: #18191a;
            }}
            .phone-content-scroll::-webkit-scrollbar-thumb {{
                background: #444444;
                border-radius: 10px;
            }}
            .fb-cover-banner {{
                width: 100%;
                height: 120px;
                background-color: #242526;
                position: relative;
            }}
            .fb-cover-banner img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            .fb-avatar {{
                position: absolute;
                bottom: -25px;
                left: 15px;
                width: 70px;
                height: 70px;
                border-radius: 50%;
                border: 4px solid #18191a;
                object-fit: cover;
            }}
            .fb-meta-info {{
                padding: 35px 15px 10px 15px;
            }}
            .fb-title {{
                font-size: 18px;
                font-weight: 800;
                color: #ffffff;
            }}
            .fb-handle {{
                font-size: 12px;
                color: #b0b3b8;
                margin-top: 2px;
            }}
            .fb-followers {{
                font-size: 12px;
                color: #e4e6eb;
                margin-top: 6px;
                margin-bottom: 12px;
            }}
            .fb-detailed-bio {{
                font-size: 13px;
                color: #e4e6eb;
                line-height: 1.5;
                padding: 0 15px 15px 15px;
                border-bottom: 1px solid #3a3b3c;
            }}
            .action-buttons {{
                display: flex;
                gap: 6px;
                padding: 15px;
            }}
            .mock-btn {{
                flex: 1;
                background-color: #3a3b3c;
                color: white !important;
                text-align: center;
                padding: 7px 0;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }}
            .mock-btn-blue {{
                background-color: #1877f2;
            }}
            .grid-feed {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2px;
                background: #18191a;
                padding: 2px 0 20px 0;
            }}
            .feed-img {{
                width: 100%;
                aspect-ratio: 1 / 1;
                object-fit: cover;
            }}
        </style>
        <a class="phone-link-wrapper" href="https://www.facebook.com/tiapharikopimy/?locale=ms_MY" target="_blank">
            <div class="phone-mockup">
                <div class="phone-header">
                    <span style="color:#fff;">🔍 Tiap Hari Kopi</span>
                    <span style="color:#fff;">💬</span>
                </div>
                <div class="phone-content-scroll">
                    <div class="fb-cover-banner">
                        <img src="{b64_srcs[3]}">
                        <img class="fb-avatar" src="{placeholder_img}">
                    </div>
                    <div class="fb-meta-info">
                        <div class="fb-title">Tiap Hari Kopi</div>
                        <div class="fb-handle">@tiapharikopimy • Coffee Shop</div>
                        <div class="fb-followers">👥 <b>3.3K</b> followers • <b>295</b> following</div>
                    </div>
                    <div class="fb-detailed-bio">
                        📍 Kubang Kerian, Kelantan<br>
                        Open Daily 3PM – 11PM<br>
                        Kitchen last order @ 10PM<br>
                        ❌ Closed on Wednesday<br>
                        <span style="color: #b0b3b8; font-size: 11px;">EDANAZ ENTERPRISE (KT0487519-X)</span>
                    </div>
                    <div class="action-buttons">
                        <div class="mock-btn mock-btn-blue">✓ Liked</div>
                        <div class="mock-btn">Message</div>
                    </div>
                    <div class="grid-feed">
                        <img class="feed-img" src="{fb_srcs[0]}">
                        <img class="feed-img" src="{fb_srcs[1]}">
                        <img class="feed-img" src="{fb_srcs[2]}">
                        <img class="feed-img" src="{fb_srcs[3]}">
                        <img class="feed-img" src="{fb_srcs[4]}">
                        <img class="feed-img" src="{fb_srcs[5]}">
                        <img class="feed-img" src="{fb_srcs[6]}">
                        <img class="feed-img" src="{fb_srcs[7]}">
                        <img class="feed-img" src="{fb_srcs[8]}">
                    </div>
                </div>
            </div>
        </a>
        """
        st.components.v1.html(facebook_mock_html, height=660)

    # ==================================================
    # HELPER FUNCTIONS TO FETCH LIVE FOLLOWER COUNTS
    # ==================================================
    @st.cache_data(ttl=10800) 
    def get_live_followers():
        counts = {
            "facebook": "3.3K",
            "instagram": "3,331",
            "tiktok": "766"
        }
        
        try:
            ig_url = "https://www.instagram.com/tiapharikopi/?__a=1&__d=dis"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(ig_url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = data['graphql']['user']['edge_followed_by']['count']
                counts["instagram"] = f"{count:,}"
        except:
            pass 
            
        try:
            tt_url = "https://www.tiktok.com/@tiapharikopi"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            res = requests.get(tt_url, headers=headers, timeout=5)
            match = re.search(r'"followerCount":(\d+)', res.text)
            if match:
                count = int(match.group(1))
                counts["tiktok"] = f"{count:,}" if count < 1000 else f"{count/1000:.1f}K"
        except:
            pass

        return counts

    live_counts = get_live_followers()

    # ==================================================
    # FOOTER SECTION (Tiap Hari Kopi Style)
    # ==================================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    # =====================================
    # SEKSYEN KIRI (Header, About Us, Visit Hub, Call)
    # =====================================
    with col1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: -10px;">
                <h1 style="color: #E0F7FA; font-family: 'Arial Black', sans-serif; font-size: 42px; font-weight: 900; letter-spacing: 1px; margin: 0;">TIAP HARI KOPI</h1>
                <span style="font-size: 38px;">☕</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <h2 style="color: #F3E5D8; font-size: 26px; margin-top: 25px; margin-bottom: 10px;">About Us</h2>
            <p style="color: #E0E0E0; font-size: 15px; margin-bottom: 5px;">Every single cup carries raw passion, home comfort, and a little bit of daily happiness.</p>
            <p style="font-size: 16px; margin-top: 0;">🤎</p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <h2 style="color: #F3E5D8; font-size: 26px; margin-top: 25px; margin-bottom: 10px;">📍 Visit Our Hub</h2>
            <p style="color: #E0E0E0; font-size: 15px; line-height: 1.6;">
            Lot 2046, Kampung Gok Bata, Jalan Raja Perempuan Zainab II, <br>16150 Kota Bharu, Kelantan.
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <h2 style="color: #F3E5D8; font-size: 26px; margin-top: 10px; margin-bottom: 15px;">📞 Call Us</h2>
            <div style="display: flex; align-items: center; gap: 15px;">
                <a href="tel:+60134944337" style="text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/3616/3616215.png" width="48" style="border-radius: 50%;">
                </a>
                <a href="tel:+60134944337" style="font-size: 28px; text-decoration: none; color: #E5A967; font-weight: bold; font-family: sans-serif;">
                    013-4944337
                </a>
                <a href="https://wa.me/60134944337" target="_blank" style="text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="48">
                </a>
            </div>
        """, unsafe_allow_html=True)

    # =====================================
    # SEKSYEN KANAN (Connect With Us & Followers)
    # =====================================
    with col2:
        st.markdown("""
            <h2 style="color: #F3E5D8; font-size: 26px; margin-bottom: 15px;">🔗 Connect With Us</h2>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="display: flex; gap: 15px; margin-bottom: 25px;">
                <a href="https://www.facebook.com/tiapharikopimy/?locale=ms_MY" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="45">
                </a>
                <a href="https://www.instagram.com/TiapHariKopi" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="45">
                </a>
                <a href="https://www.tiktok.com/@TiapHariKopi" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/3046/3046121.png" width="45">
                </a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="font-size: 16px; font-family: sans-serif; color: #E0E0E0; display: flex; flex-direction: column; gap: 15px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="24">
                    <span><b>Facebook : {live_counts['facebook']} Followers</b></span>
                </div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="24">
                    <span><b>Instagram : {live_counts['instagram']} Followers</b></span>
                </div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/3046/3046121.png" width="24">
                    <span><b>TikTok : {live_counts['tiktok']} Followers</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # =====================================
    # BAHAGIAN BAWAH (Opening Hours & Copyright)
    # =====================================
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top: 10px; margin-bottom: 20px;">
            <h2 style="color: #F3E5D8; font-size: 28px; display: flex; align-items: center; gap: 10px;">
                🕒 Opening Hours
            </h2>
            <ul style="color: #E0E0E0; font-size: 16px; list-style-type: disc; padding-left: 20px; line-height: 1.8;">
                <li>Open Daily : 3PM - 11PM</li>
                <li>Kitchen Last Order : 10PM</li>
                <li>Closed on Wednesday</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

elif selected_route == "LOG IN":
    import app as backend
    import importlib
    importlib.reload(backend)
    
    # 1. Cipta Header Utama Portal
    st.markdown("<h2 style='color: white; text-align: center;'>🔒 Internal Portal & Analytics</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # 2. Semakan Status Login: Jika BELUM Login, paparkan sub-menu Login Portal
    if not st.session_state.get('logged_in', False):
        st.markdown("<h3 style='color: #00bbff;'>🔑 Staff Login Portal</h3>", unsafe_allow_html=True)
        # Memanggil borang login daripada app.py
        backend.auth_page()
        
    # 3. Jika SUDAH Berjaya Login, paparkan sub-menu Dashboard Analytics
    else:
        st.markdown("<h3 style='color: #00ff88;'>📊 Business Analytics Dashboard</h3>", unsafe_allow_html=True)
        
        # Butang Log Out disediakan di atas dashboard untuk kemudahan staff
        # if st.button("🚪 Log Out dari Portal"):
        #    st.session_state['logged_in'] = False
        #    st.rerun()
            
        # Memanggil paparan dashboard utama daripada app.py
        backend.admin_workspace()
        
# 3. INTERACTIVE NATIVE HTML/CSS FLOATING "GO TO TOP" BUTTON (ACCESSIBLE EVERYWHERE)
st.markdown("""
<div class="scroll-wrapper-global">
    <a href="#top-anchor" target="_self" class="scroll-top-link">
        <span class="arrow-icon">▲</span>
        <span class="btn-text">GO TO TOP</span>
    </a>
</div>
""", unsafe_allow_html=True)

# Garisan pemisah halus sebelum hak cipta
st.markdown("<br><hr style='border-top: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# --- FOOTER NAVIGATION LINKS (Placed right on top of the footer columns) ---
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 5px; margin-bottom: 30px; font-family: sans-serif; font-size: 14px; letter-spacing: 0.5px;">
        <a class="{get_active_class('HOME')}" href="?page=HOME" target="_self" style="text-decoration: none; font-weight: bold;">HOME</a> 
        <span style="color: #444444;">&nbsp;&nbsp;&bull;&nbsp;&nbsp;</span> 
        <a class="{get_active_class('MENU')}" href="?page=MENU" target="_self" style="text-decoration: none; font-weight: bold;">MENU</a> 
        <span style="color: #444444;">&nbsp;&nbsp;&bull;&nbsp;&nbsp;</span> 
        <a class="{get_active_class('RESERVATIONS')}" href="?page=RESERVATIONS" target="_self" style="text-decoration: none; font-weight: bold;">RESERVATIONS</a> 
        <span style="color: #444444;">&nbsp;&nbsp;&bull;&nbsp;&nbsp;</span> 
        <a class="{get_active_class('FEEDBACK')}" href="?page=FEEDBACK" target="_self" style="text-decoration: none; font-weight: bold;">FEEDBACK</a> 
        <span style="color: #444444;">&nbsp;&nbsp;&bull;&nbsp;&nbsp;</span> 
        <a class="{get_active_class('ABOUT US')}" href="?page=ABOUT US" target="_self" style="text-decoration: none; font-weight: bold;">ABOUT US</a> 
        <span style="color: #444444;">&nbsp;&nbsp;&bull;&nbsp;&nbsp;</span> 
        <a class="{get_active_class('LOG IN')}" href="?page=LOG IN" target="_self" style="text-decoration: none; font-weight: bold;">LOG IN</a>
    </div>
""", unsafe_allow_html=True)

# Hak Cipta & Inspirasi Template
st.markdown("""
    <div style="text-align: center; font-size: 14px; padding-top: 15px; padding-bottom: 20px; color: rgba(255,255,255,0.5); line-height: 1.6; font-family: sans-serif;">
        © 2026 Tiap Hari Kopi Enterprise.<br>
        All Rights Reserved.<br><br>
        Inspired by Nasken Website Template
    </div>
""", unsafe_allow_html=True)
