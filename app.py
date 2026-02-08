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
duty_points = ["1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

def generate_shift_rotation(staff_list):
    if not staff_list: return [], []
    current_receptionists = [name for name in staff_list if name in receptionists_pool]
    current_guards = [name for name in staff_list if name not in receptionists_pool]
    
    # Randomly pick 2 receptionists
    if len(current_receptionists) >= 2:
        reception = random.sample(current_receptionists, 2)
    else:
        needed = 2 - len(current_receptionists)
        reception = current_receptionists + random.sample(current_guards, min(needed, len(current_guards))) if current_guards else []
    
    # Shuffle guards
    remaining_guards = [g for g in current_guards if g not in reception]
    random.shuffle(remaining_guards)
    
    rotation = []
    for i, point in enumerate(duty_points):
        name = remaining_guards[i] if i < len(remaining_guards) else "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": name})
    return rotation, reception

st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")
st.title("🛡️ Mathalamparai Daily Duty Rotation")

# Date Selection
selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_str = str(selected_date.day)

if st.button(f'Generate Rotation for Date: {day_str}'):
    try:
        # Load the entire sheet without headers first to find the date
        df_raw = pd.read_csv(url, header=None)
        
        date_col_idx = None
        # Scanning first 10 rows to find the date number
        for r in range(min(10, len(df_raw))):
            for c in range(len(df_raw.columns)):
                cell_val = str(df_raw.iloc[r, c]).strip()
                if cell_val == day_str or cell_val == day_str.zfill(2):
                    date_col_idx = c
                    break
            if date_col_idx is not None: break

        if date_col_idx is not None:
            shift_data = {"A": [], "B": [], "C": []}
            # Start scanning names from Row 5 (index 4)
            for i in range(4, 50):
                if i < len(df_raw):
                    name = str(df_raw.iloc[i, 1]).strip().upper() # Column B for Names
                    shift_val = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                    if shift_val in shift_data:
                        shift_data[shift_val].append(name)

            # Display tables for A, B, and C
            for s in ["A", "B", "C"]:
                st.divider()
                st.header(f"📅 {s} SHIFT")
                rot, rec = generate_shift_rotation(shift_data[s])
                
                if not rot and not rec:
                    st.warning(f"No staff marked as '{s}' for this date.")
                else:
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        st.subheader("🛎️ Reception")
                        for r in rec: st.info(r)
                    with c2:
                        st.subheader("📍 Duty Points")
                        st.table(pd.DataFrame(rot))
        else:
            st.error(f"Could not find Date '{day_str}' in your sheet. Please check if the date is entered as a number (1, 2, 3...) in the top rows.")
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")
