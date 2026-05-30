import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import pytz
import os
import re
import random

# --- 0. PAGE CONFIG (Must be first) ---
st.set_page_config(page_title="Mathalamparai Executive", layout="wide")

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
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700;800&display=swap');
            .stApp { font-family: 'Rajdhani', sans-serif; background: linear-gradient(rgba(4, 9, 20, 0.85), rgba(4, 9, 20, 0.95)), url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2000&auto=format&fit=crop') no-repeat center center fixed !important; background-size: cover !important; }
            header, [data-testid="stSidebar"], .stDeployButton {display: none !important;}
            [data-testid="stVerticalBlock"] > div > div { display: flex; justify-content: center; }
            [data-testid="stHorizontalBlock"] { margin-top: 10vh; align-items: center; justify-content: center; }
            .sci-fi-card { background: rgba(2, 12, 27, 0.7); backdrop-filter: blur(10px); border: 2px solid rgba(14, 165, 233, 0.4); border-radius: 15px; padding: 40px; box-shadow: 0 0 30px rgba(14, 165, 233, 0.2), inset 0 0 20px rgba(14, 165, 233, 0.1); text-align: center; animation: pulseGlow 3s infinite alternate; position: relative; width: 100%; max-width: 480px; }
            .sci-fi-card::before, .sci-fi-card::after { content: ''; position: absolute; width: 40px; height: 40px; border-top: 3px solid #0ea5e9; }
            .sci-fi-card::before { top: -2px; left: -2px; border-left: 3px solid #0ea5e9; border-top-left-radius: 15px; }
            .sci-fi-card::after { top: -2px; right: -2px; border-right: 3px solid #0ea5e9; border-top-right-radius: 15px; }
            .sci-fi-card-bottom-left, .sci-fi-card-bottom-right { position: absolute; width: 40px; height: 40px; border-bottom: 3px solid #0ea5e9; }
            .sci-fi-card-bottom-left { bottom: -2px; left: -2px; border-left: 3px solid #0ea5e9; border-bottom-left-radius: 15px; }
            .sci-fi-card-bottom-right { bottom: -2px; right: -2px; border-right: 3px solid #0ea5e9; border-bottom-right-radius: 15px; }
            .shield-icon { font-size: 55px; margin-bottom: 10px; filter: drop-shadow(0 0 15px #0ea5e9); }
            .portal-title { color: #e0f2fe; font-size: 34px; font-weight: 800; letter-spacing: 4px; margin: 0 0 5px 0; text-shadow: 0 0 10px #0ea5e9; white-space: nowrap; }
            .portal-subtitle { color: #38bdf8; font-size: 14px; font-weight: 600; letter-spacing: 5px; margin: 0 0 20px 0; text-transform: uppercase; }
            .target-container { margin-top: 15px; margin-bottom: -15px; position: relative; z-index: 50; }
            .target-text { color: #38bdf8; font-size: 12px; letter-spacing: 2px; font-weight: bold; animation: blinkText 1.5s infinite; }
            .animated-arrow { color: #0ea5e9; font-size: 30px; text-shadow: 0 0 15px #0ea5e9; animation: bouncePoint 1s infinite; margin-top: 5px; }
            @keyframes bouncePoint { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(15px); } }
            @keyframes blinkText { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
            div[data-baseweb="input"] > div { background-color: rgba(2, 6, 23, 0.8) !important; border: 2px solid #0ea5e9 !important; border-radius: 8px; padding: 10px 12px; position: relative; overflow: hidden; }
            div[data-baseweb="input"] > div:focus-within { box-shadow: 0 0 25px rgba(14, 165, 233, 0.8) !important; background-color: rgba(15, 23, 42, 0.9) !important; }
            input[type="password"] { color: #38bdf8 !important; text-align: center; letter-spacing: 5px; font-weight: bold; font-size: 20px; z-index: 10; }
            input::placeholder { letter-spacing: 2px; color: #475569 !important; font-weight: normal; font-size: 14px; }
            @keyframes pulseGlow { from { box-shadow: 0 0 20px rgba(14, 165, 233, 0.1), inset 0 0 10px rgba(14, 165, 233, 0.05); } to { box-shadow: 0 0 40px rgba(14, 165, 233, 0.3), inset 0 0 20px rgba(14, 165, 233, 0.15); } }
            </style>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("""
                <div class="sci-fi-card">
                    <div class="sci-fi-card-bottom-left"></div><div class="sci-fi-card-bottom-right"></div>
                    <div class="shield-icon">🛡️</div>
                    <h1 class="portal-title">MATHALAMPARAI</h1>
                    <p class="portal-subtitle">EXECUTIVE DUTY PORTAL</p>
                    <div class="target-container"><div class="target-text">AWAITING SECURE INPUT</div><div class="animated-arrow">▼</div></div>
            """, unsafe_allow_html=True)
            st.text_input("PASSWORD", type="password", on_change=password_entered, key="password", label_visibility="collapsed", placeholder="ENTER PASSCODE")
            st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# --- 3. DATABASE FUNCTIONS ---
def load_database():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if "Role" not in df.columns: df["Role"] = "GUARD"
            return df
        except: return pd.DataFrame(columns=["Date", "Shift", "Staff Name", "Point", "Role"])
    else: return pd.DataFrame(columns=["Date", "Shift", "Staff Name", "Point", "Role"])

def save_to_database(new_data):
    if os.path.exists(CSV_FILE):
        history_df = pd.read_csv(CSV_FILE)
        if "Role" not in history_df.columns: history_df["Role"] = "GUARD"
        date_str = new_data[0]["Date"]
        shift_str = new_data[0]["Shift"]
        history_df = history_df[~((history_df["Date"] == date_str) & (history_df["Shift"] == shift_str))]
        new_df = pd.DataFrame(new_data)
        updated_df = pd.concat([history_df, new_df], ignore_index=True)
    else: updated_df = pd.DataFrame(new_data)
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
    return ", ".join(sups) if sups else "N/A", ", ".join(final_recep) if final_recep else "N/A", ", ".join(well) if well else "N/A"

def clean_point_name(p):
    p_str = str(p).upper()
    p_str = re.sub(r'^\d+\.\s*', '', p_str) 
    return re.sub(r'[^A-Z0-9]', '', p_str)

def get_guard_history(staff_name, current_date):
    if not os.path.exists(CSV_FILE): return {}
    df = pd.read_csv(CSV_FILE)
    if "Role" not in df.columns: return {}
    df["DateObj"] = pd.to_datetime(df["Date"], format='%Y-%m-%d', errors='coerce')
    current_date_obj = pd.to_datetime(current_date, format='%Y-%m-%d')

    mask = (df["Staff Name"] == staff_name) & (df["Role"] == "GUARD") & (df["DateObj"] < current_date_obj)
    past_duties = df[mask].copy()
    history = {}
    for _, row in past_duties.iterrows():
        if pd.notna(row["DateObj"]):
            pt_clean = clean_point_name(row["Point"])
            days_ago = (current_date_obj - row["DateObj"]).days
            if pt_clean not in history or days_ago < history[pt_clean]: history[pt_clean] = days_ago
    return history

if check_password():
    TIMEOUT_MINUTES = 5 
    if "last_active" in st.session_state:
        elapsed_time = datetime.now() - st.session_state["last_active"]
        if elapsed_time > timedelta(minutes=TIMEOUT_MINUTES):
            st.session_state["password_correct"] = False; st.session_state["screenshot_mode"] = False
            st.warning("⏱️ Session Expired! (5 நிமிடங்களுக்கு மேல் பயன்படுத்தாததால் சிஸ்டம் லாக் செய்யப்பட்டது)")
            st.rerun()
    st.session_state["last_active"] = datetime.now()
    
    if st.session_state["screenshot_mode"]:
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {display: none;} header {display: none;}
            .stApp {background-color: #f8fafc !important;}
            .roster-card { background: white; border: 2px solid #0f172a; border-radius: 12px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); overflow: hidden;}
            .roster-header { background: #0f172a; color: white; text-align: center; padding: 15px; font-weight: 800; font-size: 18px;}
            .roster-body { padding: 20px;}
            .info-text { font-size: 15px; line-height: 1.6; border-bottom: 2px dashed #e2e8f0; padding-bottom: 10px; margin-bottom: 15px;}
            .roster-table { width: 100%; border-collapse: collapse; font-size: 14px;}
            .roster-table th, .roster-table td { border: 1px solid #cbd5e1; padding: 10px; text-align: left; color: #0f172a !important;}
            .roster-table th { background: #f1f5f9; font-weight: bold; color: #334155 !important;}
            .vacant { color: #dc2626 !important; font-weight: bold; }
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
            .stApp { background: #f8fafc !important; font-family: sans-serif; }
            [data-testid="stSidebar"] { background-color: #0f172a !important; }
            [data-testid="stSidebar"] label { color: #ffffff !important; font-weight: bold !important; }
            .main-header { background: #0f172a; padding: 20px; border-radius: 0 0 20px 20px; color: #f1f5f9; text-align: center; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;}
            .shift-banner { background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56,189,248,0.3); padding: 15px; border-radius: 12px; color: #0f172a; text-align: center; font-size: 20px; font-weight: 800; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .stat-row { display: flex; gap: 10px; margin-bottom: 15px; }
            .stat-card { background: white; padding: 15px; border-radius: 10px; flex: 1; text-align: center; border: 1px solid #e2e8f0; color: #0f172a; box-shadow: 0 2px 4px rgba(0,0,0,0.02);}
            .stat-card small { color: #64748b; font-weight: bold;}
            table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02);}
            th, td { border: 1px solid #e2e8f0; padding: 10px; text-align: left; color: #0f172a !important;}
            th { background-color: #f1f5f9; color: #334155 !important; text-transform: uppercase; font-size: 13px;}
            [data-testid="stMarkdownContainer"] p { color: #0f172a !important; }
            </style>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("<h2 style='text-align: center; color: white;'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 EXIT SYSTEM", use_container_width=True):
        st.session_state["password_correct"] = False; st.rerun()
    st.sidebar.divider()
    
    ist = pytz.timezone('Asia/Kolkata')
    current_time_obj = datetime.now(ist)
    current_time = current_time_obj.strftime("%I:%M %p")
    current_hour = current_time_obj.hour
    today_date = current_time_obj.date()
    current_year = today_date.year
    
    ALLOWED_START_DATE = datetime(current_year, 1, 1).date()
    ALLOWED_END_DATE = datetime(current_year, 12, 31).date() 
    
    if today_date < ALLOWED_START_DATE: default_date = ALLOWED_START_DATE
    elif today_date > ALLOWED_END_DATE: default_date = ALLOWED_END_DATE
    else: default_date = today_date

    selected_date = st.sidebar.date_input("SELECT DATE", value=default_date, min_value=ALLOWED_START_DATE, max_value=ALLOWED_END_DATE)
    
    if 4 <= current_hour < 12: default_shift_index = 0  
    elif 12 <= current_hour < 19: default_shift_index = 1  
    else: default_shift_index = 2  

    target_shift = st.sidebar.selectbox("SELECT SHIFT", ["A Shift", "B Shift", "C Shift"], index=default_shift_index)
    date_str_key = selected_date.strftime("%Y-%m-%d")
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    secret_edit = st.sidebar.checkbox("✏️ EDIT MODE", help="Enable to edit duties manually")
    
    if not st.session_state["screenshot_mode"]:
        st.markdown(f"<div class='main-header'><div>🛡️ MATHALAMPARAI EXECUTIVE</div><div>🕒 {current_time}</div></div>", unsafe_allow_html=True)

    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "SATHYAJOTHY", "MUTHUVADIVU", "MUTHU VADIVU", "SUBHASHINI", "MERLIN NIRMALA", "MERLINNIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "BALA SUBRAMANIAN", "PONMARI", "POULSON"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "DHILIPMOHAN", "RANJITH KUMAR", "RANJITHKUMAR"]
    regular_duty_points = ["1. MAIN GATE-1", "2. SECOND GATE", "3. CAR PARKING", "4. PATROLLING", "5. MAIN GATE-2", "6. DG POWER ROOM", "7. A BLOCK AREA", "8. B BLOCK AREA", "9. C BLOCK AREA", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    dynamic_sheet_name = selected_date.strftime("%B-%Y").upper()
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(dynamic_sheet_name)}"

    try:
        db_df = load_database()
        shift_data = db_df[(db_df["Date"] == date_str_key) & (db_df["Shift"] == target_shift)]
        
        db_already_calculated = not shift_data[shift_data["Role"] == "GUARD"].empty
        db_wellness_list = shift_data[shift_data["Role"] == "WELLNESS"]["Staff Name"].tolist()
        db_wellness = db_wellness_list[0] if db_wellness_list else "VACANT"
        
        with st.spinner("🔄 Checking Live Updates in Sheet..."):
            df_raw = pd.read_csv(url, header=None)
            
        day_str = str(selected_date.day)
        date_col_idx = None
        for r in range(min(15, len(df_raw))):
            for c in range(len(df_raw.columns)):
                if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]: date_col_idx = c; break
            if date_col_idx is not None: break

        sheet_code = target_shift[0]
        staff_on_duty, sups, week_offs, on_leave, general_staff, final_recep_team = [], [], [], [], [], []
        
        if date_col_idx:
            for i in range(len(df_raw)):
                if i > 85: break
                name = str(df_raw.iloc[i, 1]).strip().upper()
                status = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                
                if name and name not in ["NAME", "NAN"]:
                    if status in ["WO", "W/O", "OFF"]: week_offs.append(name)
                    elif status in ["L", "LEAVE"]: on_leave.append(name)
                    elif status in ["G", "GEN", "GENERAL"] and target_shift == "A Shift":
                        if any(s in name for s in supervisors_pool): sups.append(f"{name} (GEN)") 
                        else: general_staff.append(name)
                    elif status == sheet_code: 
                        if any(s in name for s in supervisors_pool): sups.append(name)
                        else: staff_on_duty.append({'id': i, 'name': name})

        # --- THE FIX: SMART MISMATCH DETECTOR LAUNCHED ---
        current_sheet_leaves = set(week_offs + on_leave)
        
        db_active_names = set(shift_data[shift_data["Role"].isin(["GUARD", "WELLNESS", "RECEPTION", "SUPERVISOR"])]["Staff Name"].tolist())
        db_leave_names = set(shift_data[shift_data["Role"].isin(["WO", "LEAVE"])]["Staff Name"].tolist())
        
        db_active_names = {n.replace(" (GEN)", "").strip() for n in db_active_names if n != "VACANT"}
        db_leave_names = {n.replace(" (GEN)", "").strip() for n in db_leave_names}
        
        sheet_working_names = {s['name'] for s in staff_on_duty} | set(general_staff)
        for s in sups: sheet_working_names.add(s.replace(" (GEN)", "").strip())

        # Smart Checks
        anyone_went_on_leave = any(name in current_sheet_leaves for name in db_active_names)
        anyone_returned_from_leave = any(name in sheet_working_names for name in db_leave_names)
        
        # Sync ONLY if database is empty OR if someone's actual attendance state changed in the Google Sheet
        sync_needed = not db_already_calculated or anyone_went_on_leave or anyone_returned_from_leave

        if not sync_needed:
            if not secret_edit and not st.session_state["screenshot_mode"]: 
                st.success("🔒 SYSTEM LOCKED: Showing Saved Roster")
            
            sups_text, recep_text, wellness_text = get_role_summary(date_str_key, target_shift)
            wo_names = ", ".join(week_offs) if week_offs else "NONE"
            ol_names = ", ".join(on_leave) if on_leave else "NONE"
            
            guard_df = shift_data[shift_data["Role"] == "GUARD"].copy()
            
            if db_wellness != "VACANT" and db_wellness != "N/A":
                wellness_row = pd.DataFrame([{"Point": "WELLNESS", "Staff Name": db_wellness}])
                guard_df = pd.concat([guard_df, wellness_row], ignore_index=True)
            elif secret_edit:
                 wellness_row = pd.DataFrame([{"Point": "WELLNESS", "Staff Name": "VACANT"}])
                 guard_df = pd.concat([guard_df, wellness_row], ignore_index=True)
            
            point_order = {p: i for i, p in enumerate(regular_duty_points)}
            def sort_key(pt):
                if pt == "WELLNESS": return -1 
                if pt == "RECEPTION RELIEVER": return 0
                if "EXTRA" in str(pt):
                    try: return 100 + int(str(pt).split('-')[1].split('.')[0])
                    except: return 199
                return point_order.get(pt, 200)
            
            guard_df["sort_val"] = guard_df["Point"].apply(sort_key)
            df_display = guard_df.sort_values("sort_val")[["Point", "Staff Name"]]
            
        else:
            if db_already_calculated and not st.session_state["screenshot_mode"]:
                st.warning("🔄 Google Sheet Attendance Changes Detected! Auto-Updating and Re-calculating...")

            specialist_present = next((s for s in staff_on_duty if any(w.replace(" ","") in s['name'].replace(" ","") for w in wellness_specialists)), None)
            regular_recep_present = [s for s in staff_on_duty if any(r.replace(" ","") in s['name'].replace(" ","") for r in receptionists_pool)]
            guards_pool = [s for s in staff_on_duty if s not in regular_recep_present and (not specialist_present or s['name'] != specialist_present['name'])]

            wellness = "VACANT"
            if specialist_present: 
                wellness = specialist_present['name']
            elif guards_pool:
                day_of_year = selected_date.timetuple().tm_yday
                guard_index_for_wellness = day_of_year % len(guards_pool)
                wellness = guards_pool.pop(guard_index_for_wellness)['name']

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
            
            for guard in guards_pool:
                g_name = guard['name']
                history_map[g_name] = get_guard_history(g_name, date_str_key)
                unassigned_guards.append(guard)

            if unassigned_guards:
                def assign_point_centric(guards_list, pts_list, target_ban=7):
                    for current_ban in range(target_ban, -1, -1):
                        def backtrack(rem_pts, rem_guards):
                            if not rem_pts or not rem_guards: return {}
                            curr_pt = rem_pts[0]
                            eligible_guards = []
                            for g in rem_guards:
                                gn = g['name']
                                days_ago = history_map.get(gn, {}).get(clean_point_name(curr_pt), 999)
                                if days_ago > current_ban: eligible_guards.append((g, days_ago))
                            if not eligible_guards: return None 
                            eligible_guards.sort(key=lambda x: x[1], reverse=True)
                            top_candidates = [eg[0] for eg in eligible_guards[:3]]
                            random.shuffle(top_candidates)
                            for chosen_g in top_candidates:
                                next_pts = rem_pts[1:]
                                next_guards = [g for g in rem_guards if g['name'] != chosen_g['name']]
                                res = backtrack(next_pts, next_guards)
                                if res is not None:
                                    res[chosen_g['name']] = curr_pt 
                                    return res
                            return None 
                        shuffled_pts = list(pts_list)
                        random.shuffle(shuffled_pts)
                        solution = backtrack(shuffled_pts, guards_list)
                        if solution is not None: return solution
                    emergency = {}
                    for i, g in enumerate(guards_list):
                        if i < len(pts_list): emergency[g['name']] = pts_list[i]
                    return emergency
                
                strict_solution = assign_point_centric(unassigned_guards, available_today, target_ban=7)
                final_assignments.update(strict_solution)

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
            
            if wellness != "VACANT": rot_data.append({"Point": "WELLNESS", "Staff Name": wellness})
            elif secret_edit: rot_data.append({"Point": "WELLNESS", "Staff Name": "VACANT"})
                
            point_order = {p: i for i, p in enumerate(current_duty_points)}
            def sort_key(pt):
                if pt == "WELLNESS": return -1
                if pt == "RECEPTION RELIEVER": return 0
                if "EXTRA" in str(pt):
                    try: return 100 + int(str(pt).split('-')[1].split('.')[0])
                    except: return 199
                return point_order.get(pt, 200)

            rot_data.sort(key=lambda x: sort_key(x["Point"]))
            df_display = pd.DataFrame(rot_data)
            
            sups_text, recep_text, wellness_text = get_role_summary(date_str_key, target_shift)
            wo_names = ", ".join(week_offs) if week_offs else "NONE"
            ol_names = ", ".join(on_leave) if on_leave else "NONE"

        if st.session_state["screenshot_mode"]:
            html_rows = ""
            for _, row in df_display.iterrows():
                if row['Point'] != "WELLNESS":
                    name = row['Staff Name']
                    style_class = "vacant" if name == "VACANT" else ("extra" if "EXTRA" in row['Point'] else "")
                    html_rows += f"<tr><td>{row['Point']}</td><td class='{style_class}'>{name}</td></tr>"
            card_html = f"""
            <div class="roster-card">
                <div class="roster-header">🛡️ MATHALAMPARAI ROSTER <br><span style="font-size: 15px; font-weight: normal;">{selected_date.strftime("%d %b %Y")} | {target_shift}</span></div>
                <div class="roster-body"><div class="info-text"><b>👨‍💼 Supervisor:</b> {sups_text}<br><b>👩‍💼 Reception:</b> {recep_text}<br><b>⚕️ Wellness:</b> {wellness_text}</div>
                    <table class="roster-table"><tr><th>📍 Duty Point</th><th>💂 Assigned Staff</th></tr>{html_rows}</table>
                    <div class="footer-card"><span style="color:#dc2626;">🏖️ Week Off:</span> {wo_names}<br><span style="color:#dc2626;">🏥 On Leave:</span> {ol_names}</div>
                </div></div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
        else:
            st.markdown(f'<div class="shift-banner">📅 {target_shift} - {selected_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            st.markdown(f"""<div class="stat-row">
                <div class="stat-card"><small>SUPERVISOR</small><br><b>{sups_text}</b></div>
                <div class="stat-card"><small>RECEPTION</small><br><b>{recep_text}</b></div>
                <div class="stat-card"><small>WELLNESS</small><br><b>{wellness_text}</b></div>
            </div>""", unsafe_allow_html=True)
            df_display = df_display.reset_index(drop=True)
            df_display.index += 1

            if secret_edit:
                st.warning("⚠️ EDIT MODE ENABLED (God Mode) - You can assign anyone anywhere. 7-Day rule is Bypassed!")
                
                all_history_df = pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else pd.DataFrame(columns=["Staff Name"])
                all_known_staff = all_history_df["Staff Name"].dropna().unique().tolist()
                
                safe_week_offs = week_offs if isinstance(week_offs, list) else []
                safe_on_leave = on_leave if isinstance(on_leave, list) else []
                safe_sups = sups if isinstance(sups, list) else []
                safe_final_recep_team = final_recep_team if isinstance(final_recep_team, list) else []
                safe_staff_on_duty = [s['name'] for s in staff_on_duty] if isinstance(staff_on_duty, list) else []

                sheet_staff = safe_staff_on_duty + safe_week_offs + safe_on_leave + safe_sups + safe_final_recep_team
                combined_pool = list(set(all_known_staff + sheet_staff + df_display["Staff Name"].tolist() + ["VACANT"]))
                combined_pool = [n for n in combined_pool if n not in ["VACANT", "N/A"]]
                dropdown_names = sorted(combined_pool) + ["VACANT"]
                
                edited_df = st.data_editor(df_display, column_config={"Staff Name": st.column_config.SelectboxColumn("ASSIGN STAFF", options=dropdown_names), "Point": st.column_config.Column(disabled=True)}, use_container_width=True, key="data_editor")
                
                if st.button("💾 SAVE CHANGES TO DATABASE", type="primary"):
                    staff_list = edited_df["Staff Name"].tolist()
                    duplicates = []
                    seen = set()
                    for name in staff_list:
                        if name != "VACANT":
                            if name in seen: duplicates.append(name)
                            seen.add(name)
                    if duplicates:
                        dup_names = ", ".join(set(duplicates))
                        st.error(f"⚠️ பிழை: '{dup_names}' இரண்டு இடங்களில் உள்ளது! ஒருவருக்கு சரியாக மாற்றிவிட்டு சேவ் செய்யவும்.")
                    else:
                        current_db = pd.read_csv(CSV_FILE)
                        mask_keep = ~((current_db["Date"] == date_str_key) & (current_db["Shift"] == target_shift) & (current_db["Role"].isin(["GUARD", "WELLNESS"])))
                        new_db = current_db[mask_keep].copy()
                        new_rows = []
                        for _, row in edited_df.iterrows():
                            if row["Point"] == "WELLNESS" and row["Staff Name"] == "VACANT": continue
                            role_val = "WELLNESS" if row["Point"] == "WELLNESS" else "GUARD"
                            new_rows.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": row["Staff Name"], "Point": row["Point"], "Role": role_val})
                        final_db = pd.concat([new_db, pd.DataFrame(new_rows)], ignore_index=True)
                        final_db.to_csv(CSV_FILE, index=False)
                        st.success("✅ Changes Saved Permanently!")
                        st.rerun()
            else:
                display_only_guards = df_display[df_display["Point"] != "WELLNESS"]
                st.table(display_only_guards)
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("📸 OPEN SCREENSHOT MODE", use_container_width=True, type="primary"): st.session_state["screenshot_mode"] = True; st.rerun()
            
            st.markdown(f"""<div class="stat-row" style='background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 14px; margin-top: 15px;'>
                <span><b style='color:#be123c;'>🏖️ WEEK OFF:</b> <span style='color:#0f172a; font-weight:bold;'>{wo_names}</span></span>
                <span><b style='color:#0369a1;'>🏥 ON LEAVE:</b> <span style='color:#0f172a; font-weight:bold;'>{ol_names}</span></span>
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        if "HTTP Error 400: Bad Request" in str(e): st.error(f"⚠️ Error: Google Sheet-ல் '{dynamic_sheet_name}' என்ற பெயரில் Tab இல்லை! Sheet-ஐ சரிபார்க்கவும்.")
        else: st.error(f"System Error: {e}")
