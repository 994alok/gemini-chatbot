import streamlit as st
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyCIXuzDiGIAMC1SrHbFtRMSfJHtd8F2k9E')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Google Sheets setup
@st.cache_resource
def get_worksheet():
    # Try to get from environment variable first
    service_account_json = os.getenv('SERVICE_ACCOUNT_JSON')
    
    if service_account_json:
        service_account_info = json.loads(service_account_json)
    else:
        # Fallback to hardcoded for development
        service_account_info = {
            "type": "service_account",
            "project_id": "gen-lang-client-0819640616",
            "private_key_id": "8e39f4413d6834f2568b4c181a7aed47a5a8588b",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0mf8klI4SMsoz\nCo0HWIFIuUy7ivHM6uSZf/F+Xc99gKMtyMgLcx7wnHRAAWyiq62WiRBLsMrI3P6o\nCWu+1xQRQFt9VUBOSnVG+YBCeMQ/2KWAm7g26xycvc+zkHpICicn5W+tzu1Lp6jx\nKuvChcGJ7UjNlZE3Yij3mjPzK5SJjC0CglXKN5SubEWOjnoFTPNsS0eQJ7PSh+lC\n1dLEMtpegk+JaSExqsbwTKO5o3PGNnndjdrdcWA1vyuMe2W15KOi9VHUeEybC3fM\nDycgQ2BrJCHrxjjD5IBDL7tYn5x8lTEkiQeg8rcqTTYYO4jHB7v4XbJTm+Yi99Hk\nrp6qbaP/AgMBAAECggEAUzoSd8+T5zQLtVjb4/I35gUqpNSjmKz4uvpYlkTx/SKe\nUFeSRKCBNh3LfsGJSC+4d8JjRZZL5SPeoR5yTkh8gXS4lLoIP+wVPqd1IWzY95lF\nr85TJs/TaDIauOPQTkmLgNm9TQoqla5Gbxk5+3M7XO4CGmeeO7kbKvufjCTdt0Kf\nBieLdxXEKXd0TOpFHD//HNOrAPFuya6TV1Eym0O4sEdH507NdmZQxUkveWWnw7ok\nMN2Itk/xum5cuIlYZZ7p5CkWbIXPTVmzyuyQM33/rSU6kjDnPOdDOzKMTDCo9xwY\ngm7eDyWNwp7viR9vMqVnri1wc+aIaE4WzE3BpajBwQKBgQD5u7bUbnFnAAN8iT3A\nkoopB3zUkZVmoAn3II9naB3cuxxqOzeyv5zs9laXAUaaBZGpmXPVo9oleEdjPHkS\nNfA2MDyqWQnmXPo6bCaKY+jQryh4P6dQVhlxlUN/oXQF0oX90+SAj7Cc5OE/e7DX\nTRJALfum0sMGe7/REnxqvx10vwKBgQC5Ii44b1cGeu5gEkIZITVjcfWdp7s3FegO\ntXARnbqbeRwKEAaCRjul5G5zVJ2VX9gXm4rS3R26d8HZFGgerNjwPzBwERatuPq2\nZk0Sz8EpoW+PC17JY9MvYJ/Gs3ZS2c5xqJ/g3K6wuc4nEhE7cjKp15aUn4cRzQtz\nS7exnc9gwQKBgQCnQthjU01UxSeQo4Lelcc/T6qF3LQJtiq2f/JMOem2SwPvCpZ1\ne+yosRyxqsMUqaIzy3lPn5yd9/8oMfqM/d9TC9+14EjHJ4LY2lK94ciu7IHYeBmh\nruj/sA8zTnmc5LGlneOvT43kp09N65Q3v4D3x1SDGSpSD1QbvZvjCvm5lQKBgBbf\nezhrwSPC0mq6NsJmEPONY9wrmfzPTxFqJ0N16lVFHEq9+h/kT4BKfb7wCFwpMEiS\nZg9xVDfyjdelJswLbO4Z0IE4C0ZBYXBhqUoWsvXSxTa2H+rf03q6BGOHTqoj0NbI\nD6C3gznAaxD2sXxXupyzTx5jq0tuuuhuxW5DYhjBAoGBAKuM7hxIVTTcXCP7Uy4z\nd/uhGvyWJQWumThOnECGHYRo/b5cfCcf+GSrgUtnZ8DvAyQrt9ynZaVS8/F+Q8LW\n3Tt0t2YPdK97O2YLB6ze1zpSEoo82BcxIGEXj2ozE6wjwUq3o3vLuK7OcOcrNQSE\n3+C8woc3SaqTRADNuLAea351\n-----END PRIVATE KEY-----\n",
            "client_email": "perm-688@gen-lang-client-0819640616.iam.gserviceaccount.com",
            "client_id": "118231592347705731276",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/perm-688%40gen-lang-client-0819640616.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
    
    creds = Credentials.from_service_account_info(
        service_account_info, 
        scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    
    return gspread.authorize(creds).open_by_key('1pH8iyT_3lOZKEE5Ts5SmZ9l5ECDEpaxhHQUoGjROKLI').worksheets()[0]

# User functions
def find_user_row(username):
    all_values = get_worksheet().get_all_values()
    for i, row in enumerate(all_values):
        if row and row[0] == username:
            return i + 1, row
    return None, None

def check_user_exists(username):
    return find_user_row(username)[0] is not None

def create_user(username, password):
    ws = get_worksheet()
    next_row = len(ws.get_all_values()) + 1
    ws.update(f'A{next_row}:C{next_row}', [[username, password, '[]']])

def verify_user(username, password):
    _, row = find_user_row(username)
    return row and len(row) >= 2 and row[1] == password

def get_user_chat_history(username):
    _, row = find_user_row(username)
    if row and len(row) >= 3 and row[2]:
        try:
            return json.loads(row[2])
        except:
            pass
    return []

def save_user_chat_history(username, messages):
    row_num, _ = find_user_row(username)
    if row_num:
        get_worksheet().update(f'C{row_num}', [[json.dumps(messages)]])

# Initialize session state
for key, default in [("logged_in", False), ("username", None), ("messages", []), ("chat", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# Login/Signup Page
if not st.session_state.logged_in:
    st.title("🤖 Gemini Chatbot")
    st.divider()
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.subheader("Login to your account")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login") and login_username and login_password:
                if verify_user(login_username, login_password):
                    st.session_state.update({
                        "logged_in": True,
                        "username": login_username,
                        "messages": get_user_chat_history(login_username),
                        "chat": model.start_chat(history=[])
                    })
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    with tab2:
        st.subheader("Create a new account")
        with st.form("signup_form"):
            signup_username = st.text_input("Choose Username")
            signup_password = st.text_input("Choose Password", type="password")
            signup_confirm = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Sign Up") and all([signup_username, signup_password, signup_confirm]):
                if signup_password != signup_confirm:
                    st.error("❌ Passwords don't match!")
                elif check_user_exists(signup_username):
                    st.error("❌ Username already exists!")
                else:
                    create_user(signup_username, signup_password)
                    st.success("✅ Account created! Please login.")

# Chat Interface
else:
    with st.sidebar:
        st.write(f"👤 **{st.session_state.username}**")
        
        col1, col2 = st.columns(2)
        if col1.button("🚪 Logout", use_container_width=True):
            save_user_chat_history(st.session_state.username, st.session_state.messages)
            st.session_state.update({"logged_in": False, "username": None, "messages": [], "chat": None})
            st.rerun()
        
        if col2.button("🗑️ Clear", use_container_width=True):
            st.session_state.update({"messages": [], "chat": model.start_chat(history=[])})
            save_user_chat_history(st.session_state.username, [])
            st.rerun()
        
        st.divider()
        st.caption(f"Chat auto-saves\nMessages: {len(st.session_state.messages)}")
    
    st.title("🤖 Gemini Chatbot")
    st.caption(f"Welcome back, {st.session_state.username}!")
    
    if st.session_state.chat is None:
        st.session_state.chat = model.start_chat(history=[])
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    save_user_chat_history(st.session_state.username, st.session_state.messages)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
