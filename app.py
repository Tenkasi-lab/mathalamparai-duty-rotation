import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. FULL APP LOCK LOGIC (Daily Pin - No Hint) ---
def check_password():
    def password_entered():
        # Inniku date thaan password (e.g., Feb 09 => '0902')
        correct_pin = datetime.now().strftime("%d%m")
        if st.session_state["password"] == correct_pin:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center;'>🛡️ Mathalamparai Duty System</h2>", unsafe_allow_html=True)
        st.text_input("Enter Daily PIN to Access", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='text-align: center;'>🛡️ Mathalamparai Duty System</h2>", unsafe_allow_html=True)
        st.text_input("Enter Daily PIN to Access", type="password", on_change=password_entered, key="password")
        # HINT REMOVED: Just showing error now
        st.error("❌ Invalid PIN!") 
        return False
    else:
        return True

# --- 2. START THE APP ONLY IF LOGGED IN ---
if check_password():
    if st.sidebar.button("🔒 Logout System"):
        st.session_state["password_correct"] = False
        st.rerun()

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
        
        wellness_person = next((s for s in rotated_pool if any(sp in s['name'] for sp in wellness_specialists)), rotated_pool[0])
        pool_after_wellness = [s for s in rotated_pool if s['id'] != wellness_person['id']]
        
        needed_reception = 1 if is_weekend else 2
        selected_reception = [s['name'] for s in pool_after_wellness if any(r in s['name'] for r in receptionists_pool)][:needed_reception]
        guard_candidates = [s for s in pool_after_wellness if s['name'] not in selected_reception]
        
        point_assignments = {}
        staff_count = len(guard_candidates)
        essential_points = [p for p in regular_duty_points if p not in ["3. SECOND GATE", "9. A BLOCK"]]
        
        idx = 0
        for point in essential_points:
            point_assignments[point] = guard_candidates[idx]['name'] if idx < staff_count else "OFF / BUFFER"
            idx += 1
        point_assignments["9. A BLOCK"] = guard_candidates[idx]['name'] if idx < staff_count else "VACANT"; idx += 1
        point_assignments["3. SECOND GATE"] = guard_candidates[idx]['name'] if idx < staff_count else "VACANT"

        rotation = [{"Point": p, "Staff Name": point_assignments.get(p, "OFF")} for p in regular_duty_points]
        return rotation, selected_reception, wellness_person['name']

    # --- UI Setup ---
    st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

    # FIXED: unsafe_allow_html=True used to avoid TypeError
    st.markdown("""
        <style>
        .stApp { background: #f1f5f9; }
        [data-testid="stSidebar"] { background-color: #0f172a !important; color: white; }
        .shift-header { padding: 18px; border-radius: 12px; color: white; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .shift-a { background: linear-gradient(135deg, #dc2626, #f87171); }
        .shift-b { background: linear-gradient(135deg, #2563eb, #60a5fa); }
        .shift-c { background: linear-gradient(135deg, #059669, #34d399); }
        .summary-box { border: 2px solid #000; padding: 15px; margin-bottom: 15px; background-color: #f9fafb !important; border-radius: 8px; }
        .leave-box { border: 1px dashed #666; padding: 10px; margin-top: 20px; font-size: 16px; background-color: #fff !important; }
        @media print { .stButton, .stSidebar, footer, header, hr, .no-print { display: none !important; } .main { padding: 10px !important; } }
        </style>
        """, unsafe_allow_html=True)

    st.title("🛡️ Mathalamparai Duty System")

    selected_date = st.sidebar.date_input("Select Date", datetime.now())
    day_str = str(selected_date.day)
    target_shift = st.sidebar.selectbox("Select Shift to View/Print", ["A Shift", "B Shift", "C Shift", "All Shifts"])

    col1, col2 = st.columns([1, 1])
    with col1:
        gen_btn = st.button('🚀 Generate Rotation')
    with col2:
        # Working Print Button
        st.components.v1.html('<button style="background: #2563eb; color: white; padding: 12px 24px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; width: 100%;" onclick="window.parent.print()">🖨️ Print to PDF</button>', height=60)

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

            if date_col_idx:
                shift_data = {"A": [], "B": [], "C": []}
                supervisors_by_shift = {"A": [], "B": [], "C": []}
                week_offs, on_leave = [], []

                for i in range(len(df_raw)):
                    if i > 85: break
                    name = str(df_raw.iloc[i, 1]).strip().upper()
                    status = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                    
                    if name and name not in ["NAME", "NAN", "STAFF NAME"]:
                        if status == "WO" or status == "W/O" or "OFF" in status:
                            week_offs.append(name)
                        elif status == "L" or "LEAVE" in status:
                            on_leave.append(name)
                        elif any(sup in name for sup in supervisors_pool):
                            if status in ["A", "B", "C"]: supervisors_by_shift[status].append(name)
                        elif status in ["A", "B", "C"]:
                            shift_data[status].append({'id': i, 'name': name})

                # --- Sidebar Summary ---
                st.sidebar.markdown("---")
                st.sidebar.subheader("📊 Summary")
                st.sidebar.info(f"🏖️ **Week Off:**\n" + "\n".join([f"- {n}" for n in week_offs]) if week_offs else "None")
                st.sidebar.warning(f"🏥 **On Leave:**\n" + "\n".join([f"- {n}" for n in on_leave]) if on_leave else "None")

                display_list = ["A", "B", "C"] if target_shift == "All Shifts" else [target_shift[0]]

                for s in display_list:
                    if not shift_data[s]: continue
                    
                    rot, rec, wellness = generate_shift_rotation(shift_data[s], (selected_date.weekday() >= 5), selected_date)
                    dropdown_options = sorted([stf['name'] for stf in shift_data[s]] + ["VACANT", "OFF"])

                    # Shift Header
                    color_class = f"shift-{s.lower()}"
                    st.markdown(f'<div class="shift-header {color_class}">📅 {s} SHIFT - {selected_date.strftime("%d-%b-%Y")}</div>', unsafe_allow_html=True)
                    
                    # PRINT SUMMARY (Supervisor, Reception, Wellness)
                    st.markdown(f"""
                    <div class="summary-box">
                        <b>👨‍💼 Supervisor:</b> {", ".join(supervisors_by_shift[s]) if supervisors_by_shift[s] else "N/A"} <br>
                        <b>🛎️ Reception:</b> {", ".join(rec)} <br>
                        <b>🏥 Wellness:</b> {wellness}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Main Duty Table with Dropdown
                    st.data_editor(
                        pd.DataFrame(rot),
                        column_config={"Staff Name": st.column_config.SelectboxColumn("Staff Name", options=dropdown_options, width="large")},
                        hide_index=True, use_container_width=True, key=f"editor_{s}"
                    )
                    
                    # NEW: LEAVE & WEEK OFF DETAILS (Now shows up in PRINT too)
                    st.markdown(f"""
                    <div class="leave-box">
                        <b>🏖️ Today's Week Off:</b> {", ".join(week_offs) if week_offs else "None"} <br>
                        <b>🏥 Today's On Leave:</b> {", ".join(on_leave) if on_leave else "None"}
                    </div>
                    """, unsafe_allow_html=True)
                    st.divider()
            else:
                st.error("Date column not found in Sheet!")
        except Exception as e:
            st.error(f"Error: {e}")
