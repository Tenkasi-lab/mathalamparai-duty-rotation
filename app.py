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

# Permanent Pools
receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]

# Regular Duty Points Order
regular_duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
]

def generate_shift_rotation(staff_with_ids, is_weekend):
    if not staff_with_ids: return [], [], "NOT ASSIGNED"
    
    random.shuffle(staff_with_ids)
    
    # 1. Wellness Duty Logic
    wellness_person = None
    present_specialists = [s for s in staff_with_ids if any(sp in s['name'] for sp in wellness_specialists)]
    
    if present_specialists:
        wellness_person = present_specialists[0]
    else:
        # If no specialist, pick any guard (not from receptionist pool)
        potential_guards = [s for s in staff_with_ids if not any(r in s['name'] for r in receptionists_pool)]
        if potential_guards:
            wellness_person = random.choice(potential_guards)
            
    # Pool after taking wellness person
    pool_after_wellness = [s for s in staff_with_ids if s['id'] != (wellness_person['id'] if wellness_person else -1)]

    # 2. Reception Logic (Weekend 1, Weekday 2)
    needed_reception = 1 if is_weekend else 2
    reception_pool = [s for s in pool_after_wellness if any(r in s['name'] for r in receptionists_pool)]
    
    selected_reception = random.sample(reception_pool, min(needed_reception, len(reception_pool)))
    
    # Pool after taking receptionists
    final_guard_pool = [s for s in pool_after_wellness if s not in selected_reception]
    random.shuffle(final_guard_pool)

    # 3. Sequential Vacant Logic
    staff_count = len(final_guard_pool)
    point_assignments = {}
    
    # Essential points that MUST be filled first
    essential_points = [p for p in regular_duty_points if p not in ["3. SECOND GATE", "9. A BLOCK"]]
    
    idx = 0
    # Assign staff to essential points
    for point in essential_points:
        if idx < staff_count:
            point_assignments[point] = final_guard_pool[idx]['name']
            idx += 1
        else:
            point_assignments[point] = "OFF / BUFFER"

    # Assign staff to A BLOCK (Priority 2 to leave vacant)
    if idx < staff_count:
        point_assignments["9. A BLOCK"] = final_guard_pool[idx]['name']
        idx += 1
    else:
        point_assignments["9. A BLOCK"] = "VACANT"

    # Assign staff to SECOND GATE (Priority 1 to leave vacant)
    if idx < staff_count:
        point_assignments["3. SECOND GATE"] = final_guard_pool[idx]['name']
        idx += 1
    else:
        point_assignments["3. SECOND GATE"] = "VACANT"

    # Display Order
    rotation = []
    for point in regular_duty_points:
        rotation.append({"Point": point, "Staff Name": point_assignments.get(point, "OFF / BUFFER")})
        
    return rotation, [s['name'] for s in selected_reception], (wellness_person['name'] if wellness_person else "NOT ASSIGNED")

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
            # Scanner Range A1 to A59
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
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c1:
                    st.subheader("🛎️ Reception")
                    for r in rec: st.info(r)
                with c2:
                    st.subheader("📍 Regular Duty")
                    st.table(pd.DataFrame(rot))
                with c3:
                    st.subheader("🏥 Wellness")
                    st.warning(f"13. WELLNESS: {wellness}")
        else:
            st.error("Date column not found!")
    except Exception as e:
        st.error(f"Error: {e}")
