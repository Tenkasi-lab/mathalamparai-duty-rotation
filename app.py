import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. LOGIN LOGIC ---
def check_password():
    def password_entered():
        if st.session_state["password"] == datetime.now().strftime("%d%m"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center;'>🛡️ Mathalamparai Duty System</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Enter Daily PIN", type="password", on_change=password_entered, key="password")
        return False
    return True

if check_password():
    # Google Sheet Config
    sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
    sheet_name = "FEBRUARY-2026" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"

    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
    regular_duty_points = ["1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

    # PREMIUM CSS
    st.markdown("""
        <style>
        .stApp { background: #f8fafc; }
        .shift-header { padding: 15px; border-radius: 12px; color: white; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
        .shift-a { background: linear-gradient(90deg, #e11d48, #fb7185); }
        .shift-b { background: linear-gradient(90deg, #2563eb, #60a5fa); }
        .shift-c { background: linear-gradient(90deg, #059669, #34d399); }
        .summary-banner { background: white; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 15px; display: flex; justify-content: space-around; font-size: 15px; }
        @media print { .no-print, .stButton, [data-testid="stSidebar"], .stCheckbox { display: none !important; } }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar
    if st.sidebar.button("🔒 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    selected_date = st.sidebar.date_input("Select Date", datetime.now())
    target_shift = st.sidebar.selectbox("Select Shift", ["A Shift", "B Shift", "C Shift"])

    # --- EDIT OPTION TOGGLE ---
    st.sidebar.markdown("---")
    edit_mode = st.sidebar.toggle("🛠️ Enable Edit Mode", value=False)
    
    st.markdown("<h2 style='color: #1e293b;'>🛡️ Mathalamparai Duty Dashboard</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        gen_btn = st.button('🚀 Refresh Duty Rotation')
    with col2:
        st.components.v1.html('<button style="background: #0f172a; color: white; padding: 10px 24px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; width: 100%;" onclick="window.parent.print()">🖨️ Print Final Roster (PDF)</button>', height=60)

    if gen_btn or 'current_df' in st.session_state:
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

            if date_col_idx:
                shift_code = target_shift[0]
                staff_on_duty = []
                sups = []
                week_offs, on_leave = [], []

                for i in range(len(df_raw)):
                    if i > 85: break
                    name = str(df_raw.iloc[i, 1]).strip().upper()
                    status = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                    
                    if name and name not in ["NAME", "NAN"]:
                        if status in ["WO", "W/O", "OFF"]: week_offs.append(name)
                        elif status in ["L", "LEAVE"]: on_leave.append(name)
                        elif any(s in name for s in supervisors_pool) and status == shift_code: sups.append(name)
                        elif status == shift_code: staff_on_duty.append({'id': i, 'name': name})

                wellness = next((s['name'] for s in staff_on_duty if any(w in s['name'] for w in wellness_specialists)), "VACANT")
                recep = [s['name'] for s in staff_on_duty if any(r in s['name'] for r in receptionists_pool)][:2]
                guards = [s for s in staff_on_duty if s['name'] != wellness and s['name'] not in recep]

                # Initial Rotation Data
                if gen_btn or 'current_df' not in st.session_state:
                    rot_data = [{"Point": p, "Staff Name": (guards[idx % len(guards)]['name'] if guards else "VACANT")} for idx, p in enumerate(regular_duty_points)]
                    st.session_state.current_df = pd.DataFrame(rot_data)

                # RENDER
                st.markdown(f'<div class="shift-header shift-{shift_code.lower()}">📅 {target_shift} - {selected_date.strftime("%d-%b-%Y")}</div>', unsafe_allow_html=True)
                
                st.markdown(f"""<div class="summary-banner">
                    <div><b>👨‍💼 Supervisor:</b> {", ".join(sups) if sups else "N/A"}</div>
                    <div><b>🛎️ Reception:</b> {", ".join(recep) if recep else "N/A"}</div>
                    <div><b>🏥 Wellness:</b> {wellness}</div>
                </div>""", unsafe_allow_html=True)

                # --- EDIT vs VIEW MODE ---
                if edit_mode:
                    st.warning("⚠️ Edit Mode Active: Select names from dropdown and click 'Save Changes'")
                    dropdown_names = sorted([s['name'] for s in staff_on_duty] + ["VACANT", "OFF"])
                    
                    edited_df = st.data_editor(
                        st.session_state.current_df,
                        column_config={"Staff Name": st.column_config.SelectboxColumn("Edit Staff", options=dropdown_names, width="large")},
                        hide_index=True, use_container_width=True
                    )
                    if st.button("💾 Save Changes"):
                        st.session_state.current_df = edited_df
                        st.success("Changes Saved Successfully!")
                        st.rerun()
                else:
                    st.table(st.session_state.current_df)

                st.markdown(f"""<div style='background: white; padding: 10px; border-radius: 8px; border-left: 5px solid #64748b; margin-top:10px;'>
                    <small>🏖️ <b>Week Off:</b> {", ".join(week_offs) if week_offs else "None"} | 🏥 <b>Leave:</b> {", ".join(on_leave) if on_leave else "None"}</small>
                </div>""", unsafe_allow_html=True)
            else: st.error("Date column not found in Sheet!")
        except Exception as e: st.error(f"Error: {e}")
