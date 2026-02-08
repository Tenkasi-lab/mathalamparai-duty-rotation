import streamlit as st
import pandas as pd
import random
from datetime import datetime
import urllib.parse

# Google Sheet Details
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
    
    if len(current_receptionists) >= 2:
        reception = random.sample(current_receptionists, 2)
    else:
        needed = 2 - len(current_receptionists)
        reception = current_receptionists + (random.sample(current_guards, min(needed, len(current_guards))) if current_guards else [])
    
    remaining_guards = [g for g in current_guards if g not in reception]
    random.shuffle(remaining_guards)
    
    rotation = []
    for i, point in enumerate(duty_points):
        name = remaining_guards[i] if i < len(remaining_guards) else "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": name})
    return rotation, reception

# --- UI Setup ---
st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")
st.title("🛡️ Mathalamparai Daily Duty Rotation")

# Sidebar for Date Selection
st.sidebar.header("Settings")
selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_to_check = str(selected_date.day)

if st.button(f'Generate Rotation for {selected_date.strftime("%d-%b-%Y")}'):
    try:
        df = pd.read_csv(url)
        date_col = None
        for col in df.columns:
            if str(col).strip() == day_to_check:
                date_col = col
                break
        
        if date_col:
            shift_data = {"A": [], "B": [], "C": []}
            for index, row in df.iloc[3:48].iterrows():
                name = str(row.iloc[1]).strip().upper()
                shift_val = str(row[date_col]).strip().upper()
                if shift_val in shift_data:
                    shift_data[shift_val].append(name)
            
            for s_name in ["A", "B", "C"]:
                st.subheader(f"📅 {s_name} SHIFT")
                rot, rec = generate_shift_rotation(shift_data[s_name])
                if not rot and not rec:
                    st.write(f"No staff assigned for Shift {s_name}")
                else:
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        st.write("**Receptionists:**")
                        for r in rec: st.success(r)
                    with c2:
                        st.table(pd.DataFrame(rot))
                st.divider()
        else:
            st.error(f"Date {day_to_check} not found in Sheet columns!")
    except Exception as e:
        st.error(f"Error: {e}")
