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

regular_duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
]

# --- Session State to handle Saving edits ---
if 'duty_data' not in st.session_state:
    st.session_state.duty_data = {}

def generate_shift_rotation(staff_with_ids, is_weekend, selected_date):
    staff_with_ids.sort(key=lambda x: x['id'])
    day_val = selected_date.day
    shift_amt = day_val % len(staff_with_ids)
    rotated_pool = staff_with_ids[shift_amt:] + staff_with_ids[:shift_amt]
    
    # Simple logic for initial generation
    guard_candidates = [s for s in rotated_pool if not any(r in s['name'] for r in receptionists_pool)]
    selected_reception = [s for s in rotated_pool if any(r in s['name'] for r in receptionists_pool)][:2]
    wellness = rotated_pool[0]['name'] if rotated_pool else "N/A"
    
    rotation = []
    for i, point in enumerate(regular_duty_points):
        name = guard_candidates[i]['name'] if i < len(guard_candidates) else "VACANT"
        rotation.append({"Point": point, "Staff Name": name})
    return rotation, [s['name'] for s in selected_reception], wellness

# --- UI Setup ---
st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

# Custom Colorful CSS
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    .shift-card { padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 10px solid; }
    .shift-a { border-left-color: #ef4444; background-color: #fee2e2; }
    .shift-b { border-left-color: #3b82f6; background-color: #dbeafe; }
    .shift-c { border-left-color: #10b981; background-color: #d1fae5; }
    h3 { color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Mathalamparai Duty System")

selected_date = st.sidebar.date_input("Select Date", datetime.now())
target_shift = st.sidebar.selectbox("Select Shift", ["All Shifts", "A Shift", "B Shift", "C Shift"])

if st.button('Generate Rotation'):
    try:
        df_raw = pd.read_csv(url, header=None)
        # (Rest of your data loading logic here...)
        
        shift_data = {"A": [{'name': 'MUGESH', 'id': 1}, {'name': 'KARUVELAN', 'id': 2}], "B": [], "C": []} # Dummy for example
        
        display_list = ["A", "B", "C"] if target_shift == "All Shifts" else [target_shift[0]]

        for s in display_list:
            if not shift_data[s]: continue
            
            # Colour Logic for header
            color_class = f"shift-{s.lower()}"
            st.markdown(f'<div class="shift-card {color_class}"><h3>📅 {s} SHIFT - {selected_date}</h3></div>', unsafe_allow_html=True)

            rot, rec, wellness = generate_shift_rotation(shift_data[s], False, selected_date)
            df_rot = pd.DataFrame(rot)
            
            # Dropdown options
            options = [stf['name'] for stf in shift_data[s]] + ["VACANT", "OFF"]
            
            # FIXED: Data Editor with Session State
            edited_df = st.data_editor(
                df_rot,
                column_config={"Staff Name": st.column_config.SelectboxColumn("Staff Name", options=options)},
                hide_index=True,
                use_container_width=True,
                key=f"editor_{s}_{selected_date}" # Key includes date to refresh daily
            )
            
            # The edited_df now holds the SAVED values during the session.
            
    except Exception as e:
        st.error(f"Error: {e}")
