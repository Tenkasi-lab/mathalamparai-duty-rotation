import streamlit as st
import pandas as pd
import random
from datetime import datetime
import urllib.parse

# Google Sheet Details
sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
sheet_name = "FEBRUARY-2026" 

# Special encoding to fix the 'ascii' error with hyphen/spaces
encoded_sheet_name = urllib.parse.quote(sheet_name)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

# Receptionist names only
receptionists_pool = [
    "KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", 
    "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"
]

# Your 12 Duty Points
duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", 
    "4. CAR PARKING", "5. PATROLLING", "6. DG POWER ROOM", 
    "7. C BLOCK", "8. B BLOCK", "9. A BLOCK", 
    "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
]

def generate_rotation():
    try:
        # Read sheet with UTF-8 encoding
        df = pd.read_csv(url, encoding='utf-8')
        
        # Taking Column B (index 1) which has names, from row 5 to 49
        # pandas index-la Row 5 is index 3 or 4 depending on header
        all_staff = df.iloc[3:48, 1].dropna().tolist()
        all_staff = [str(name).strip().upper() for name in all_staff]
        
        # Remove Receptionists from Main Pool
        main_guard_pool = [name for name in all_staff if name not in receptionists_pool]
        
        # Pick 2 for Reception
        today_receptionists = random.sample(receptionists_pool, 2)
        
        # Shuffle Main Guards
        random.shuffle(main_guard_pool)
        
        # Tuesday Wellness Check
        today = datetime.now().strftime('%A')
        tuesday_person = None
        if today == "Tuesday" and len(main_guard_pool) > 0:
            tuesday_person = main_guard_pool.pop(0)

        # Assign 12 Points
        final_rotation = []
        for i, point in enumerate(duty_points):
            name = main_guard_pool[i] if i < len(main_guard_pool) else "OFF / BUFFER"
            final_rotation.append({"Point": point, "Staff Name": name})
            
        return final_rotation, today_receptionists, tuesday_person
    except Exception as e:
        return str(e), [], None

# --- UI ---
st.set_page_config(page_title="Mathalamparai Duty Chart", layout="wide")
st.title("🛡️ Mathalamparai Daily Duty Rotation")

if st.button('Generate New Random Rotation'):
    rotation, reception, tuesday_spl = generate_rotation()
    
    if isinstance(rotation, str):
        st.error(f"Error reading sheet: {rotation}")
        st.info("Tip: Make sure the Google Sheet is shared with 'Anyone with the link' as Viewer.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🛎️ Reception Duty")
            for i, r_name in enumerate(reception):
                st.info(f"Receptionist {i+1}: **{r_name}**")
        with col2:
            if tuesday_spl:
                st.warning(f"📅 Tuesday Special: **{tuesday_spl}** (Wellness Duty)")
            else:
                st.success(f"Today is {datetime.now().strftime('%A')} - Normal Routine")

        st.divider()
        st.subheader("📍 Main Guard Rotation")
        st.table(pd.DataFrame(rotation))
