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

# 13 Duty Points
duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", 
    "12. NEW CANTEEN", "13. WELLNESS CENTRE"
]

def generate_shift_rotation(staff_with_ids, is_weekend):
    if not staff_with_ids: return [], []
    
    # 1. Filter out Week Off (W/O)
    active_staff = [s for s in staff_with_ids if s['status'] not in ["W/O", "OFF"]]
    random.shuffle(active_staff)
    
    # 2. Reception Logic (Weekend 1, Weekday 2)
    needed_reception = 1 if is_weekend else 2
    reception_pool = [s for s in active_staff if any(r in s['name'] for r in receptionists_pool)]
    
    selected_reception = random.sample(reception_pool, min(needed_reception, len(reception_pool)))
    remaining_after_reception = [s for s in active_staff if s not in selected_reception]

    # 3. Wellness Duty Logic (Point 13)
    # Specialist irundha avangala priority-la wellness-ku assign pannuvom
    present_specialists = [s for s in remaining_after_reception if any(sp in s['name'] for sp in wellness_specialists)]
    
    assigned_wellness = None
    if present_specialists:
        assigned_wellness = present_specialists[0]
    elif remaining_after_reception:
        # Specialist illena guards-la irundhu oruthara pick pannuvom
        assigned_wellness = random.choice(remaining_after_reception)
    
    # 4. Final Duty Assignment
    rotation = []
    # Wellness-ku ponavarai thavira mathavangala shuffle pannuvom
    guard_pool = [s for s in remaining_after_reception if s != assigned_wellness]
    random.shuffle(guard_pool)

    for i, point in enumerate(duty_points):
        if "WELLNESS" in point:
            name = assigned_wellness['name'] if assigned_wellness else "OFF / BUFFER"
        elif i < len(guard_pool):
            name = guard_pool[i]['name']
        else:
            name = "OFF / BUFFER"
        rotation.append({"Point": point, "Staff Name": name})
        
    return rotation, [s['name'] for s in selected_reception]

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
            # Scanner from A5 to A70
            for i in range(4, 75): 
                if i < len(df_raw):
                    name = str(df_raw.iloc[i, 1]).strip().upper()
                    status_val = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                    
                    if status_val in ["A", "B", "C", "W/O"]:
                        # status W/O-ah irundhaalum record-ah fetch panni 'W/O' nu mark panrom
                        target_shift = status_val if status_val != "W/O" else "A" # Defaulting W/O to a shift for data handling
                        shift_data[target_shift].append({
                            'id': i, 'name': name, 'status': status_val
                        })

            for s in ["A", "B", "C"]:
                if not shift_data[s]: continue
                st.divider()
                st.header(f"📅 {s} SHIFT")
                rot, rec = generate_shift_rotation(shift_data[s], is_weekend)
                
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.subheader("🛎️ Reception")
                    if rec:
                        for r in rec: st.info(r)
                    else:
                        st.write("No staff for Reception")
                with c2:
                    st.subheader("📍 Duty Points (13 Points)")
                    st.table(pd.DataFrame(rot))
        else:
            st.error("Date column not found!")
    except Exception as e:
        st.error(f"Error: {e}")
