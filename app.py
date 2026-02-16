import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import pytz
import os

# --- 1. CONFIGURATION ---
CSV_FILE = "duty_database.csv"
sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
sheet_name = "FEBRUARY-2026" 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"

# --- 2. PASSWORD LOGIC ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

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
        
        # Remove existing entries for this shift
        date_str = new_data[0]["Date"]
        shift_str = new_data[0]["Shift"]
        history_df = history_df[~((history_df["Date"] == date_str) & (history_df["Shift"] == shift_str))]
        
        new_df = pd.DataFrame(new_data)
        updated_df = pd.concat([history_df, new_df], ignore_index=True)
    else:
        updated_df = pd.DataFrame(new_data)
    
    updated_df.to_csv(CSV_FILE, index=False)
    return updated_df

def update_database_entry(date_str, shift_str, staff_name, new_point):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # Find row by Date/Shift/Name
        mask = (df["Date"] == date_str) & (df["Shift"] == shift_str) & (df["Staff Name"] == staff_name)
        if not df.loc[mask].empty:
            df.loc[mask, "Point"] = new_point
            # If they were edited into a Reception Reliever spot, ensure Role is GUARD so it stays visible
            if new_point == "RECEPTION RELIEVER":
                df.loc[mask, "Role"] = "GUARD"
            df.to_csv(CSV_FILE, index=False)
            return True
    return False

def get_blocked_points(staff_name, current_date):
    if not os.path.exists(CSV_FILE): return []
    df = pd.read_csv(CSV_FILE)
    if "Role" not in df.columns: return []
    
    df["DateObj"] = pd.to_datetime(df["Date"])
    current_date_obj = pd.to_datetime(current_date)
    
    mask = (df["Staff Name"] == staff_name) & \
           (df["DateObj"] < current_date_obj) & \
           (df["DateObj"] >= (current_date_obj - timedelta(days=5)))
    
    return df.loc[mask, "Point"].tolist()

def get_role_summary(date_str, shift_str):
    if not os.path.exists(CSV_FILE): return "N/A", "N/A", "N/A"
    
    df = pd.read_csv(CSV_FILE)
    if "Role" not in df.columns: return "N/A", "N/A", "N/A"
    
    mask = (df["Date"] == date_str) & (df["Shift"] == shift_str)
    shift_df = df[mask]
    
    if shift_df.empty: return "N/A", "N/A", "N/A"

    sups = shift_df[shift_df["Role"] == "SUPERVISOR"]["Staff Name"].tolist()
    
    # Reception: Include regular receptionists AND the Guard acting as Reliever
    recep = shift_df[shift_df["Role"] == "RECEPTION"]["Staff Name"].tolist()
    recep_reliever = shift_df[shift_df["Point"] == "RECEPTION RELIEVER"]["Staff Name"].tolist()
    final_recep = recep + recep_reliever
    
    well = shift_df[shift_df["Role"] == "WELLNESS"]["Staff Name"].tolist()
    
    return ", ".join(sups) if sups else "N/A", \
           ", ".join(final_recep) if final_recep else "N/A", \
           ", ".join(well) if well else "N/A"

if check_password():
    st.set_page_config(page_title="Mathalamparai Executive", layout="wide")
    
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #0f172a !important; }
        [data-testid="stSidebar"] label { color: #ffffff !important; font-weight: bold !important; }
        .main-header { background: #0f172a; padding: 20px; border-radius: 0 0 20px 20px; color: #f1f5f9; text-align: center; display: flex; justify-content: space-between; align-items: center; }
        .shift-banner { padding: 15px; border-radius: 12px; color: white; text-align: center; font-size: 24px; font-weight: 800; margin: 15px 0; }
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
    
    selected_date = st.sidebar.date_input("SELECT DATE", datetime.now())
    target_shift = st.sidebar.selectbox("SELECT SHIFT", ["A Shift", "B Shift", "C Shift"])
    st.sidebar.markdown("<br>"*2, unsafe_allow_html=True)
    secret_edit = st.sidebar.checkbox("✏️ EDIT MODE", help="Enable to edit duties manually")
    
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%I:%M %p")
    st.markdown(f"<div class='main-header'><div>🛡️ PERMANENT DUTY SYSTEM</div><div>🕒 {current_time}</div></div>", unsafe_allow_html=True)

    # --- POOLS ---
    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
    regular_duty_points = ["1. MAIN GATE-1", "2. SECOND GATE", "3. CAR PARKING", "4. PATROLLING", "5. MAIN GATE-2", "6. DG POWER ROOM", "7. A BLOCK AREA", "8. B BLOCK AREA", "9. C BLOCK AREA", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    try:
        db_df = load_database()
        date_str_key = selected_date.strftime("%Y-%m-%d")
        
        shift_data = db_df[(db_df["Date"] == date_str_key) & (db_df["Shift"] == target_shift)]
        
        has_guards = not shift_data[shift_data["Role"] == "GUARD"].empty
        has_details = not shift_data[shift_data["Role"].isin(["WO", "LEAVE", "SUPERVISOR"])].empty
        should_calculate = not has_guards or (has_guards and not has_details)

        if not should_calculate:
            # --- DISPLAY FROM DB ---
            if not secret_edit: st.success("✅ LOADED FROM DATABASE")
            
            sups_text, recep_text, wellness_text = get_role_summary(date_str_key, target_shift)
            
            wo = shift_data[shift_data["Role"] == "WO"]["Staff Name"].tolist()
            le = shift_data[shift_data["Role"] == "LEAVE"]["Staff Name"].tolist()
            wo_names = ", ".join(wo) if wo else "NONE"
            ol_names = ", ".join(le) if le else "NONE"
            
            guard_df = shift_data[shift_data["Role"] == "GUARD"].copy()
            
            point_order = {p: i for i, p in enumerate(regular_duty_points)}
            def sort_key(pt):
                if pt == "RECEPTION RELIEVER": return 0 # Show reliever at top
                return point_order.get(pt, 100 + int(pt.split('-')[1]) if "EXTRA" in pt else 200)
            
            guard_df["sort_val"] = guard_df["Point"].apply(sort_key)
            df_display = guard_df.sort_values("sort_val")[["Point", "Staff Name"]]
            
        else:
            # --- CALCULATE NEW ---
            with st.spinner("Fetching Google Sheet & Calculating..."):
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
                            elif status == shift_code: 
                                if any(s in name for s in supervisors_pool): sups.append(name)
                                else: staff_on_duty.append({'id': i, 'name': name})

                    specialist_present = next((s for s in staff_on_duty if any(w in s['name'] for w in wellness_specialists)), None)
                    regular_recep_present = [s for s in staff_on_duty if any(r in s['name'] for r in receptionists_pool)]
                    guards_pool = [s for s in staff_on_duty if s not in regular_recep_present and (not specialist_present or s['name'] != specialist_present['name'])]

                    wellness = "VACANT"
                    if specialist_present: wellness = specialist_present['name']
                    elif selected_date.weekday() == 1 and guards_pool:
                        week_num = selected_date.isocalendar()[1]
                        wellness = guards_pool.pop(week_num % len(guards_pool))['name']

                    final_recep_team = [r['name'] for r in regular_recep_present]
                    # --- FIXED RECEPTION RELIEVER LOGIC ---
                    reception_reliever_name = None
                    if selected_date.weekday() == 5 and guards_pool:
                        week_num = selected_date.isocalendar()[1]
                        # Don't add to final_recep_team, keep separate to be in Table
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
                    for guard in guards_pool:
                        history = get_blocked_points(guard['name'], date_str_key)
                        assigned = False
                        for point in available_today:
                            is_blocked = False
                            for blocked_pt in history:
                                if len(blocked_pt) > 4 and (blocked_pt in point or point in blocked_pt):
                                    is_blocked = True
                            if not is_blocked:
                                final_assignments[guard['name']] = point
                                available_today.remove(point)
                                assigned = True
                                break
                        if not assigned and available_today:
                            final_assignments[guard['name']] = available_today.pop(0)

                    # --- SAVE DATA ---
                    rot_data = []
                    save_list = []
                    
                    for name, point in final_assignments.items():
                        rot_data.append({"Point": point, "Staff Name": name})
                        save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": name, "Point": point, "Role": "GUARD"})
                    
                    # Add Reception Reliever as a GUARD so they appear in Table
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

                    for vac in points_forced_vacant:
                        rot_data.append({"Point": vac, "Staff Name": "VACANT"})
                        save_list.append({"Date": date_str_key, "Shift": target_shift, "Staff Name": "VACANT", "Point": vac, "Role": "GUARD"})
                    
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

        # --- RENDER UI ---
        st.markdown(f'<div class="shift-banner {target_shift[0].lower()}-shift">📅 {target_shift} - {selected_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""<div class="stat-row">
            <div class="stat-card"><small>SUPERVISOR</small><br><b>{sups_text}</b></div>
            <div class="stat-card"><small>RECEPTION</small><br><b>{recep_text}</b></div>
            <div class="stat-card"><small>WELLNESS</small><br><b>{wellness_text}</b></div>
        </div>""", unsafe_allow_html=True)

        if secret_edit:
            st.warning("⚠️ EDIT MODE ENABLED - Changes are saved permanently!")
            dropdown_names = sorted(df_display["Staff Name"].unique().tolist() + 
                                  shift_data[shift_data["Role"].isin(["WO", "LEAVE", "SUPERVISOR"])]["Staff Name"].tolist() + 
                                  ["VACANT"])
            
            edited_df = st.data_editor(
                df_display, 
                column_config={
                    "Staff Name": st.column_config.SelectboxColumn("ASSIGN STAFF", options=dropdown_names)
                }, 
                use_container_width=True,
                key="data_editor",
                hide_index=True
            )
            
            if st.button("💾 SAVE CHANGES TO DATABASE", type="primary"):
                for index, row in edited_df.iterrows():
                    update_database_entry(date_str_key, target_shift, row["Staff Name"], row["Point"])
                
                # RE-SAVE strategy (Compact)
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
        
        st.markdown(f"""<div class="footer-info" style='background: white; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 14px; margin-top: 15px;'>
            <span><b style='color:#1e3a8a;'>🏖️ WEEK OFF:</b> <span style='color:#dc2626; font-weight:bold;'>{wo_names}</span></span>
            <span><b style='color:#1e3a8a;'>🏥 ON LEAVE:</b> <span style='color:#dc2626; font-weight:bold;'>{ol_names}</span></span>
        </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"System Error: {e}")
