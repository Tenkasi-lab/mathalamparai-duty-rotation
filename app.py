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

def generate_shift_rotation(staff_with_ids, is_weekend, selected_date):
    if not staff_with_ids: return [], [], "NOT ASSIGNED"
    staff_with_ids.sort(key=lambda x: x['id'])
    day_val = selected_date.day
    shift_amt = day_val % len(staff_with_ids)
    rotated_pool = staff_with_ids[shift_amt:] + staff_with_ids[:shift_amt]
    
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
            
    point_assignments = {}
    staff_count = len(guard_candidates)
    essential_points = [p for p in regular_duty_points if p not in ["3. SECOND GATE", "9. A BLOCK"]]
    
    idx = 0
    for point in essential_points:
        if idx < staff_count:
            point_assignments[point] = guard_candidates[idx]['name']
            idx += 1
        else: point_assignments[point] = "OFF / BUFFER"

    if idx < staff_count:
        point_assignments["9. A BLOCK"] = guard_candidates[idx]['name']; idx += 1
    else: point_assignments["9. A BLOCK"] = "VACANT"

    if idx < staff_count:
        point_assignments["3. SECOND GATE"] = guard_candidates[idx]['name']; idx += 1
    else: point_assignments["3. SECOND GATE"] = "VACANT"

    rotation = []
    for point in regular_duty_points:
        rotation.append({"Point": point, "Staff Name": point_assignments.get(point, "OFF / BUFFER")})
        
    return rotation, [s['name'] for s in selected_reception], (wellness_person['name'] if wellness_person else "NOT ASSIGNED")

# --- UI Setup ---
st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

# PRINT SCRIPT & PREMIUM CSS
st.markdown("""
    <style>
    .stApp { background: #f1f5f9; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; color: white; }
    .shift-header {
        padding: 20px; border-radius: 12px; margin: 25px 0px 15px 0px;
        color: white; font-weight: 800; text-align: center; font-size: 26px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .shift-a { background: linear-gradient(135deg, #dc2626, #f87171); }
    .shift-b { background: linear-gradient(135deg, #2563eb, #60a5fa); }
    .shift-c { background: linear-gradient(135deg, #059669, #34d399); }
    .info-card { background-color: white; padding: 18px; border-radius: 12px; border-top: 4px solid #4f46e5; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px; }
    
    @media print {
        .stButton, .stSidebar, footer, header, .no-print {display: none !important;}
        .main {margin: 0 !important; padding: 0 !important; background: white !important;}
        .stApp {background: white !important;}
        .stMarkdown {margin: 0 !important;}
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Mathalamparai Duty System")

# Sidebar Controls
selected_date = st.sidebar.date_input("Select Date", datetime.now())
day_str = str(selected_date.day)
is_weekend = selected_date.weekday() >= 5 
target_shift = st.sidebar.selectbox("Select Shift to View", ["All Shifts", "A Shift", "B Shift", "C Shift"])

# BUTTONS SECTION
col1, col2 = st.columns([1, 1])
with col1:
    gen_btn = st.button(f'🚀 Generate Rotation')
with col2:
    # UPDATED: More robust print button using Javascript
    st.components.v1.html("""
        <button style="background-color: #2563eb; color: white; padding: 12px 24px; border-radius: 12px; border: none; font-weight: bold; cursor: pointer; font-family: sans-serif;" onclick="window.parent.print()">🖨️ Print to PDF</button>
    """, height=60)

if gen_btn:
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
            week_offs, on_leave, supervisors_on_duty = [], [], []

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
                                supervisors_on_duty.append(f"{name_cell} ({status_cell})")
                        elif status_cell in ["A", "B", "C"]:
                            shift_data[status_cell].append({'id': i, 'name': name_cell})

            # Sidebar Summary
            st.sidebar.markdown("---")
            st.sidebar.subheader("📊 Summary")
            if supervisors_on_duty: st.sidebar.success(f"👨‍💼 **Supervisors:**\n" + "\n".join([f"- {n}" for n in supervisors_on_duty]))
            if week_offs: st.sidebar.info(f"🏖️ **Week Off:**\n" + "\n".join([f"- {n}" for n in week_offs]))
            if on_leave: st.sidebar.warning(f"🏥 **On Leave:**\n" + "\n".join([f"- {n}" for n in on_leave]))

            display_list = ["A", "B", "C"] if target_shift == "All Shifts" else [target_shift[0]]

            for s in display_list:
                if not shift_data[s]: continue
                color_class = f"shift-{s.lower()}"
                st.markdown(f'<div class="shift-header {color_class}">📅 {s} SHIFT - {selected_date.strftime("%d-%b-%Y")}</div>', unsafe_allow_html=True)
                rot, rec, wellness = generate_shift_rotation(shift_data[s], is_weekend, selected_date)
                dropdown_options = sorted([stf['name'] for stf in shift_data[s]] + ["VACANT", "OFF / BUFFER"])

                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    st.markdown('<div class="info-card"><b>🛎️ Receptionist</b></div>', unsafe_allow_html=True)
                    for r in rec: st.info(r)
                with c2:
                    st.data_editor(
                        pd.DataFrame(rot),
                        column_config={"Staff Name": st.column_config.SelectboxColumn("Staff Name", options=dropdown_options, width="large", required=True)},
                        hide_index=True, use_container_width=True, key=f"editor_{s}"
                    )
                with c3:
                    st.markdown('<div class="info-card"><b>🏥 Wellness</b></div>', unsafe_allow_html=True)
                    st.warning(f"13. WELLNESS: {wellness}")
        else:
            st.error("Date column not found!")
    except Exception as e:
        st.error(f"Error: {e}")
