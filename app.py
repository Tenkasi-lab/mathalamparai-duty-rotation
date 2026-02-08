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

def generate_shift_rotation(staff_list, is_weekend, is_tuesday):
    if not staff_list: return [], [], None
    
    staff_list = [name.strip().upper() for name in staff_list if str(name).strip()]
    
    # 1. Tuesday Wellness Logic
    tuesday_wellness_person = None
    if is_tuesday and len(staff_list) > 13: # Only if extra staff available
        tuesday_wellness_person = random.choice(staff_list)
        staff_list.remove(tuesday_wellness_person)

    # 2. Reception Logic
    current_receptionists = [name for name in staff_list if any(r in name for r in receptionists_pool)]
    current_guards = [name for name in staff_list if name not in current_receptionists]
    
    needed_reception = 1 if is_weekend else 2
    
    reception = []
    if current_receptionists:
        reception = random.sample(current_receptionists, min(needed_reception, len(current_receptionists)))
    
    if len(reception) < needed_reception:
        needed = needed_reception - len(reception)
        extra = random.sample(current_guards, min(needed, len(current_guards)))
        reception.extend(extra)

    # 3. Guard Duty (All remaining staff)
    remaining_staff = [s for s in staff_list if s not in reception]
    random.shuffle(remaining_staff)
    
    rotation = []
    for i, point in enumerate(duty_points):
        # Ippo kaila irukura ellaraiyum points-ku use pannuvom
        name = remaining_staff[i] if i < len(remaining_staff) else "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": name})
        
    return rotation, reception, tuesday_wellness_person

st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")
st.title("🛡️ Mathalamparai Duty Rotation System")

selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_str = str(selected_date.day)
is_weekend = selected_date.weekday() >= 5 
is_tuesday = selected_date.weekday() == 1 # Tuesday is index 1

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
            # Extended range to A52 to pick all names
            for i in range(4, 55): 
                if i < len(df_raw):
                    name = str(df_raw.iloc[i, 1]).strip().upper()
                    shift_val = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                    if shift_val in shift_data:
                        shift_data[shift_val].append(name)

            for s in ["A", "B", "C"]:
                st.divider()
                st.header(f"📅 {s} SHIFT")
                rot, rec, wellness = generate_shift_rotation(shift_data[s], is_weekend, is_tuesday)
                
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.subheader("🛎️ Reception")
                    for r in rec: st.info(r)
                    if wellness:
                        st.warning(f"🏥 Wellness: {wellness}")
                with c2:
                    st.subheader("📍 Duty Points")
                    st.table(pd.DataFrame(rot))
        else:
            st.error("Date column not found in Sheet!")
    except Exception as e:
        st.error(f"Error: {e}")
