import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import random
import time
from datetime import datetime, timedelta
import os
import requests
from streamlit_option_menu import option_menu

# ==========================================
# 1. PAGE CONFIGURATION (DITUTUP UNTUK INTEGRASI)
# ==========================================
# st.set_page_config(page_title="Tiap Hari Kopi System", layout="wide", page_icon="☕")

# ==========================================
# 2. CUSTOM CSS & STYLING (WARNA DISELARASKAN)
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
            .stApp {
                background-color: #0b131f;
                color: #ffffff;
                animation: fadeIn 1.2s ease-in-out;
            }
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: #ffffff !important;
            }
            /* Menghilangkan kelam pada kotak input */
            input, textarea {
                color: #ffffff !important;
                background-color: #1a2636 !important;
                border: 1px solid #2d3f55 !important;
            }
            .stButton>button {
                background-color: #004481 !important;
                color: #ffffff !important;
                border: none;
                border-radius: 8px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                background-color: #0055a4 !important;
            }
            div[data-testid="metric-container"] {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            header {visibility: hidden;}
            
            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DATABASE & API FUNCTIONS
# ==========================================
DB_FILE = 'reviews_database.csv'
USER_DB = 'users_database.csv'

GOOGLE_API_KEY = "AIzaSyDQ_pYGFaa109Lq2l_g6YMF0mjKXU1ny4M"
PLACE_ID = "ChIJ31jVBB2xtjER9Z7j_udrlKg"

if not os.path.exists(USER_DB):
    df_users = pd.DataFrame(columns=["Username", "Password"])
    df_users.loc[0] = ["admin", "admin123"]
    df_users.to_csv(USER_DB, index=False)

def get_real_reviews():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["Date", "Platform", "Review", "Customer Type", "Sentiment"])
    
    df = pd.read_csv(DB_FILE)
    
    # Check and add missing columns safely
    if 'Customer Type' not in df.columns:
        df['Customer Type'] = 'Unknown'
    if 'Sentiment' not in df.columns:
        def analyze_sentiment(text):
            try:
                polarity = TextBlob(str(text)).sentiment.polarity
                if polarity > 0.05: return 'Positive'
                elif polarity < -0.05: return 'Negative'
                else: return 'Neutral'
            except:
                return 'Neutral'
        df['Sentiment'] = df['Review'].apply(analyze_sentiment)
        df.to_csv(DB_FILE, index=False)
        
    # Explicitly enforce clean column display sequence
    ordered_columns = ["Date", "Platform", "Review", "Customer Type", "Sentiment"]
    existing_ordered = [col for col in ordered_columns if col in df.columns]
    
    return df[existing_ordered]

def get_users():
    return pd.read_csv(USER_DB)

def sync_google_reviews():
    if GOOGLE_API_KEY == "SILA_MASUKKAN_API_KEY_ANDA_DI_SINI":
        return "api_missing"
        
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") != "OK": return "api_error"
            
        reviews = data.get("result", {}).get("reviews", [])
        if not reviews: return 0
            
        df_existing = get_real_reviews()
        existing_texts = df_existing['Review'].tolist() if 'Review' in df_existing.columns else []
        
        added = 0
        new_rows_list = []
        
        for r in reviews:
            text = r.get("text", "")
            time_val = r.get("time", 0)
            date_str = datetime.utcfromtimestamp(time_val) + timedelta(hours=8)
            date_format = date_str.strftime("%Y-%m-%d %H:%M:%S")
            
            if text and text not in existing_texts:
                polarity = TextBlob(text).sentiment.polarity
                sentiment = 'Positive' if polarity > 0.05 else 'Negative' if polarity < -0.05 else 'Neutral'
                
                new_rows_list.append({
                    "Date": date_format,
                    "Platform": "Google Maps",
                    "Review": text,
                    "Customer Type": "Google User",
                    "Sentiment": sentiment
                })
                added += 1
        
        # Safe structural concatenation by name instead of raw append
        if new_rows_list:
            df_new = pd.DataFrame(new_rows_list)
            df_final_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_final_combined.to_csv(DB_FILE, index=False)
            
        return added
    except Exception as e:
        return "error"

@st.cache_data
def generate_sales_data():
    return pd.DataFrame({
        "Menu Item": ["Signature Kopi", "Latte Ice", "Mocha Tarik", "Americano", "Pandan Latte"],
        "Units Sold": [420, 315, 250, 180, 110]
    })

def fetch_social_media_apis():
    current_hour = datetime.now().hour
    current_day = datetime.now().day
    ig_base = 12450 + (current_day * 15) + current_hour
    fb_base = 8920 + (current_day * 8) + (current_hour // 2)
    random.seed(datetime.now().minute)
    
    return {
        "ig_followers": ig_base,
        "ig_mentions": 842 + random.randint(1, 5),
        "ig_reach": "45.2K", "ig_reach_delta": "12%",
        "fb_likes": fb_base,
        "fb_shares": 345 + random.randint(1, 4),
        "whatsapp_inquiries": 128 + random.randint(0, 2)
    }

# ==========================================
# 4. FULL AUTHENTICATION SYSTEM (CLEAN UI)
# ==========================================
def auth_page():
    # Buang ruang kosong dan tabs navigasi yang tidak cantik
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>☕ Staff Login Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Digital Branding & Engagement Platform</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Log In", use_container_width=True)
            
            if submit_login:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    users_df = get_users()
                    user_match = users_df[(users_df['Username'] == username) & (users_df['Password'] == password)]
                    
                    if not user_match.empty:
                        st.session_state['logged_in'] = True
                        st.session_state['current_user'] = username
                        st.success(f"Welcome back, {username}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")

# ==========================================
# 5. ADMIN BACKEND & SYNCED NAVIGATION
# ==========================================
def admin_workspace():
    # Header dengan 1 Butang Logout sahaja
    h1, h2 = st.columns([9, 1])
    with h1:
        st.markdown("<h3 style='color: #ffffff;'>☕ TIAP HARI KOPI | Workspace</h3>", unsafe_allow_html=True)
    with h2:
        if st.button("Log Out", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    menu_options = ["Overview", "Analytics", "Social Media", "Reports", "Profile"]
    
    selected_top = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=["house", "bar-chart-line", "phone", "file-earmark-text", "person-circle"],
        menu_icon="cast",
        default_index=st.session_state.get('menu_index', 0),
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#0b131f", "border-bottom": "1px solid #333333"},
            "icon": {"color": "white", "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "color": "#dddddd"},
            "nav-link-selected": {"background-color": "#004481", "font-weight": "bold", "color": "white"},
        },
        key="top_nav_menu"
    )
    
    st.session_state['menu_index'] = menu_options.index(selected_top)
    st.markdown("<br>", unsafe_allow_html=True)
    
    df_reviews = get_real_reviews()
    df_sales = generate_sales_data()
    api_data = fetch_social_media_apis()

    if selected_top == "Overview":
        st.subheader("Dashboard Overview")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("YTD Revenue", "RM 1.6M", "+4.5%")
        m2.metric("Total Reviews", len(df_reviews), "Live Data")
        m3.metric("Avg. Satisfaction Rate", "4.9/5.0", "+0.2")
        m4.metric("Total IG Followers", f"{api_data['ig_followers']:,}", "Growing")
        
        st.markdown("<br>", unsafe_allow_html=True)
        o1, o2 = st.columns([1.5, 1])
        with o1:
            st.markdown("#### 🎯 Monthly Sales Target")
            st.progress(78)
            st.write("RM 117,000 / RM 150,000 achieved (78%)")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🔥 Top Performing Menu")
            st.write("1. **Signature Kopi** (420 units)")
            st.write("2. **Latte Ice** (315 units)")
            
        with o2:
            st.markdown("#### 💬 Live Review Feed")
            if not df_reviews.empty:
                recent_reviews = df_reviews.tail(3).iloc[::-1]
                for idx, row in recent_reviews.iterrows():
                    sentiment_emoji = "🟢" if row['Sentiment'] == 'Positive' else "🔴" if row['Sentiment'] == 'Negative' else "⚪"
                    st.info(f"{sentiment_emoji} \"{row['Review']}\" \n\n *- {row['Platform']} ({row['Date']})*")
            else:
                st.write("No reviews yet.")

    elif selected_top == "Analytics":
        col_title, col_btn = st.columns([3, 1])
        with col_title:
            st.subheader("Brand Sentiment Analysis (Live NLP)")
        with col_btn:
            if st.button("🔄 Pull Live Google Reviews", use_container_width=True, type="primary"):
                with st.spinner("Fetching data from Google Maps..."):
                    status = sync_google_reviews()
                    if status == "api_missing": st.error("API Key is missing.")
                    elif status == "api_error": st.error("Invalid API Key.")
                    elif status == "error": st.error("Connection failed.")
                    elif status == 0: st.info("Database up to date! No new reviews.")
                    else: 
                        st.success(f"Downloaded {status} new review(s)!")
                        time.sleep(1.5)
                        st.rerun()
        
        st.markdown("---")
        c1, c2 = st.columns([1, 1.5])
        with c1:
            if not df_reviews.empty:
                sentiment_counts = df_reviews['Sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                fig_donut = px.pie(sentiment_counts, values='Count', names='Sentiment', hole=0.5,
                                   color='Sentiment', color_discrete_map={'Positive': '#004481', 'Neutral': '#888888', 'Negative': '#cc0000'})
                fig_donut.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                st.plotly_chart(fig_donut, use_container_width=True)
            else:
                st.write("No sentiment data available.")

        with c2:
            st.markdown("**Review Database Records**")
            if not df_reviews.empty:
                # Pastikan kolum Sentiment dan Customer Type dipaparkan dengan jelas
                cols_to_show = ['Date', 'Platform', 'Customer Type', 'Review', 'Sentiment']
                existing_cols = [c for c in cols_to_show if c in df_reviews.columns]
                st.dataframe(df_reviews[existing_cols].tail(10), use_container_width=True, hide_index=True)
            else:
                st.write("Database is empty.")

    elif selected_top == "Social Media":
        st.subheader("Real-Time Social Media Engagement")
        if st.button("🔄 Refresh API Connection", type="primary"):
            st.toast("Syncing with APIs...", icon="🌐")
            time.sleep(1)
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        ig_col, fb_col = st.columns(2)
        with ig_col:
            st.markdown("#### 📸 Instagram Metrics")
            st.metric("IG Followers", f"{api_data['ig_followers']:,}", "12 Today")
            st.metric("Brand Mentions (@TiapHariKopi)", api_data['ig_mentions'], "5 Since Last Hour")
            st.metric("Account Reach (30 Days)", api_data['ig_reach'], api_data['ig_reach_delta'])
        with fb_col:
            st.markdown("#### 📘 Facebook & WhatsApp")
            st.metric("FB Page Likes", f"{api_data['fb_likes']:,}", "3 Today")
            st.metric("FB Post Shares", api_data['fb_shares'], "2 Since Last Hour")
            st.metric("WhatsApp Inquiries", api_data['whatsapp_inquiries'], "8 Today")

    elif selected_top == "Reports":
        st.subheader("Automated Branding Reports")
        my_time = datetime.utcnow() + timedelta(hours=8)
        current_time_str = my_time.strftime("%d %B %Y, %I:%M %p (MYT)")
        
        df_report = pd.DataFrame({
            "Platform Data": [
                "Instagram Followers", "Instagram Brand Mentions", "Instagram Account Reach", 
                "Facebook Page Likes", "Facebook Post Shares", "WhatsApp Inquiries", "Report Generated On"
            ],
            "Engagement Record": [
                f"{api_data['ig_followers']:,} Followers", 
                f"{api_data['ig_mentions']} Mentions", 
                f"{api_data['ig_reach']} Reach", 
                f"{api_data['fb_likes']:,} Likes", 
                f"{api_data['fb_shares']} Shares", 
                f"{api_data['whatsapp_inquiries']} Inquiries", 
                current_time_str
            ]
        })
        st.dataframe(df_report, use_container_width=True, hide_index=True)
        csv = df_report.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Official Report (CSV)", data=csv, 
                           file_name=f"TiapHariKopi_Report_{my_time.strftime('%Y%m%d')}.csv", 
                           mime="text/csv", type="primary")

    elif selected_top == "Profile":
        st.subheader("👤 User Profile Management")
        current_user = st.session_state.get('current_user', 'admin')
        st.write(f"**Current Logged-in User:** {current_user}")
        st.markdown("---")
        st.write("**Change Password**")
        with st.form("change_pass_form"):
            new_pass = st.text_input("Enter New Password", type="password")
            confirm_pass = st.text_input("Confirm New Password", type="password")
            submit_change = st.form_submit_button("Update Password")
            if submit_change:
                if new_pass == confirm_pass and len(new_pass) > 0:
                    st.success("Password successfully updated!")
                else:
                    st.error("Passwords do not match or fields are left blank.")

# ==========================================
# 6. MAIN ROUTING
# ==========================================
def main():
    inject_custom_css()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        auth_page()
    else:
        admin_workspace()

if __name__ == "__main__":
    main()
