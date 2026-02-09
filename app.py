import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. PREMIUM LOGIN LOGIC ---
def check_password():
    def password_entered():
        correct_pin = datetime.now().strftime("%d%m")
        if st.session_state["password"] == correct_pin:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h1 style='color: #1e293b; font-size: 40px;'>🛡️</h1>
                <h2 style='color: #1e293b; font-family: sans-serif;'>Mathalamparai Duty System</h2>
                <p style='color: #64748b;'>Secure Access Portal</p>
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Enter Daily PIN (DDMM)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ Access Denied: Invalid PIN")
        st.rerun()
    return True

# --- 2. START APP ---
if check_password():
    # Google Sheet Settings
    sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
    sheet_name = "FEBRUARY-2026" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"

    receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
    wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]
    supervisors_pool = ["INDIRAJITH", "DHILIP MOHAN", "RANJITH KUMAR"]
    
    regular_duty_points = [
        "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
        "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
        "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
    ]

    st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

    # --- ADVANCED PREMIUM CSS ---
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%); }
        [data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #1e293b; }
        
        /* Shift Header - Modern Gradient */
        .shift-header { 
            padding: 20px; border-radius: 15px; color: white; text-align: center; 
            font-size: 26px; font-weight: bold; margin-bottom: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .shift-a { background: linear-gradient(90deg, #e11d48, #fb7185); }
        .shift-b { background: linear-gradient(90deg, #2563eb, #60a5fa); }
        .shift-c { background: linear-gradient(90deg, #059669, #34d399); }
        
        /* Summary Banner */
        .summary-banner {
            background: white; padding: 15px; border-radius: 12px;
            border: 1px solid #e2e8f0; margin-bottom: 15px;
            display: flex; justify-content: space-around; align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        
        /* Remove Table Scroll */
        div[data-testid="stTable"] table { width: 100% !important; font-size: 16px !important; }
        
        @media print {
            .no-print, .stButton, [data-testid="stSidebar"] { display: none !important; }
            .stApp { background: white !important; }
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar
    if st.sidebar.button("🔒 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    selected_date = st.sidebar.date_input("Select Date", datetime.now())
    target_shift = st.sidebar.selectbox("Select Shift", ["A Shift", "B Shift", "C Shift", "All Shifts"])

    st.markdown("<h2 style='color: #1e293b;'>🛡️ Mathalamparai Duty Dashboard</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        gen_btn = st.button('🚀 Refresh Duty Rotation')
    with col2:
        st.components.v1.html('<button style="background: #0f172a; color: white; padding: 12px 24px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" onclick="window.parent.print()">🖨️ Print Final Roster (PDF)</button>', height=60)

    if gen_btn:
        try:
            df_raw = pd.read_csv(url, header=None)
            day_str = str(selected_date.day)
            
            date_col_idx = None
            for r in range(min(15, len(df_raw))):
                for c in range(len(df_raw.columns)):
                    if str(df_raw.iloc[r, c]).strip() in [day_str, day_str.zfill(2)]:
                        date_col_idx = c
                        break
                if date_col_idx is not None: break

            if date_col_idx:
                shift_data, supervisors_by_shift = {"A":[], "B":[], "C":[]}, {"A":[], "B":[], "C":[]}
                week_offs, on_leave = [], []

                for i in range(len(df_raw)):
                    if i > 85: break
                    name = str(df_raw.iloc[i, 1]).strip().upper()
                    status = str(df_raw.iloc[i, date_col_idx]).strip().upper().replace(" ", "")
                    
                    if name and name not in ["NAME", "NAN"]:
                        if status in ["WO", "W/O", "OFF"]: week_offs.append(name)
                        elif status in ["L", "LEAVE"]: on_leave.append(name)
                        elif any(sup in name for sup in supervisors_pool):
                            if status in ["A", "B", "C"]: supervisors_by_shift[status].append(name)
                        elif status in ["A", "B", "C"]: shift_data[status].append({'id': i, 'name': name})

                display_list = ["A", "B", "C"] if target_shift == "All Shifts" else [target_shift[0]]

                for s in display_list:
                    if not shift_data[s]: continue
                    
                    wellness_person = next((stf['name'] for stf in shift_data[s] if any(w in stf['name'] for w in wellness_specialists)), "VACANT")
                    recep_list = [stf['name'] for stf in shift_data[s] if any(r in stf['name'] for r in receptionists_pool)][:2]
                    guard_pool = [stf for stf in shift_data[s] if stf['name'] != wellness_person and stf['name'] not in recep_list]

                    rotated = [{"Point": p, "Staff Name": (guard_pool[idx % len(guard_pool)]['name'] if guard_pool else "VACANT")} for idx, p in enumerate(regular_duty_points)]
                    
                    # RENDER
                    st.markdown(f'<div class="shift-header shift-{s.lower()}">📅 {s} SHIFT - {selected_date.strftime("%d-%b-%Y")}</div>', unsafe_allow_html=True)
                    
                    # Modern Banner for Top Staff
                    st.markdown(f"""
                        <div class="summary-banner">
                            <div><b>👨‍💼 Supervisor:</b> {", ".join(supervisors_by_shift[s]) if supervisors_by_shift[s] else "N/A"}</div>
                            <div><b>🛎️ Reception:</b> {", ".join(recep_list) if recep_list else "N/A"}</div>
                            <div><b>🏥 Wellness:</b> {wellness_person}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.table(pd.DataFrame(rotated))
                    
                    # Bottom Leave Info
                    st.markdown(f"""
                        <div style='background: white; padding: 10px; border-radius: 8px; border-left: 5px solid #64748b;'>
                            <small>🏖️ <b>Week Off:</b> {", ".join(week_offs) if week_offs else "None"} | 🏥 <b>Leave:</b> {", ".join(on_leave) if on_leave else "None"}</small>
                        </div>
                    """, unsafe_allow_html=True)
                    st.divider()
            else: st.error("Sheet-la date kandupudikka mudiyala!")
        except Exception as e: st.error(f"Error: {e}")
