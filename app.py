import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import pytz
import os
import re
import random

# --- 1. CONFIGURATION ---
CSV_FILE = "duty_database.csv"
sheet_id = "1-adQfc6NIVLpy50L9GpnH75IiX6IMJ-UwjYsx88rmFk" 

# --- 2. PASSWORD LOGIC ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if "screenshot_mode" not in st.session_state:
    st.session_state["screenshot_mode"] = False

def check_password():
    def password_entered():
        if st.session_state["password"] == "Sec@2026": 
            st.session_state["password_correct"] = True
            st.session_state["last_active"] = datetime.now()
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # --- NEW ULTRA-PREMIUM HOLO-LOGIN UI ---
        st.markdown("""
            <style>
            /* Reset & Core Styling */
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
            
            .stApp { 
                font-family: 'Space Grotesk', sans-serif;
                background: #020617; 
                overflow: hidden;
            }
            
            /* Hide Streamlit components on login page */
            header, [data-testid="stSidebar"], .stDeployButton {visibility: hidden; display: none !important;}
            
            /* Background Schematic Grid */
            .stApp::before {
                content: '';
                position: absolute;
                width: 200%; height: 200%;
                top: -50%; left: -50%;
                background-image: 
                    linear-gradient(rgba(56, 189, 248, 0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(56, 189, 248, 0.04) 1px, transparent 1px);
                background-size: 40px 40px;
                transform: rotate(15deg);
                z-index: -1;
            }
            
            /* Main Holographic Container */
            .login-container {
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                height: 80vh; margin-top: 10vh; text-align: center;
                perspective: 1000px;
            }
            
            .holo-card {
                background: rgba(30, 41, 59, 0.1);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(56, 189, 248, 0.15);
                border-radius: 20px;
                padding: 60px 50px;
                box-shadow: 0 0 50px rgba(56, 189, 248, 0.1), inset 0 0 15px rgba(56, 189, 248, 0.1);
                animation: floatIn 1.5s ease-out, floatCard 6s ease-in-out infinite;
                transform-style: preserve-3d;
            }
            
            /* Shield Icon with Dynamic Light Beams */
            .shield-icon {
                font-size: 90px;
                position: relative; margin-bottom: 25px;
                filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.7));
            }
            .shield-icon::after {
                content: ''; position: absolute;
                width: 150px; height: 150px;
                top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: radial-gradient(circle, rgba(56, 189, 248, 0.3) 0%, transparent 70%);
                z-index: -1;
            }
            
            /* Main Title & Subtitle Styling */
            .portal-title {
                font-size: 56px; font-weight: 900; letter-spacing: 8px;
                background: linear-gradient(135deg, #ffffff 10%, #38bdf8 60%, #ffffff 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin: 0; padding-bottom: 5px;
            }
            .portal-subtitle {
                color: #94a3b8; letter-spacing: 10px; font-size: 15px; font-weight: 500;
                margin-top: 5px; margin-bottom: 40px; text-transform: uppercase;
            }
            
            /* Placeholder for Faint Data Readouts */
            .data-readout {
                position: absolute; color: rgba(56, 189, 248, 0.2);
                font-family: monospace; font-size: 10px; letter-spacing: 2px;
                user-select: none;
            }
            .dr-tl {top: 10px; left: 10px;} .dr-tr {top: 10px; right: 10px;}
            .dr-bl {bottom: 10px; left: 10px;} .dr-br {bottom: 10px; right: 10px;}

            /* Animations */
            @keyframes floatIn {
                0% { opacity: 0; transform: translateY(50px) rotateX(-20deg); }
                100% { opacity: 1; transform: translateY(0) rotateX(0); }
            }
            @keyframes floatCard {
                0%, 100% { transform: translateY(0) rotateX(0deg); }
                50% { transform: translateY(-10px) rotateX(2deg); }
            }
            </style>
            
            <div class="login-container">
                <div class="holo-card">
                    <span class="data-readout dr-tl">SYS.STATUS:OK</span>
                    <span class="data-readout dr-tr">SEC_LVL.5</span>
                    <div class="shield-icon">🛡️</div>
                    <h1 class="portal-title">MATHALAMPARAI</h1>
                    <p class="portal-subtitle">EXECUTIVE DUTY PORTAL</p>
                    <span class="data-readout dr-bl">LAT.10.8</span>
                    <span class="data-readout dr-br">LNG.78.2</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Centered input field without label
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.text_input("PASSWORD", type="password", on_change=password_entered, key="password", label_visibility="collapsed", placeholder="🔒 ENTER PASSCODE TO ACCESS")
        
        return False
    return True

# --- 3. DATABASE FUNCTIONS ---
def load_database():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if "Role" not in df.columns: df["Role"] = "GUARD"
            return df
        except:
            return pd.DataFrame(columns=["Date", "Shift", "Staff Name", "Point", "Role"])
    else:
        return pd.DataFrame(columns=["Date", "Shift", "Staff Name", "Point", "Role"])

def save_to_database(new_data):
    if os.path.exists(CSV_FILE):
        history_df = pd.read_csv(CSV_FILE)
        if "Role" not in history_df.columns: history_df["Role"] = "GUARD"
        
        date_str = new_data[0]["Date"]
        shift_str = new_data[0]["Shift"]
        history_df = history_df[~((history_df["Date"] == date_str) & (history_df["Shift"] == shift_str))]
        
        new_df = pd.DataFrame(new_data)
        updated_df = pd.concat([history_df, new_df], ignore_index=True)
    else:
        updated_df = pd.DataFrame(new_data)
    
    updated_df.to_csv(CSV_FILE, index=False)
    return updated_df

def get_role_summary(date_str, shift_str):
    if not os.path.exists(CSV_FILE): return "N/A", "N/A", "N/A"
    
    df = pd.read_csv(CSV_FILE)
    if "Role" not in df.columns: return "N/A", "N/A", "N/A"
    
    mask = (df["Date"] == date_str) & (df["Shift"] == shift_str)
    shift_df = df[mask]
    
    if shift_df.empty: return "N/A", "N/A", "N/A"

    sups = shift_df[shift_df["Role"] == "SUPERVISOR"]["Staff Name"].tolist()
    recep = shift_df[shift_df["Role"] == "RECEPTION"]["Staff Name"].tolist()
    recep_reliever = shift_df[shift_df["Point"] == "RECEPTION RELIEVER"]["Staff Name"].tolist()
    final_recep = recep + recep_reliever
    well = shift_df[shift_df["Role"] == "WELLNESS"]["Staff Name"].tolist()
    
    return ", ".join(sups) if sups else "N/A", \
           ", ".join(final_recep) if final_recep else "N/A", \
           ", ".join(well) if well else "N/A"

def clean_point_name(p):
    return re.sub(r'[^A-Z]', '', str(p).upper())

def get_guard_history(staff_name, current_date):
    if not os.path.exists(CSV_FILE): return {}
    df = pd.read_csv(CSV_FILE)
    if "Role" not in df.columns: return {}

    df["DateObj"] = pd.to_datetime(df["Date"])
    current_date_obj = pd.to_datetime(current_date)

    past_duties = df[(df["Staff Name"] == staff_name) & 
                     (df["Role"] == "GUARD") & 
                     (df["DateObj"] < current_date_obj)].sort_values(by="DateObj", ascending=False)
    
    history = {}
    shift_count = 1
    for pt in past_duties["Point"]:
        pt_clean = clean_point_name(pt)
        if pt_clean not in history:
            history[pt_clean] = shift_count
        shift_count += 1
    return history

def get_penalty(guard_name, point_name, history_map):
    pt_clean = clean_point_name(point_name)
    hist = history_map[guard_name]
    if pt_clean in hist:
        shift_ago = hist[pt_clean]
        if shift_ago <= 11:
            return 10000 - shift_ago 
        else:
            return 100 - shift_ago
    return 0

if check_password():
    # --- AUTO-LOGOUT LOGIC ---
    TIMEOUT_MINUTES = 5 
    
    if "last_active" in st.session_state:
        elapsed_time = datetime.now() - st.session_state["last_active"]
        if elapsed_time > timedelta(minutes=TIMEOUT_MINUTES):
            st.session_state["password_correct"] = False
            st.session_state["screenshot_mode"] = False
            st.warning("⏱️ Session Expired! (5 நிமிடங்களுக்கு மேல் பயன்படுத்தாததால் சிஸ்டம் லாக் செய்யப்பட்டது)")
            st.rerun()
            
    st.session_state["last_active"] = datetime.now()
    # ------------------------------

    st.set_page_config(page_title="Mathalamparai Executive", layout="wide")
    
    if st.session_state["screenshot_mode"]:
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {display: none;}
            header {display: none;}
            .stApp {background-color: #f8fafc;}
            .roster-card { background: white; border: 2px solid #0f172a; border-radius: 12px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); overflow: hidden;}
            .roster-header { background: #0f172a; color: white; text-align: center; padding: 15px; font-weight: 800; font-size: 18px;}
            .roster-body { padding: 20px;}
            .info-text { font-size: 15px; line-height: 1.6; border-bottom: 2px dashed #e2e8f0; padding-bottom: 10px; margin-bottom: 15px;}
            .roster-table { width: 100%; border-collapse: collapse; font-size: 14px;}
            .roster-table th, .roster-table td { border: 1px solid #cbd5e1; padding: 10px; text-align: left;}
            .roster-table th { background: #f1f5f9; font-weight: bold; color: #334155;}
            .vacant { color: #dc2626; font-weight: bold; }
            .extra { background-color: #f8fafc; font-style: italic; }
            .footer-card { margin-top: 15px; font-size: 13px; font-weight: bold;}
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("❌ EXIT SCREENSHOT MODE", use_container_width=True):
                st.session_state["screenshot_mode"] = False
                st.rerun()

    if not st.session_state["screenshot_mode"]:
        st.markdown("""
            <style>
            .stApp { background-color: #f8fafc; font-family: sans-serif; }
            [data-testid="stSidebar"] { background-color: #0f172a !important; }
            [data-testid="stSidebar"] label { color: #ffffff !important; font-weight: bold !important; }
            .main-header { background: #0f172a; padding: 20px; border-radius: 0 0 20px 20px; color: #f1f5f9; text-align: center; display: flex; justify-content: space-between; align-items: center; }
            .shift-banner { padding: 15px; border-radius: 12px; color: white; text-align: center; font-size: 24px; font-weight: 800; margin: 15px 0; border: 2px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .a-shift { background: linear-gradient(90deg, #be123c, #fb7185); }
            .b-shift { background: linear-gradient(90deg, #1d4ed8, #60a5fa); }
            .c-shift { background: linear-gradient(90deg, #047857, #34d399); }
            .stat-row { display: flex; gap: 10px; margin-bottom: 15px; }
            .stat-card { background: white; padding: 15px; border-radius: 10px; flex: 1; text-align: center; border: 1px solid #e2e8f0; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            </style>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("<h2 style='text-align: center; color: white;'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 EXIT SYSTEM", use_container_width=True):
        st.session_state["password_correct"] = False
        st.rerun()
    st.sidebar.divider()
    
    # --- TIME CALCULATION ---
    ist = pytz.timezone('Asia/Kolkata')
    current_time_obj = datetime.now(ist)
    current_time = current_time_obj.strftime("%I:%M %p")
    current_hour = current_time_obj.hour
    
    today_date = current_time_obj.date()
    current_year = today_date.year
    
    ALLOWED_START_DATE = datetime(current_year, 1, 1).date()
    ALLOWED_END_DATE = datetime(current_year, 12, 31).date() 
    
    if today_date < ALLOWED_START_DATE:
        default_date = ALLOWED_START_DATE
    elif today_date > ALLOWED_END_DATE:
        default_date = ALLOWED_END_DATE
    else:
        default_date = today_date

    selected_date = st.sidebar.date_input("SELECT DATE", value=default_date, min_value=ALLOWED_START_DATE, max_value=ALLOWED_END_DATE)
    
    # --- AUTO SHIFT SELECTION LOGIC ---
    if 4 <= current_hour < 12: # 4 AM to 11:59 AM
        default_shift_index = 0  # A Shift
    elif 12 <= current_hour < 19: # 12 PM to 6:59 PM
        default_shift_index = 1  # B Shift
    else: # 7 PM to 3:59 AM
        default_shift_index = 2  # C Shift

    target_shift = st.sidebar.selectbox("SELECT SHIFT", ["A Shift", "B Shift", "C Shift"], index=default_shift_index)
    
    st.sidebar.markdown("<br>"*2, unsafe_allow_html=True)
    secret_edit = st.sidebar.checkbox("✏️ EDIT MODE", help="Enable to edit duties manually")
    
    if not st.session_state["screenshot_mode"]:
        st.markdown(f"<div class='main-header'><div>🛡️ PERMANENT DUTY SYSTEM</div><div>🕒 {current_time}</div></div>", unsafe_allow_html=True)

    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULson"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
    regular_duty_points = ["1. MAIN GATE-1", "2. SECOND GATE", "3. CAR PARKING", "4. PATROLLING", "5. MAIN GATE-2", "6. DG POWER ROOM", "7. A BLOCK AREA", "8. B BLOCK AREA", "9. C BLOCK AREA", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    dynamic_sheet_name = selected_date.strftime("%B-%Y").upper()
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(dynamic_sheet_name)}"

    try:
        db_df = load_database()
        date_str_key = selected_date.strftime("%Y-%m-%d")
        shift_data = db_df[(db_df["Date"] == date_str_key) & (db_df["Shift"] == target_shift)]
        has_guards = not shift_data[shift_data["Role"] == "GUARD"].empty
        
        with st.spinner("🔄 Checking Live Updates in Sheet..."):
            df_raw = pd.read_csv(url, header=None)
            
        day_str = str(selected_date.day)
        date_col_idx = None
        for r in range(min(15, len(df_raw))):
            for c in range(len(df_raw.columns)):
                if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]:
                    date_col_idx = c; break
            if date_col_idx is not None: break

        sheet_code = target_shift[0]
        staff_on_duty, sups, week_offs, on_leave, general_staff = [], [], [], [], []
        
        if date_col_idx:
            for i in range(len(df_raw)):
                if i > 85: break
                name = str(df_raw.iloc[i, 1]).strip().upper()
                status = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                
                if name and name not in ["NAME", "NAN"]:
                    if status in ["WO", "W/O", "OFF"]: week_offs.append(name)
                    elif status in ["L", "LEAVE"]: on_leave.append(name)
                    elif status in ["G", "GEN", "GENERAL"]:
                        if any(s in name for s in supervisors_pool): sups.append(f"{name} (GEN)") 
                        else: general_staff.append(name)
                    elif status == sheet_code: 
                        if any(s in name for s in supervisors_pool): sups.append(name)
                        else: staff_on_duty.append({'id': i, 'name': name})

        db_wo = shift_data[shift_data["Role"] == "WO"]["Staff Name"].tolist()
        db_leave = shift_data[shift_data["Role"] == "LEAVE"]["Staff Name"].tolist()
        db_guards_names = shift_data[shift_data["Role"] == "GUARD"]["Staff Name"].tolist()
        db_guards_real = [g for g in db_guards_names if g != "VACANT"]
        
        specialist_present = next((s for s in staff_on_duty if any(w in s['name'] for w in wellness_specialists)), None)
        regular_recep_present = [s for s in staff_on_duty if any(r in s['name'] for r in receptionists_pool)]
        guards_pool = [s for s in staff_on_duty if s not in regular_recep_present and (not specialist_present or s['name'] != specialist_present['name'])]
        sheet_guard_names = [g['name'] for g in guards_pool]

        leaves_changed = (set(week_offs) != set(db_wo)) or (set(on_leave) != set(db_leave))
        guards_changed = (set(sheet_guard_names) != set(db_guards_real))
        
        sync_needed = (not has_guards) or leaves_changed or guards_changed

        if not sync_needed:
            if not secret_edit and not st.session_state["screenshot_mode"]: 
                st.success("✅ SYSTEM UP TO DATE (No changes in Sheet)")
            
            sups_text, recep_text, wellness_text = get_role_summary(date_str_key, target_shift)
            wo_names = ", ".join(week_offs) if week_offs else "NONE"
            ol_names = ", ".join(on_leave) if on_leave else "NONE"
            
            guard_df = shift_data[shift_data["Role"] == "GUARD"].copy()
            point_order = {p: i for i, p in enumerate(regular_duty_points)}
            def sort_key(pt):
                if pt == "RECEPTION RELIEVER": return 0
                return point_order.get(pt, 100 + int(pt.split('-')[1]) if "EXTRA" in pt else 200)
            guard_df["sort_val"] = guard_df["Point"].apply(sort_key)
            df_display = guard_df.sort_values("sort_val")[["Point", "Staff Name"]]
            
        else:
            if has_guards and not st.session_state["screenshot_mode"]:
                st.warning("⚠️ Sheet Updates Detected! Auto-Syncing...")

            wellness = "VACANT"
            if specialist_present: wellness = specialist_present['name']
            elif selected_date.weekday() == 1 and guards_pool:
                week_num = selected_date.isocalendar()[1]
                wellness = guards_pool.pop(week_num % len(guards_pool))['name']

            final_recep_team = [r['name'] for r in regular_recep_present]
            reception_reliever_name = None
            if selected_date.weekday() == 5 and guards_pool:
                week_num = selected_date.isocalendar()[1]
                reception_reliever_name = guards_pool.pop((week_num + 3) % len(guards_pool))['name']
            
            current_duty_points = list(regular_duty_points)
            if target_shift == "C Shift": current_duty_points[9] = "10. ESCORT"

            sacrifice_points = ["2. SECOND GATE", "7. A BLOCK AREA", "4. PATROLLING"]
            shortage = 12 - len(guards_pool)
            points_forced_vacant = sacrifice_points[:shortage] if shortage > 0 else []
            active_duty_points = [p for p in current_duty_points if p not in points_forced_vacant]

            available_today = list(active_duty_points)
            day_of_year = selected_date.timetuple().tm_yday
            if available_today:
                shift_amt = day_of_year % len(available_today)
                available_today = available_today[shift_amt:] + available_today[:shift_amt]

            final_assignments = {}
            unassigned_guards = []
            history_map = {}
            
            existing_guard_assignments = {}
            if not shift_data.empty:
                for _, r in shift_data[shift_data["Role"] == "GUARD"].iterrows():
                    existing_guard_assignments[r["Staff Name"]] = r["Point"]
            
            for guard in guards_pool:
                g_name = guard['name']
                history_map[g_name] = get_guard_history(g_name, date_str_key)
                
                if g_name in existing_guard_assignments:
                    pt = existing_guard_assignments[g_name]
                    if pt in available_today:
                        final_assignments[g_name] = pt
                        available_today.remove(pt)
                    else:
                        unassigned_guards.append(guard)
                else:
                    unassigned_guards.append(guard)

            best_temp_assignments = {}
            least_penalty = float('inf')
            
            for attempt in range(500):
                temp_assignments = {}
                temp_available = list(available_today)
                current_penalty = 0
                
                random.shuffle(unassigned_guards)
                
                for guard in unassigned_guards:
                    g_name = guard['name']
                    
                    temp_available.sort(key=lambda p: get_penalty(g_name, p, history_map))
                    
                    if temp_available:
                        best_score = get_penalty(g_name, temp_available[0], history_map)
                        best_points = [p for p in temp_available if get_penalty(g_name, p, history_map) == best_score]
                        
                        chosen_pt = random.choice(best_points)
                        temp_assignments[g_name] = chosen_pt
                        current_penalty += best_score
                        temp_available.remove(chosen_pt)

                if current_penalty < least_penalty:
                    least_penalty = current_penalty
                    best_temp_assignments = temp_assignments
                    if least_penalty == 0:
                        break 

            final_assignments.update(best_temp_assignments)

            rot_data = []
            save_list = []
            
            for name, point in final_assignments.items():
                rot_data.append({"Point": point, "Staff Name": name})
                save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": name, "Point": point, "Role": "GUARD"})
            
            if reception_reliever_name:
                rot_data.append({"Point": "RECEPTION RELIEVER", "Staff Name": reception_reliever_name})
                save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": reception_reliever_name, "Point": "RECEPTION RELIEVER", "Role": "GUARD"})

            assigned_names = list(final_assignments.keys())
            if reception_reliever_name: assigned_names.append(reception_reliever_name)
            
            extra_c = 1
            for guard in guards_pool:
                if guard['name'] not in assigned_names:
                    p_name = f"EXTRA-{extra_c}. GENERAL RELIEVER"
                    rot_data.append({"Point": p_name, "Staff Name": guard['name']})
                    save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": guard['name'], "Point": p_name, "Role": "GUARD"})
                    extra_c += 1

            assigned_point_names = final_assignments.values()
            for pt in current_duty_points:
                if pt not in assigned_point_names:
                    rot_data.append({"Point": pt, "Staff Name": "VACANT"})
                    save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": "VACANT", "Point": pt, "Role": "GUARD"})
            
            if target_shift == "A Shift":
                gen_start = 13
                for g in general_staff:
                    p_name = f"{gen_start}. OLD CAR PARKING (General)"
                    rot_data.append({"Point": p_name, "Staff Name": g})
                    save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": g, "Point": p_name, "Role": "GUARD"})
                    gen_start += 1
                    
            for s in sups: save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": s, "Point": "SUPERVISOR", "Role": "SUPERVISOR"})
            for r in final_recep_team: save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": r, "Point": "RECEPTION", "Role": "RECEPTION"})
            if wellness != "VACANT": save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": wellness, "Point": "WELLNESS", "Role": "WELLNESS"})
            for w in week_offs: save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": w, "Point": "WO", "Role": "WO"})
            for l in on_leave: save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": l, "Point": "LEAVE", "Role": "LEAVE"})

            save_to_database(save_list)
            
            point_order = {p: i for i, p in enumerate(current_duty_points)}
            def sort_key(pt):
                if pt == "RECEPTION RELIEVER": return 0
                return point_order.get(pt, 100 + int(pt.split('-')[1]) if "EXTRA" in pt else 200)

            rot_data.sort(key=lambda x: sort_key(x["Point"]))
            df_display = pd.DataFrame(rot_data)
            
            sups_text, recep_text, wellness_text = get_role_summary(date_str_key, target_shift)
            wo_names = ", ".join(week_offs) if week_offs else "NONE"
            ol_names = ", ".join(on_leave) if on_leave else "NONE"

        if st.session_state["screenshot_mode"]:
            html_rows = ""
            for _, row in df_display.iterrows():
                name = row['Staff Name']
                style_class = "vacant" if name == "VACANT" else ("extra" if "EXTRA" in row['Point'] else "")
                html_rows += f"<tr><td>{row['Point']}</td><td class='{style_class}'>{name}</td></tr>"

            card_html = f"""
            <div class="login-container">
                <div class="holo-card">
                    <span class="data-readout dr-tl">SYS.STATUS:OK</span>
                    <span class="data-readout dr-tr">SEC_LVL.5</span>
                    <div class="shield-icon">🛡️</div>
                    <h1 class="portal-title">MATHALAMPARAI</h1>
                    <p class="portal-subtitle">EXECUTIVE DUTY PORTAL</p>
                    <span class="data-readout dr-bl">LAT.10.8</span>
                    <span class="data-readout dr-br">LNG.78.2</span>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
        else:
            st.markdown(f'<div class="shift-banner {target_shift[0].lower()}-shift">📅 {target_shift} - {selected_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            
            st.markdown(f"""<div class="stat-row">
                <div class="stat-card"><small>SUPERVISOR</small><br><b>{sups_text}</b></div>
                <div class="stat-card"><small>RECEPTION</small><br><b>{recep_text}</b></div>
                <div class="stat-card"><small>WELLNESS</small><br><b>{wellness_text}</b></div>
            </div>""", unsafe_allow_html=True)

            df_display = df_display.reset_index(drop=True)
            df_display.index += 1

            if secret_edit:
                st.warning("⚠️ EDIT MODE ENABLED - Changes are saved permanently!")
                dropdown_names = sorted(df_display["Staff Name"].unique().tolist() + 
                                      shift_data[shift_data["Role"].isin(["WO", "LEAVE", "SUPERVISOR"])]["Staff Name"].tolist() + 
                                      ["VACANT"])
                
                edited_df = st.data_editor(
                    df_display, 
                    column_config={
                        "Staff Name": st.column_config.SelectboxColumn("ASSIGN STAFF", options=dropdown_names),
                        "Point": st.column_config.Column(disabled=True)
                    }, 
                    use_container_width=True,
                    key="data_editor"
                )
                
                if st.button("💾 SAVE CHANGES TO DATABASE", type="primary"):
                    staff_list = edited_df["Staff Name"].tolist()
                    duplicates = []
                    seen = set()
                    
                    for name in staff_list:
                        if name != "VACANT":
                            if name in seen:
                                duplicates.append(name)
                            seen.add(name)
                    
                    if duplicates:
                        dup_names = ", ".join(set(duplicates))
                        st.error(f"⚠️ பிழை: '{dup_names}' irandu idangalil ullathu! Oruvarukku sariyaga matrivittu save seyyavum.")
                    else:
                        current_db = pd.read_csv(CSV_FILE)
                        mask_keep = ~((current_db["Date"] == date_str_key) & 
                                      (current_db["Shift"] == target_shift) & 
                                      (current_db["Role"] == "GUARD"))
                        new_db = current_db[mask_keep].copy()
                        
                        new_rows = []
                        for _, row in edited_df.iterrows():
                            new_rows.append({
                                "Date": date_str_key, 
                                "Shift": target_shift, 
                                "Staff Name": row["Staff Name"], 
                                "Point": row["Point"], 
                                "Role": "GUARD"
                            })
                        
                        final_db = pd.concat([new_db, pd.DataFrame(new_rows)], ignore_index=True)
                        final_db.to_csv(CSV_FILE, index=False)
                        st.success("Changes Saved Permanently!")
                        st.rerun()
            else:
                st.table(df_display)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("📸 OPEN SCREENSHOT MODE", use_container_width=True, type="primary"):
                        st.session_state["screenshot_mode"] = True
                        st.rerun()
            
            st.markdown(f"""<div class="footer-info" style='background: white; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 14px; margin-top: 15px;'>
                <span><b style='color:#1e3a8a;'>🏖️ WEEK OFF:</b> <span style='color:#dc2626; font-weight:bold;'>{wo_names}</span></span>
                <span><b style='color:#1e3a8a;'>🏥 ON LEAVE:</b> <span style='color:#dc2626; font-weight:bold;'>{ol_names}</span></span>
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        if "HTTP Error 400: Bad Request" in str(e):
            st.error(f"⚠️ Error: Google Sheet-il '{dynamic_sheet_name}' endra peyaril Tab illai! Sheet-ai saripaarkkavum.")
        else:
            st.error(f"System Error: {e}")
