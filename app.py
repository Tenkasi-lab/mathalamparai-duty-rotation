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
wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]

# 12 Regular Points (Wellness-ah thaniya handle pannuvom)
regular_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", 
    "12. NEW CANTEEN"
]

def generate_shift_rotation(staff_with_ids, is_weekend):
    if not staff_with_ids: return [], [], None
    
    # Shuffle all available staff
    random.shuffle(staff_with_ids)
    
    # 1. Wellness Duty Logic (Priority to specialists)
    wellness_person = None
    present_specialists = [s for s in staff_with_ids if any(sp in s['name'] for sp in wellness_specialists)]
    
    if present_specialists:
        wellness_person = present_specialists[0]
    else:
        # Specialists yarume illana, guards-la oruthara pick pannuvom
        potential_guards = [s for s in staff_with_ids if not any(r in s['name'] for r in receptionists_pool)]
        if potential_guards:
            wellness_person = random.choice(potential_guards)
            
    # Remove wellness person from current pool
    pool_after_wellness = [s for s in staff_with_ids if s != wellness_person]

    # 2. Reception Logic (Weekend 1, Weekday 2)
    needed_reception = 1 if is_weekend else 2
    reception_pool = [s for s in pool_after_wellness if any(r in s['name'] for r in receptionists_pool)]
    guard_pool_for_rec = [s for s in pool_after_wellness if s not in reception_pool]
    
    selected_reception = random.sample(reception_pool, min(needed_reception, len(reception_pool)))
    
    # If not enough receptionists, take from guards
    if len(selected_reception) < needed_reception:
        needed = needed_reception - len(selected_reception)
        if guard_pool_for_rec:
            extra = random.sample(guard_pool_for_rec, min(needed, len(guard_pool_for_rec)))
            selected_reception.extend(extra)
            
    # 3. Guard Duty (Remaining points)
    final_guards = [s for s in pool_after_wellness if s not in selected_reception]
    random.shuffle(final_guards)
    
    rotation = []
    for i, point in enumerate(regular_points):
        name = final_guards[i]['name'] if i < len(final_guards) else "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": name})
        
    return rotation, [s['name'] for s in selected_reception], wellness_person['name'] if wellness_person else "NOT ASSIGNED"

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
            for i in range(0, 60): 
                if i < len(df_raw):
                    name_cell = str(df_raw.iloc[i, 1]).strip().upper()
                    status_cell = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                    if name_cell and name_cell not in ["NAME", "STAFF NAME", "NAN"]:
                        if status_cell in ["A", "B", "C"]:
                            shift_data[status_cell].append({'id': i, 'name': name_cell})

            for s in ["A", "B", "C"]:
                if not shift_data[s]: continue
                st.divider()
                st.header(f"📅 {s} SHIFT")
                rot, rec, wellness = generate_shift_rotation(shift_data[s], is_weekend)
                
                c1, c2 = st.columns([1, 2, 1])
                with c1:
                    st.subheader("🛎️ Reception")
                    for r in rec: st.info(r)
                with c2:
                    st.subheader("📍 Regular Points")
                    st.table(pd.DataFrame(rot))
                with c3 if 'c3' in locals() else c1: # Simple layout fix
                    st.subheader("🏥 Wellness")
                    st.warning(wellness)
        else:
            st.error("Date not found!")
    except Exception as e:
        st.error(f"Error: {e}")
