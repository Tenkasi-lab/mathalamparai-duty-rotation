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

def generate_shift_rotation(staff_with_ids, is_weekend, is_tuesday):
    if not staff_with_ids: return [], [], None
    
    # Shuffle all staff first
    random.shuffle(staff_with_ids)
    
    # 1. Tuesday Wellness Logic (Pick 1 from guards, not receptionists)
    wellness_person = None
    if is_tuesday:
        potential_wellness = [s for s in staff_with_ids if not any(r in s['name'] for r in receptionists_pool)]
        if potential_wellness:
            wellness_person = random.choice(potential_wellness)
            staff_with_ids = [s for s in staff_with_ids if s['id'] != wellness_person['id']]

    # 2. Reception Logic
    needed_reception = 1 if is_weekend else 2
    reception_pool = [s for s in staff_with_ids if any(r in s['name'] for r in receptionists_pool)]
    guard_pool = [s for s in staff_with_ids if s not in reception_pool]
    
    selected_reception = []
    if reception_pool:
        selected_reception = random.sample(reception_pool, min(needed_reception, len(reception_pool)))
    
    if len(selected_reception) < needed_reception:
        needed = needed_reception - len(selected_reception)
        if guard_pool:
            extra = random.sample(guard_pool, min(needed, len(guard_pool)))
            selected_reception.extend(extra)

    # 3. Final Duty Points (All remaining staff)
    final_pool = [s for s in staff_with_ids if s not in selected_reception]
    random.shuffle(final_pool)
    
    rotation = []
    for i, point in enumerate(duty_points):
        staff_name = final_pool[i]['name'] if i < len(final_pool) else "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": staff_name})
        
    return rotation, [s['name'] for s in selected_reception], wellness_person['name'] if wellness_person else None

st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")
st.title("🛡️ Mathalamparai Duty Rotation System")

selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_str = str(selected_date.day)
is_weekend = selected_date.weekday() >= 5 
is_tuesday = selected_date.weekday() == 1 

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
            for i in range(4, 55): # A5 to A55
                if i < len(df_raw):
                    name = str(df_raw.iloc[i, 1]).strip().upper()
                    shift_val = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                    if shift_val in shift_data:
                        # Storing name with index as unique ID
                        shift_data[shift_val].append({'id': i, 'name': name})

            for s in ["A", "B", "C"]:
                st.divider()
                st.header(f"📅 {s} SHIFT")
                rot, rec, wellness = generate_shift_rotation(shift_data[s], is_weekend, is_tuesday)
                
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.subheader("🛎️ Reception")
                    for r in rec: st.info(r)
                    if wellness: st.warning(f"🏥 Wellness Duty: {wellness}")
                with c2:
                    st.subheader("📍 Duty Points")
                    st.table(pd.DataFrame(rot))
        else:
            st.error("Date column not found!")
    except Exception as e:
        st.error(f"Error: {e}")
