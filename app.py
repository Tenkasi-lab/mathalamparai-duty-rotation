import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. SESSION SETUP ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

# --- 2. SINGLE PASSWORD LOGIC ---
def check_password():
    def password_entered():
        # UNGA FIXED PASSWORD INGA IRUKKU (Maanthikalam)
        if st.session_state["password"] == "1234": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("""
            <style>
            .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
            .login-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 40px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center; color: white; margin-top: 50px; }
            </style>
            <div class='login-card'><h1>🛡️</h1><h2>MATHALAMPARAI</h2><p>EXECUTIVE DUTY PORTAL</p></div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.text_input("ENTER PASSWORD", type="password", on_change=password_entered, key="password")
        return False
    return True

if check_password():
    # --- 3. VARIABLES ---
    sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
    sheet_name = "FEBRUARY-2026" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"
    
    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
    
    # 1 to 12 Points (Rotation)
    regular_duty_points = ["1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    st.set_page_config(page_title="Mathalamparai Executive", layout="wide")

    # --- 4. ADVANCED CSS ---
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        
        /* SIDEBAR FIXES */
        [data-testid="stSidebar"] { background-color: #0f172a !important; }
        [data-testid="stSidebar"] label { color: #ffffff !important; font-weight: bold !important; }
        
        /* DROPDOWN & INPUT TEXT FIX */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div { background-color: white !important; color: black !important; }
        [data-testid="stSidebar"] div[data-baseweb="select"] span { color: black !important; }
        [data-testid="stSidebar"] input { color: black !important; background-color: white !important; }
        
        /* LOGOUT BUTTON (Red) */
        [data-testid="stSidebar"] .stButton > button { background-color: #ef4444 !important; color: white !important; border: 1px solid #b91c1c !important; }

        /* HIDDEN CHECKBOX (Secret Dot) */
        [data-testid="stSidebar"] .stCheckbox label span { color: #334155 !important; font-size: 10px !important; }

        /* PRINT OPTIMIZATION */
        @media print {
            .no-print, [data-testid="stSidebar"], .stButton, header, footer { display: none !important; }
            .main { padding: 0 !important; }
            .stApp { background: white !important; }
            .main-header { padding: 10px !important; margin-bottom: 5px !important; }
            .shift-banner { padding: 5px !important; font-size: 16px !important; margin-bottom: 5px !important; }
            .stat-row { gap: 5px !important; margin-bottom: 5px !important; }
            .stat-card { padding: 5px !important; font-size: 10px !important; border-bottom: 2px solid #334155 !important; }
            table { font-size: 9px !important; width: 100% !important; border-collapse: collapse !important; }
            td, th { padding: 2px !important; border: 1px solid #ddd !important; }
        }
        
        .main-header { background: #0f172a; padding: 20px; border-radius: 0 0 20px 20px; color: #f1f5f9; text-align: center; display: flex; justify-content: space-between; align-items: center; }
        .shift-banner { padding: 15px; border-radius: 12px; color: white; text-align: center; font-size: 24px; font-weight: 800; margin: 15px 0; }
        .a-shift { background: linear-gradient(90deg, #be123c, #fb7185); }
        .b-shift { background: linear-gradient(90deg, #1d4ed8, #60a5fa); }
        .c-shift { background: linear-gradient(90deg, #047857, #34d399); }
        .stat-row { display: flex; gap: 10px; margin-bottom: 15px; }
        .stat-card { background: white; padding: 15px; border-radius: 10px; flex: 1; text-align: center; border: 1px solid #e2e8f0; }
        </style>
        """, unsafe_allow_html=True)

    # --- 5. SIDEBAR CONTROLS ---
    st.sidebar.markdown("<h2 style='text-align: center; color: white;'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 EXIT SYSTEM", use_container_width=True):
        st.session_state["password_correct"] = False
        st.rerun()

    st.sidebar.divider()
    
    selected_date = st.sidebar.date_input("SELECT DATE", datetime.now())
    target_shift = st.sidebar.selectbox("SELECT SHIFT", ["A Shift", "B Shift", "C Shift"])
    
    # SECRET EDIT MODE (Small dot at bottom)
    st.sidebar.markdown("<br>"*5, unsafe_allow_html=True)
    secret_edit = st.sidebar.checkbox(".", help="Secret Admin Mode") 

    # --- 6. MAIN LOGIC (Auto Run) ---
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"""
        <div class='main-header no-print'>
            <div style='font-size:20px;'>🛡️ MATHALAMPARAI DUTY DASHBOARD</div>
            <div style='font-size:16px; color:#facc15;'>🕒 {current_time}</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col2: 
        st.components.v1.html('<button style="background: #1e293b; color: #facc15; padding: 12px 24px; border-radius: 12px; border: 2px solid #facc15; font-weight: bold; cursor: pointer; width: 100%;" onclick="window.parent.print()">🖨️ EXPORT TO PDF</button>', height=60)

    try:
        # DATA FETCHING
        df_raw = pd.read_csv(url, header=None)
        day_str = str(selected_date.day)
        date_col_idx = None
        for r in range(min(15, len(df_raw))):
            for c in range(len(df_raw.columns)):
                if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]:
                    date_col_idx = c; break
            if date_col_idx is not None: break

        if date_col_idx:
            shift_code = target_shift[0]
            staff_on_duty, sups, week_offs, on_leave = [], [], [], []
            general_supervisor = None
            general_staff = []

            for i in range(len(df_raw)):
                if i > 85: break
                name = str(df_raw.iloc[i, 1]).strip().upper()
                status = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                
                if name and name not in ["NAME", "NAN"]:
                    if status in ["WO", "W/O", "OFF"]: week_offs.append(name)
                    elif status in ["L", "LEAVE"]: on_leave.append(name)
                    
                    # LOGIC: Check for General Duty (G or GEN)
                    elif status in ["G", "GEN", "GENERAL"]:
                        if any(s in name for s in supervisors_pool):
                            general_supervisor = name # Sunday Supervisor
                        else:
                            general_staff.append(name) # Old Car Parking Staff
                    
                    elif any(s in name for s in supervisors_pool) and status == shift_code: sups.append(name)
                    elif status == shift_code: staff_on_duty.append({'id': i, 'name': name})

            # --- WELLNESS (Tuesday Reliever Logic) ---
            wellness = "VACANT"
            specialist_present = next((s['name'] for s in staff_on_duty if any(w in s['name'] for w in wellness_specialists)), None)
            
            if specialist_present:
                wellness = specialist_present
            elif selected_date.weekday() == 1: # Tuesday
                potential_relievers = [s['name'] for s in staff_on_duty if not any(r in s['name'] for r in receptionists_pool)]
                if potential_relievers: wellness = potential_relievers[0]
            
            recep = [s['name'] for s in staff_on_duty if any(r in s['name'] for r in receptionists_pool)][:2]
            guards = [s for s in staff_on_duty if s['name'] != wellness and s['name'] not in recep]

            # Generate Rotation (1-12)
            rot_data = [{"Point": p, "Staff Name": (guards[idx % len(guards)]['name'] if guards else "VACANT")} for idx, p in enumerate(regular_duty_points)]
            
            # ADD 13. FIXED OLD CAR PARKING (General Staff)
            old_car_parking_staff = " & ".join(general_staff) if general_staff else "VACANT"
            rot_data.append({"Point": "13. OLD CAR PARKING (General)", "Staff Name": old_car_parking_staff})

            # Update Session State
            if 'current_date' not in st.session_state or st.session_state.current_date != selected_date or st.session_state.current_shift != target_shift:
                st.session_state.current_df = pd.DataFrame(rot_data)
                st.session_state.current_date = selected_date
                st.session_state.current_shift = target_shift

            # RENDER DASHBOARD
            st.markdown(f'<div class="shift-banner {shift_code.lower()}-shift">📅 {target_shift} - {selected_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            
            # Display Sunday General Supervisor if present
            gen_sup_display = f"<br><span style='color:#b91c1c; font-size:11px;'>(GEN: {general_supervisor})</span>" if general_supervisor else ""

            st.markdown(f"""<div class="stat-row">
                <div class="stat-card"><small>SUPERVISOR</small><br><b>{", ".join(sups) if sups else "N/A"}</b>{gen_sup_display}</div>
                <div class="stat-card"><small>RECEPTION</small><br><b>{", ".join(recep) if recep else "N/A"}</b></div>
                <div class="stat-card"><small>WELLNESS</small><br><b>{wellness}</b></div>
            </div>""", unsafe_allow_html=True)

            # --- SECRET EDIT MODE ---
            if secret_edit:
                st.warning("⚠️ EDIT MODE ACTIVE")
                dropdown_names = sorted([s['name'] for s in staff_on_duty] + general_staff + ["VACANT", "OFF"])
                edited_df = st.data_editor(st.session_state.current_df, column_config={"Staff Name": st.column_config.SelectboxColumn("ASSIGN STAFF", options=dropdown_names)}, hide_index=True, use_container_width=True)
                if st.button("💾 SAVE CHANGES"):
                    st.session_state.current_df = edited_df
                    st.success("Saved!")
                    st.rerun()
            else:
                st.table(st.session_state.current_df)

            st.markdown(f"""<div class="footer-info" style='background: white; padding: 10px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 13px; margin-top: 10px;'>
                <span>🏖️ <b>WEEK OFF:</b> {", ".join(week_offs) if week_offs else "NONE"}</span>
                <span>🏥 <b>ON LEAVE:</b> {", ".join(on_leave) if on_leave else "NONE"}</span>
            </div>""", unsafe_allow_html=True)
        else: st.error("Date column not found.")
    except Exception as e: st.error(f"System Error: {e}")
