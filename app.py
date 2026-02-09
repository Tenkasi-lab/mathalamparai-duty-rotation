import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. PREMIUM LOGIN & LOGOUT LOGIC ---
def check_password():
    # Initial state setup
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    def password_entered():
        # PIN is Today's Date (e.g., 0902)
        if st.session_state["password"] == datetime.now().strftime("%d%m"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # High-Rich Login Page Design
        st.markdown("""
            <style>
            .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
            .login-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                padding: 40px; border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center; color: white;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }
            </style>
            <div class='login-card'>
                <h1 style='font-size: 50px; margin-bottom: 0;'>🛡️</h1>
                <h2 style='font-family: sans-serif; letter-spacing: 2px;'>MATHALAMPARAI</h2>
                <p style='color: #94a3b8; margin-bottom: 30px;'>EXECUTIVE DUTY PORTAL</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.text_input("ENTER DAILY PIN", type="password", on_change=password_entered, key="password", help="Enter DDMM format")
            if "password_correct" in st.session_state and not st.session_state["password_correct"]:
                st.error("❌ Access Denied: Invalid Security Pin")
        return False
    return True

# --- 2. START DASHBOARD ---
if check_password():
    # Logout Logic Fix
    def do_logout():
        st.session_state["password_correct"] = False
        st.rerun()

    # Settings
    sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
    sheet_name = "FEBRUARY-2026" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"

    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
    regular_duty_points = ["1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"]

    st.set_page_config(page_title="Mathalamparai Executive", layout="wide")

    # --- ULTRA RICH CSS ---
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 2px solid #334155; }
        
        /* Modern Header Banner */
        .main-header {
            background: #0f172a; padding: 25px; border-radius: 0 0 20px 20px;
            color: #f1f5f9; text-align: center; margin-bottom: 30px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
        
        /* Shift Cards with Rich Glow */
        .shift-banner {
            padding: 20px; border-radius: 15px; color: white; text-align: center;
            font-size: 28px; font-weight: 900; margin-bottom: 20px;
            text-transform: uppercase; letter-spacing: 2px;
        }
        .a-shift { background: linear-gradient(135deg, #be123c, #fb7185); box-shadow: 0 10px 20px -5px rgba(225, 29, 72, 0.4); }
        .b-shift { background: linear-gradient(135deg, #1d4ed8, #60a5fa); box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4); }
        .c-shift { background: linear-gradient(135deg, #047857, #34d399); box-shadow: 0 10px 20px -5px rgba(5, 150, 105, 0.4); }

        /* Summary Dashboard Row */
        .stat-row {
            display: flex; gap: 15px; margin-bottom: 20px; justify-content: space-between;
        }
        .stat-card {
            background: white; padding: 20px; border-radius: 15px; flex: 1;
            border-bottom: 4px solid #334155; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Table Style */
        div[data-testid="stTable"] table { border-radius: 15px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        th { background-color: #1e293b !important; color: white !important; padding: 15px !important; }
        
        @media print { .no-print, .stButton, [data-testid="stSidebar"], .stCheckbox { display: none !important; } }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar Logout
    st.sidebar.markdown("<h3 style='color: white;'>Settings</h3>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 EXIT SYSTEM", on_click=do_logout, use_container_width=True):
        pass

    selected_date = st.sidebar.date_input("SELECT DATE", datetime.now())
    target_shift = st.sidebar.selectbox("SELECT SHIFT", ["A Shift", "B Shift", "C Shift"])
    edit_mode = st.sidebar.toggle("🛠️ ENABLE EDIT MODE")

    # Main Header
    st.markdown("<div class='main-header'><h1>🛡️ MATHALAMPARAI DUTY DASHBOARD</h1></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        gen_btn = st.button('🚀 REFRESH DATA', use_container_width=True)
    with col2:
        st.components.v1.html('<button style="background: #1e293b; color: #facc15; padding: 12px 24px; border-radius: 12px; border: 2px solid #facc15; font-weight: bold; cursor: pointer; width: 100%;" onclick="window.parent.print()">🖨️ EXPORT TO PDF</button>', height=60)

    if gen_btn or 'current_df' in st.session_state:
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

                if gen_btn or 'current_df' not in st.session_state:
                    rot_data = [{"Point": p, "Staff Name": (guards[idx % len(guards)]['name'] if guards else "VACANT")} for idx, p in enumerate(regular_duty_points)]
                    st.session_state.current_df = pd.DataFrame(rot_data)

                # RENDER RICH SHIFT BANNER
                st.markdown(f'<div class="shift-banner {shift_code.lower()}-shift">📅 {target_shift} - {selected_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
                
                # EXECUTIVE STAT CARDS
                st.markdown(f"""
                    <div class="stat-row">
                        <div class="stat-card"><small style='color:#64748b'>SUPERVISOR</small><br><b>{", ".join(sups) if sups else "N/A"}</b></div>
                        <div class="stat-card"><small style='color:#64748b'>RECEPTION</small><br><b>{", ".join(recep) if recep else "N/A"}</b></div>
                        <div class="stat-card"><small style='color:#64748b'>WELLNESS</small><br><b>{wellness}</b></div>
                    </div>
                """, unsafe_allow_html=True)

                if edit_mode:
                    dropdown_names = sorted([s['name'] for s in staff_on_duty] + ["VACANT", "OFF"])
                    edited_df = st.data_editor(st.session_state.current_df, column_config={"Staff Name": st.column_config.SelectboxColumn("ASSIGN STAFF", options=dropdown_names)}, hide_index=True, use_container_width=True)
                    if st.button("💾 SAVE CHANGES"):
                        st.session_state.current_df = edited_df
                        st.success("Duty Roster Updated!"); st.rerun()
                else:
                    st.table(st.session_state.current_df)

                # FOOTER SUMMARY
                st.markdown(f"""<div style='background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top:20px; display: flex; justify-content: space-between;'>
                    <span>🏖️ <b>WEEK OFF:</b> {", ".join(week_offs) if week_offs else "NONE"}</span>
                    <span>🏥 <b>ON LEAVE:</b> {", ".join(on_leave) if on_leave else "NONE"}</span>
                </div>""", unsafe_allow_html=True)
            else: st.error("Database connection issue: Column not found.")
        except Exception as e: st.error(f"System Error: {e}")
