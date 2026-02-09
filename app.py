import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. DAILY DYNAMIC PASSWORD LOGIC ---
def check_password():
    def password_entered():
        # System date-ah edukkirom (Feb 13 => '1302')
        correct_password = datetime.now().strftime("%d%m") 
        
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center;'>🛡️ Mathalamparai Duty System</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Enter Daily PIN to Access</p>", unsafe_allow_html=True)
        st.text_input("Daily Password (DDMM)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='text-align: center;'>🛡️ Mathalamparai Duty System</h2>", unsafe_allow_html=True)
        st.text_input("Daily Password (DDMM)", type="password", on_change=password_entered, key="password")
        st.error("❌ Incorrect Password. (Hint: Use Today's Date DDMM)")
        return False
    else:
        return True

# --- 2. START THE APP IF PASSWORD IS CORRECT ---
if check_password():
    # Logout in Sidebar
    if st.sidebar.button("🔒 Logout System"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- REST OF YOUR CODE (Google Sheet, UI, Rotation logic) ---
    sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
    sheet_name = "FEBRUARY-2026" 
    encoded_sheet_name = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"
    
    # ... (Keep all your previous UI and rotation code here) ...
    st.title("🛡️ Mathalamparai Duty System")
    st.write(f"Logged in successfully on {datetime.now().strftime('%d-%b-%Y')}")
    
    # [Rest of your code goes here...]
