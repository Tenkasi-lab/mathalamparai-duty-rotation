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
supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
regular_duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
]

# --- Session State to store edits ---
if 'edited_data' not in st.session_state:
    st.session_state.edited_data = {}

def generate_shift_rotation(staff_list, selected_date):
    if not staff_list:
        return [{"Point": p, "Staff Name": "VACANT"} for p in regular_duty_points]
    
    # Sequential Rotation Logic
    staff_list.sort(key=lambda x: x['id'])
    day_val = selected_date.day
    shift_amt = day_val % len(staff_list)
    rotated_pool = staff_list[shift_amt:] + staff_list[shift_amt:]
    
    rotation = []
    for i, point in enumerate(regular_duty_points):
        name = rotated_pool[i]['name'] if i < len(rotated_pool) else "VACANT"
        rotation.append({"Point": point, "Staff Name": name})
    return rotation

# --- UI Setup ---
st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

# Custom CSS for Colors
st.markdown("""
    <style>
    .shift-header { padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #1e293b; font-weight: bold; }
    .shift-a { background-color: #fee2e2; border-left: 8px solid #ef4444; }
    .shift-b { background-color: #dbeafe; border-left: 8px solid #3b82f6; }
    .shift-c { background-color: #d1fae5; border-left: 8px solid #10b981; }
    [data-testid="stSidebar"] { background-color: #0f172a; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Mathalamparai Duty System")

# Sidebar
selected_date = st.sidebar.date_input("Select Date", datetime.now())
target_shift = st.sidebar.selectbox("Select Shift", ["All Shifts", "A Shift", "B Shift", "C Shift"])

if st.button('Generate Rotation'):
    try:
        df_raw = pd.read_csv(url, header=None)
        day_str = str(selected_date.day)
        
        # Find Date Column
        date_col_idx = None
        for r in range(min(15, len(df_raw))):
            for c in range(len(df_raw.columns)):
                if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]:
                    date_col_idx = c
                    break
            if date_col_idx is not None: break

        if date_col_idx is not None:
            shift_data = {"A": [], "B": [], "C": []}
            supervisors_on_duty = []

            # Row 0 to 80 scanner
            for i in range(len(df_raw)):
                if i > 80: break 
                name = str(df_raw.iloc[i, 1]).strip().upper()
                status = str(df_raw.iloc[i, date_col_idx]).strip().upper()
                
                if name and name not in ["NAME", "NAN"]:
                    if any(sup in name for sup in supervisors_pool):
                        if status in ["A", "B", "C"]: supervisors_on_duty.append(f"{name} ({status})")
                    elif status in ["A", "B", "C"]:
                        shift_data[status].append({'id': i, 'name': name})

            # Sidebar Summary
            if supervisors_on_duty:
                st.sidebar.success("**Supervisors:**\n" + "\n".join(supervisors_on_duty))

            # Display logic
            shifts_to_show = ["A", "B", "C"] if target_shift == "All Shifts" else [target_shift[0]]

            for s in shifts_to_show:
                st.markdown(f'<div class="shift-header shift-{s.lower()}">📅 {s} SHIFT - {selected_date}</div>', unsafe_allow_html=True)
                
                initial_rot = generate_shift_rotation(shift_data[s], selected_date)
                df_rot = pd.DataFrame(initial_rot)
                
                # Dropdown options for editing
                available_names = [stf['name'] for stf in shift_data[s]] + ["VACANT", "OFF"]
                
                # Permanent Edit Save using Session State key
                st.data_editor(
                    df_rot,
                    column_config={"Staff Name": st.column_config.SelectboxColumn("Staff Name", options=available_names)},
                    hide_index=True,
                    use_container_width=True,
                    key=f"edit_{s}_{selected_date}" 
                )
        else:
            st.error(f"Sheet-la {day_str}-am thaethi column-ah kandupudikka mudiyala. Check your Sheet!")
            
    except Exception as e:
        st.error(f"Error: {e}")
