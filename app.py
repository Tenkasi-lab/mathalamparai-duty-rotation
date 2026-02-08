import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# Google Sheet Settings
sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
sheet_name = "FEBRUARY-2026" 
encoded_sheet_name = urllib.parse.quote(sheet_name)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

# Configuration
receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]
supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]

# Neenga sonna athe Fixed Sequence
regular_duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
]

def generate_shift_rotation(staff_with_ids, is_weekend, selected_date):
    if not staff_with_ids: return [], [], "NOT ASSIGNED"
    
    # 1. Maintain Permanent Order
    staff_with_ids.sort(key=lambda x: x['id'])
    
    # 2. Date-based Sequential Rotation
    day_val = selected_date.day
    shift_amt = day_val % len(staff_with_ids)
    rotated_pool = staff_with_ids[shift_amt:] + staff_with_ids[:shift_amt]
    
    # 3. Specialist Logic
    wellness_person = None
    wellness_candidates = [s for s in rotated_pool if any(sp in s['name'] for sp in wellness_specialists)]
    if wellness_candidates:
        wellness_person = wellness_candidates[0]
    else:
        for s in rotated_pool:
            if not any(r in s['name'] for r in receptionists_pool):
                wellness_person = s
                break
    
    pool_after_wellness = [s for s in rotated_pool if s['id'] != (wellness_person['id'] if wellness_person else -1)]
    needed_reception = 1 if is_weekend else 2
    selected_reception = []
    guard_candidates = []
    
    for s in pool_after_wellness:
        if any(r in s['name'] for r in receptionists_pool) and len(selected_reception) < needed_reception:
            selected_reception.append(s)
        else:
            guard_candidates.append(s)
            
    # 4. Sequential Assignment to 1-12 Points
    point_assignments = {}
    staff_count = len(guard_candidates)
    
    essential_points = [p for p in regular_duty_points if p not in ["3. SECOND GATE", "9. A BLOCK"]]
    
    idx = 0
    for point in essential_points:
        if idx < staff_count:
            point_assignments[point] = guard_candidates[idx]['name']
            idx += 1
        else:
            point_assignments[point] = "OFF / BUFFER"

    # Vacant Priority Logic
    if idx < staff_count:
        point_assignments["9. A BLOCK"] = guard_candidates[idx]['name']; idx += 1
    else:
        point_assignments["9. A BLOCK"] = "VACANT"

    if idx < staff_count:
        point_assignments["3. SECOND GATE"] = guard_candidates[idx]['name']; idx += 1
    else:
        point_assignments["3. SECOND GATE"] = "VACANT"

    rotation = []
    for point in regular_duty_points:
        rotation.append({"Point": point, "Staff Name": point_assignments.get(point, "OFF / BUFFER")})
        
    return rotation, [s['name'] for s in selected_reception], (wellness_person['name'] if wellness_person else "NOT ASSIGNED")

# --- UI Setup ---
st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

# PDF Print Optimization
st.markdown("""
    <style>
    @media print {
        .stButton, .stSidebar, footer, header {display: none !important;}
        .main {margin: 0 !important; padding: 0 !important;}
        .stTable {font-size: 14px !important;}
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Mathalamparai Duty System")
st.caption("Tip: Press Ctrl + P to Save Chart as PDF")

selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_str = str(selected_date.day)
is_weekend = selected_date.weekday() >= 5 

if st.button(f'Generate Rotation for {selected_date.strftime("%d-%b-%Y")}'):
    try:
        df_raw = pd.read_csv(url, header=None)
        date_col_idx = None
        for r in range(min(15, len(df_raw))):
            for c in range(len(df_raw.columns)):
                if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]:
                    date_col_idx = c
                    break
            if date_col_idx is not None: break

        if date_col_idx is not None:
            shift_data = {"A": [], "B": [], "C": []}
            week_offs, on_leave, supervisors_present = [], [], []

            for i in range(0, 81): 
                if i < len(df_raw):
                    name_cell = str(df_raw.iloc[i, 1]).strip().upper()
                    status_cell = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                    
                    if name_cell and name_cell not in ["NAME", "STAFF NAME", "NAN", "MATHALAMPARA"]:
                        if status_cell == "WO" or status_cell == "W/O" or "OFF" in status_cell:
                            week_offs.append(name_cell)
                        elif status_cell == "L" or "LEAVE" in status_cell:
                            on_leave.append(name_cell)
                        elif any(sup in name_cell for sup in supervisors_pool):
                            if status_cell in ["A", "B", "C"]:
                                supervisors_present.append(f"{name_cell} ({status_cell})")
                        elif status_cell in ["A", "B", "C"]:
                            shift_data[status_cell].append({'id': i, 'name': name_cell})

            # Sidebar Summary
            st.sidebar.markdown("---")
            st.sidebar.subheader("📊 Summary")
            if week_offs: st.sidebar.info(f"🏖️ **Week Off ({len(week_offs)}):**\n" + "\n".join([f"- {n}" for n in week_offs]))
            if on_leave: st.sidebar.warning(f"🏥 **On Leave ({len(on_leave)}):**\n" + "\n".join([f"- {n}" for n in on_leave]))
            if supervisors_present: st.sidebar.success(f"👨‍💼 **Supervisors:**\n" + "\n".join([f"- {n}" for n in supervisors_present]))

            # Main Tables
            for s in ["A", "B", "C"]:
                if not shift_data[s]: continue
                st.divider()
                st.write(f"### 📅 {s} SHIFT - {selected_date.strftime('%d-%b-%Y')}")
                rot, rec, wellness = generate_shift_rotation(shift_data[s], is_weekend, selected_date)
                
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    st.write("**🛎️ Receptionist**")
                    for r in rec: st.info(r)
                with c2:
                    st.table(pd.DataFrame(rot)) # Simple table for better PDF view
                with c3:
                    st.write("**🏥 Wellness**")
                    st.warning(f"13. WELLNESS: {wellness}")
        else:
            st.error("Date column not found in Sheet!")
    except Exception as e:
        st.error(f"Error: {e}")
