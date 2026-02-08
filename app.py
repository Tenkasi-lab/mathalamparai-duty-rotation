import streamlit as st
import pandas as pd
import random
from datetime import datetime
import urllib.parse

# Google Sheet Settings
sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
sheet_name = "FEBRUARY-2026" 
encoded_sheet_name = urllib.parse.quote(sheet_name)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]

# 13 Duty Points (Wellness sethu)
duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", 
    "12. NEW CANTEEN", "13. WELLNESS CENTRE"
]

def generate_shift_rotation(active_staff, is_weekend):
    if not active_staff: return [], []
    
    random.shuffle(active_staff)
    
    # Reception Logic (Weekend 1, Weekday 2)
    needed_reception = 1 if is_weekend else 2
    reception_pool = [s for s in active_staff if any(r in s['name'] for r in receptionists_pool)]
    
    selected_reception = random.sample(reception_pool, min(needed_reception, len(reception_pool)))
    remaining_staff = [s for s in active_staff if s not in selected_reception]
    
    # Final Rotation
    rotation = []
    random.shuffle(remaining_staff)

    for i, point in enumerate(duty_points):
        name = remaining_staff[i]['name'] if i < len(remaining_staff) else "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": name})
        
    return rotation, [s['name'] for s in selected_reception]

# --- UI Setup ---
st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")
st.title("🛡️ Mathalamparai Daily Duty Rotation")

selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_str = str(selected_date.day)
is_weekend = selected_date.weekday() >= 5 

if st.button(f'Generate Rotation for {selected_date.strftime("%d-%b-%Y")}'):
    try:
        df_raw = pd.read_csv(url, header=None)
        date_col_idx = None
        
        for r in range(min(10, len(df_raw))):
            for c in range(len(df_raw.columns)):
                if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]:
                    date_col_idx = c
                    break
            if date_col_idx is not None: break

        if date_col_idx is not None:
            shift_data = {"A": [], "B": [], "C": []}
            
            # SCANNING Row 1 to 59 (index 0 to 58)
            for i in range(0, 59):
                if i < len(df_raw):
                    name_cell = str(df_raw.iloc[i, 1]).strip().upper()
                    status_cell = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                    
                    if name_cell and name_cell not in ["NAME", "STAFF NAME", "NAN", "MATHALAMPARA"]:
                        if status_cell in ["A", "B", "C"]:
                            shift_data[status_cell].append({'id': i, 'name': name_cell})

            for s in ["A", "B", "C"]:
                if not shift_data[s]: continue
                st.divider()
                st.header(f"📅 {s} SHIFT")
                rot, rec = generate_shift_rotation(shift_data[s], is_weekend)
                
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.subheader("🛎️ Reception")
                    for r in rec: st.info(r)
                with c2:
                    st.subheader("📍 Duty Points (13 Points)")
                    st.table(pd.DataFrame(rot))
        else:
            st.error("Date column not found!")
    except Exception as e:
        st.error(f"Error: {e}")
