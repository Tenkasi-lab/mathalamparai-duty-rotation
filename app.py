import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import pytz

# --- 1. SESSION SETUP ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if "duty_history" not in st.session_state:
    st.session_state.duty_history = {}

# --- 2. PASSWORD LOGIC ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "Sec@2026": 
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
    regular_duty_points = ["1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    st.set_page_config(page_title="Mathalamparai Executive", layout="wide")

    # --- 4. CSS ---
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #0f172a !important; }
        [data-testid="stSidebar"] label { color: #ffffff !important; font-weight: bold !important; }
        [data-testid="stSidebar"] div[data-baseweb="select"] > div { background-color: white !important; color: black !important; }
        [data-testid="stSidebar"] div[data-baseweb="select"] span { color: black !important; }
        [data-testid="stSidebar"] input { color: black !important; background-color: white !important; }
        [data-testid="stSidebar"] .stButton > button { background-color: #ef4444 !important; color: white !important; border: 1px solid #b91c1c !important; }
        [data-testid="stSidebar"] .stCheckbox label span { color: #334155 !important; font-size: 10px !important; }
        .stTable th.row_heading, .stDataFrame th.row_heading { font-weight: bold; font-size: 14px; }
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

    # --- 5. SIDEBAR ---
    st.sidebar.markdown("<h2 style='text-align: center; color: white;'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 EXIT SYSTEM", use_container_width=True):
        st.session_state["password_correct"] = False
        st.rerun()

    st.sidebar.divider()
    selected_date = st.sidebar.date_input("SELECT DATE", datetime.now())
    target_shift = st.sidebar.selectbox("SELECT SHIFT", ["A Shift", "B Shift", "C Shift"])
    st.sidebar.markdown("<br>"*5, unsafe_allow_html=True)
    secret_edit = st.sidebar.checkbox(".", help="Secret Admin Mode") 

    # --- 6. MAIN LOGIC ---
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%I:%M %p")
    
    st.markdown(f"""
        <div class='main-header no-print'>
            <div style='font-size:20px;'>🛡️ MATHALAMPARAI DUTY DASHBOARD</div>
            <div style='font-size:16px; color:#facc15;'>🕒 {current_time}</div>
        </div>
    """, unsafe_allow_html=True)

    history_key = f"{selected_date}_{target_shift}"

    try:
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
                    elif status in ["G", "GEN", "GENERAL"]:
                        if any(s in name for s in supervisors_pool): general_supervisor = name
                        else: general_staff.append(name)
                    elif any(s in name for s in supervisors_pool) and status == shift_code: sups.append(name)
                    elif status == shift_code: staff_on_duty.append({'id': i, 'name': name})

            # --- POOLS ---
            specialist_present = next((s for s in staff_on_duty if any(w in s['name'] for w in wellness_specialists)), None)
            regular_recep_present = [s for s in staff_on_duty if any(r in s['name'] for r in receptionists_pool)]
            
            guards_pool = sorted([
                s for s in staff_on_duty 
                if s not in regular_recep_present and (not specialist_present or s['name'] != specialist_present['name'])
            ], key=lambda x: x['name'])
            
            # --- WELLNESS ---
            wellness = "VACANT"
            if specialist_present:
                wellness = specialist_present['name']
            elif selected_date.weekday() == 1: 
                if guards_pool:
                    week_num = selected_date.isocalendar()[1]
                    reliever_idx = week_num % len(guards_pool)
                    reliever = guards_pool.pop(reliever_idx)
                    wellness = reliever['name']

            # --- RECEPTION (SATURDAY) ---
            final_recep_team = [r['name'] for r in regular_recep_present]
            if selected_date.weekday() == 5 and guards_pool: 
                week_num = selected_date.isocalendar()[1]
                recep_reliever_idx = (week_num + 3) % len(guards_pool)
                recep_reliever = guards_pool.pop(recep_reliever_idx)
                final_recep_team.append(recep_reliever['name'])
            
            recep_display = final_recep_team[:2]
            dropdown_names = sorted([s['name'] for s in staff_on_duty] + general_staff + ["VACANT", "OFF"])

            if history_key in st.session_state.duty_history:
                df_display = st.session_state.duty_history[history_key]
            else:
                # --- 1. SET DUTY POINT NAMES ---
                current_duty_points = list(regular_duty_points)
                if target_shift == "C Shift":
                    current_duty_points[9] = "10. ESCORT"

                # --- 2. IDENTIFY VACANCIES (Shortage Check) ---
                sacrifice_points = ["3. SECOND GATE", "9. A BLOCK", "5. PATROLLING"]
                required_count = 12
                available_count = len(guards_pool)
                shortage = required_count - available_count
                
                # Force vacancies ONLY if shortage exists
                points_forced_vacant = sacrifice_points[:shortage] if shortage > 0 else []
                
                # --- 3. FILTER ACTIVE POINTS ---
                active_duty_points = [p for p in current_duty_points if p not in points_forced_vacant]
                
                # --- 4. ASSIGNMENT (NO DUPLICATE LOGIC) ---
                rot_data = []
                day_of_year = selected_date.timetuple().tm_yday
                
                if active_duty_points:
                    shift_amt = day_of_year % len(active_duty_points)
                    rotated_active_points = active_duty_points[shift_amt:] + active_duty_points[:shift_amt]
                    
                    for i, guard in enumerate(guards_pool):
                        if i < len(rotated_active_points):
                            # Normal Assignment
                            rot_data.append({"Point": rotated_active_points[i], "Staff Name": guard['name']})
                        else:
                            # If Extra Staff exists (Surplus), assign as Reliever
                            extra_num = i - len(rotated_active_points) + 1
                            rot_data.append({"Point": f"EXTRA-{extra_num}. GENERAL RELIEVER", "Staff Name": guard['name']})

                # --- 5. FILL VACANCIES (If Shortage) ---
                for vac_point in points_forced_vacant:
                    rot_data.append({"Point": vac_point, "Staff Name": "VACANT"})

                # --- 6. SORT & DISPLAY ---
                point_order = {p: i for i, p in enumerate(current_duty_points)}
                rot_data.sort(key=lambda x: point_order.get(x["Point"], 100))

                if target_shift == "A Shift":
                    gen_start_point = 13
                    for g_staff in general_staff:
                        rot_data.append({"Point": f"{gen_start_point}. OLD CAR PARKING (General)", "Staff Name": g_staff})
                        gen_start_point += 1

                df_display = pd.DataFrame(rot_data)
                if not df_display.empty: df_display.index = df_display.index + 1
                
                st.session_state.duty_history[history_key] = df_display

            # --- RENDER ---
            st.markdown(f'<div class="shift-banner {target_shift[0].lower()}-shift">📅 {target_shift} - {selected_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            
            sup_text = ", ".join(sups) if sups else "N/A"
            if general_supervisor: sup_text += f"<br>{general_supervisor} (GENERAL)"

            st.markdown(f"""<div class="stat-row">
                <div class="stat-card"><small>SUPERVISOR</small><br><b>{sup_text}</b></div>
                <div class="stat-card"><small>RECEPTION</small><br><b>{", ".join(recep_display) if recep_display else "N/A"}</b></div>
                <div class="stat-card"><small>WELLNESS</small><br><b>{wellness}</b></div>
            </div>""", unsafe_allow_html=True)

            if secret_edit:
                st.warning("⚠️ EDIT MODE ACTIVE")
                edited_df = st.data_editor(
                    df_display, 
                    column_config={
                        "Staff Name": st.column_config.SelectboxColumn("ASSIGN STAFF", options=dropdown_names)
                    }, 
                    use_container_width=True
                )
                
                if st.button("💾 SAVE CHANGES"):
                    st.session_state.duty_history[history_key] = edited_df
                    st.success("Saved! Edits are locked for this session.")
                    st.rerun()
            else:
                st.table(df_display)

            wo_names = ", ".join(week_offs) if week_offs else "NONE"
            ol_names = ", ".join(on_leave) if on_leave else "NONE"

            st.markdown(f"""<div class="footer-info" style='background: white; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 14px; margin-top: 15px;'>
                <span><b style='color:#1e3a8a;'>🏖️ WEEK OFF:</b> <span style='color:#dc2626; font-weight:bold;'>{wo_names}</span></span>
                <span><b style='color:#1e3a8a;'>🏥 ON LEAVE:</b> <span style='color:#dc2626; font-weight:bold;'>{ol_names}</span></span>
            </div>""", unsafe_allow_html=True)
        else: st.error("Date column not found.")
    except Exception as e: st.error(f"System Error: {e}")
