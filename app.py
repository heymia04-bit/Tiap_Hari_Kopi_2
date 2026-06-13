import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import random
import time
from datetime import datetime, timedelta
import os
import requests # LIBRARY BARU UNTUK GOOGLE API
from streamlit_option_menu import option_menu

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Tiap Hari Kopi System", layout="wide", page_icon="☕")

# ==========================================
# 2. CUSTOM CSS & STYLING
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
            .stButton>button {
                background-color: #004481;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                background-color: #0055a4;
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
            
            /* SCROLL TO TOP BUTTON */
            .scroll-to-top {
                position: fixed;
                bottom: 40px;
                right: 40px;
                background-color: #004481;
                color: #ffffff !important;
                width: 45px;
                height: 45px;
                border-radius: 50%;
                text-align: center;
                line-height: 45px;
                font-size: 20px;
                font-weight: bold;
                cursor: pointer;
                text-decoration: none;
                z-index: 99999;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
                transition: transform 0.3s ease, background-color 0.3s ease;
            }
            .scroll-to-top:hover {
                transform: scale(1.15);
                background-color: #0055a4;
            }
            
            /* FOOTER COPYRIGHT STYLING */
            .footer-copyright {
                text-align: center;
                font-size: 12px;
                color: #666666;
                margin-top: 20px;
                margin-bottom: 30px;
            }
        </style>
        <div id="top"></div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DATABASE & API FUNCTIONS
# ==========================================
DB_FILE = 'reviews_database.csv'
USER_DB = 'users_database.csv'

# [PERHATIAN]: MASUKKAN API KEY ANDA DI SINI
GOOGLE_API_KEY = "AIzaSyDQ_pYGFaa109Lq2l_g6YMF0mjKXU1ny4M"
PLACE_ID = "ChIJ31jVBB2xtjER9Z7j_udrlKg"

if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=["Date", "Platform", "Review"])
    df_init.loc[0] = ["2026-06-01 10:00:00", "Web Portal", "The signature coffee is absolutely amazing!"]
    df_init.loc[1] = ["2026-06-02 14:30:00", "Web Portal", "Service was a bit slow today, but coffee is okay."]
    df_init.loc[2] = ["2026-06-03 09:15:00", "Web Portal", "Good environment and reasonable price."]
    df_init.to_csv(DB_FILE, index=False)

if not os.path.exists(USER_DB):
    df_users = pd.DataFrame(columns=["Username", "Password"])
    df_users.loc[0] = ["admin", "admin123"]
    df_users.to_csv(USER_DB, index=False)

def get_real_reviews():
    df = pd.read_csv(DB_FILE)
    def analyze_sentiment(text):
        try:
            polarity = TextBlob(str(text)).sentiment.polarity
            if polarity > 0.05: return 'Positive'
            elif polarity < -0.05: return 'Negative'
            else: return 'Neutral'
        except:
            return 'Neutral'
    df['Sentiment'] = df['Review'].apply(analyze_sentiment)
    return df

def get_users():
    return pd.read_csv(USER_DB)

def save_user(username, password):
    new_user = pd.DataFrame({"Username": [username], "Password": [password]})
    new_user.to_csv(USER_DB, mode='a', header=False, index=False)

def update_password(username, new_password):
    df = get_users()
    df.loc[df['Username'] == username, 'Password'] = new_password
    df.to_csv(USER_DB, index=False)

def sync_google_reviews():
    if GOOGLE_API_KEY == "SILA_MASUKKAN_API_KEY_ANDA_DI_SINI":
        return "api_missing"
        
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") != "OK":
            return "api_error"
            
        reviews = data.get("result", {}).get("reviews", [])
        if not reviews:
            return 0
            
        df = pd.read_csv(DB_FILE)
        existing_texts = df['Review'].tolist()
        
        added = 0
        for r in reviews:
            text = r.get("text", "")
            time_val = r.get("time", 0)
            date_str = datetime.utcfromtimestamp(time_val) + timedelta(hours=8)
            date_format = date_str.strftime("%Y-%m-%d %H:%M:%S")
            
            # Elak ulasan yang sama (Duplicate) masuk 2 kali
            if text and text not in existing_texts:
                new_row = pd.DataFrame({
                    "Date": [date_format],
                    "Platform": ["Google Maps"],
                    "Review": [text]
                })
                new_row.to_csv(DB_FILE, mode='a', header=False, index=False)
                added += 1
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
    # Gunakan 'seed' berdasarkan masa (jam) supaya data tidak melompat secara rawak
    # Ia akan nampak konsisten untuk jam tersebut, dan naik sedikit pada jam seterusnya.
    current_hour = datetime.now().hour
    current_day = datetime.now().day
    
    # Formula simulasi peningkatan berterusan (Real-growth simulator)
    ig_base = 12450 + (current_day * 15) + current_hour
    fb_base = 8920 + (current_day * 8) + (current_hour // 2)
    
    # Elemen interaktif yang berubah secara logik (Mentions & Inquiries)
    random.seed(datetime.now().minute) # Berubah setiap minit
    
    return {
        "ig_followers": ig_base,
        "ig_mentions": 842 + random.randint(1, 5),
        "ig_reach": "45.2K", "ig_reach_delta": "12%",
        "fb_likes": fb_base,
        "fb_shares": 345 + random.randint(1, 4),
        "whatsapp_inquiries": 128 + random.randint(0, 2)
    }

# ==========================================
# 4. FULL AUTHENTICATION SYSTEM
# ==========================================
def auth_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>☕ Tiap Hari Kopi</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Digital Branding & Engagement Platform</p>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔒 Log In", "📝 Sign Up", "🔑 Forgot Password"])
        
        with tab1:
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

        with tab2:
            with st.form("signup_form"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit_signup:
                    if not new_user or not new_pass or not confirm_pass:
                        st.warning("Please fill in all registration details.")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match. Please make sure they are identical.")
                    else:
                        users_df = get_users()
                        if new_user in users_df['Username'].values:
                            st.error("This username already exists. Please choose another one.")
                        else:
                            save_user(new_user, new_pass)
                            st.success("Account successfully created! Please log in at the Log In tab.")

        with tab3:
            with st.form("forgot_form"):
                recovery_user = st.text_input("Enter your registered Username")
                recovery_pass = st.text_input("Enter New Password", type="password")
                submit_forgot = st.form_submit_button("Reset Password", use_container_width=True)
                
                if submit_forgot:
                    if not recovery_user or not recovery_pass:
                        st.warning("Please enter your username and the new password.")
                    else:
                        users_df = get_users()
                        if recovery_user in users_df['Username'].values:
                            update_password(recovery_user, recovery_pass)
                            st.success("Password successfully reset! Please log in with your new password.")
                        else:
                            st.error("Account not found in our database.")

# ==========================================
# 5. ADMIN BACKEND & SYNCED NAVIGATION
# ==========================================
def admin_workspace():
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
        default_index=st.session_state['menu_index'],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#0b131f", "border-bottom": "1px solid #333333"},
            "icon": {"color": "white", "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "color": "#dddddd"},
            "nav-link-selected": {"background-color": "#004481", "font-weight": "bold", "color": "white"},
        },
        key="top_nav_menu"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    df_reviews = get_real_reviews()
    df_sales = generate_sales_data()
    api_data = fetch_social_media_apis()

    if selected_top == "Overview":
        st.subheader("Dashboard Overview")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("YTD Revenue", "RM 1.6M", "+4.5%")
        m2.metric("Total Reviews Collected", len(df_reviews), "Live Data")
        m3.metric("Avg. Satisfaction Rate", "4.9/5.0", "+0.2")
        m4.metric("Total IG Followers", f"{api_data['ig_followers']:,}", "Growing")
        
        st.markdown("<br>", unsafe_allow_html=True)
        o1, o2 = st.columns([1.5, 1])
        with o1:
            st.markdown("#### 🎯 Monthly Sales Target (June 2026)")
            st.progress(78)
            st.write("RM 117,000 / RM 150,000 achieved (78%)")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🔥 Top Performing Menu")
            st.write("1. **Signature Kopi** (420 units)")
            st.write("2. **Latte Ice** (315 units)")
            
        with o2:
            st.markdown("#### 💬 Live Review Feed")
            recent_reviews = df_reviews.tail(3).iloc[::-1]
            for idx, row in recent_reviews.iterrows():
                sentiment_emoji = "🟢" if row['Sentiment'] == 'Positive' else "🔴" if row['Sentiment'] == 'Negative' else "⚪"
                st.info(f"{sentiment_emoji} \"{row['Review']}\" \n\n *- {row['Platform']} ({row['Date']})*")

    elif selected_top == "Analytics":
        # BAHAGIAN BARU: BUTANG SYNC GOOGLE REVIEWS
        col_title, col_btn = st.columns([3, 1])
        with col_title:
            st.subheader("Brand Sentiment Analysis (Live NLP)")
        with col_btn:
            if st.button("🔄 Pull Live Google Reviews", use_container_width=True, type="primary"):
                with st.spinner("Fetching data from Google Maps..."):
                    status = sync_google_reviews()
                    if status == "api_missing":
                        st.error("Please insert your API Key in the code (Line 112).")
                    elif status == "api_error":
                        st.error("Invalid API Key or Places API is not enabled in Google Console.")
                    elif status == "error":
                        st.error("Failed to connect to Google Servers.")
                    elif status == 0:
                        st.info("Database is up to date! No new reviews found on Google.")
                    else:
                        st.success(f"Successfully downloaded {status} new review(s) from Google Maps!")
                        time.sleep(1.5)
                        st.rerun()
        
        st.markdown("---")
        
        c1, c2 = st.columns([1, 1.5])
        with c1:
            sentiment_counts = df_reviews['Sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']
            fig_donut = px.pie(sentiment_counts, values='Count', names='Sentiment', hole=0.5,
                               color='Sentiment', color_discrete_map={'Positive': '#004481', 'Neutral': '#888888', 'Negative': '#cc0000'})
            fig_donut.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig_donut, use_container_width=True)

        with c2:
            st.markdown("**Review Database Records**")
            st.dataframe(df_reviews[['Date', 'Platform', 'Review', 'Sentiment']].tail(10), use_container_width=True, hide_index=True)

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
                    update_password(current_user, new_pass)
                    st.success("Password successfully updated! Database has been synchronized.")
                else:
                    st.error("Passwords do not match or fields are left blank.")

    st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.1); margin-top: 80px;'>", unsafe_allow_html=True)
    
    selected_footer = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=["", "", "", "", ""], 
        default_index=menu_options.index(selected_top), 
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "border": "none"},
            "icon": {"display": "none"},
            "nav-link": {"font-size": "12px", "text-align": "center", "margin":"0px", "color": "#888888", "letter-spacing": "2px", "font-weight": "bold", "text-transform": "uppercase"},
            "nav-link-selected": {"background-color": "transparent", "color": "#ffffff"},
        },
        key="footer_nav_menu"
    )
    
    st.markdown("""
        <div class="footer-copyright">
            © 2026 Tiap Hari Kopi Enterprise.<br>All Rights Reserved.
        </div>
        <a href="#top" class="scroll-to-top" title="Go to top">↑</a>
    """, unsafe_allow_html=True)

    if selected_footer != selected_top:
        st.session_state['menu_index'] = menu_options.index(selected_footer)
        st.rerun() 
    elif selected_top != menu_options[st.session_state['menu_index']]:
        st.session_state['menu_index'] = menu_options.index(selected_top)

# ==========================================
# 6. MAIN ROUTING
# ==========================================
def main():
    inject_custom_css()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if 'menu_index' not in st.session_state:
        st.session_state['menu_index'] = 0

    if not st.session_state['logged_in']:
        auth_page()
    else:
        admin_workspace()

if __name__ == "__main__":
    main()