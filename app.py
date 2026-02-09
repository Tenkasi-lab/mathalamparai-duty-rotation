import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. LOGIN LOGIC (No Hint) ---
def check_password():
    def password_entered():
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
        st.error("❌ Invalid PIN!") 
        return False
    return True

# --- 2. START APP ---
if check_password():
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

    # --- UI Setup ---
    st.set_page_config(page_title="Mathalamparai Duty System", layout="wide")

    st.markdown("""
        <style>
        .stApp { background: #f1f5f9; }
        .shift-header { padding: 12px; border-radius: 10px; color: white; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
        .shift-a { background: #dc2626; }
        .shift-b { background: #2563eb; }
        .shift-c { background: #059669; }
        
        .summary-box { border: 2px solid #000; padding: 12px; margin-bottom: 10px; background-color: #fff; border-radius: 8px; }
        .duty-box { background-color: white; padding: 5px; border-radius: 8px; }
        .leave-box { border: 1px dashed #666; padding: 10px; margin-top: 10px; background-color: #fff; font-size: 14px; }
        
        @media print {
            .no-print, .stButton, [data-testid="stSidebar"] { display: none !important; }
            .main { padding: 0 !important; }
            .stApp { background: white !important; }
            .summary-box { border: 2px solid #000 !important; }
        }
        </style>
        """, unsafe_allow_html=True)

    if st.sidebar.button("🔒 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    selected_date = st.sidebar.date_input("Select Date", datetime.now())
    target_shift = st.sidebar.selectbox("Select Shift", ["A Shift", "B Shift", "C Shift", "All Shifts"])

    col1, col2 = st.columns([1, 1])
    with col1:
        gen_btn = st.button('🚀 Generate Rotation')
    with col2:
        st.components.v1.html('<button style="background: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; width: 100%;" onclick="window.parent.print()">🖨️ Print to PDF</button>', height=50)

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
                    
                    # Logic to pick Receptionists and Wellness
                    wellness_person = next((stf['name'] for stf in shift_data[s] if any(w in stf['name'] for w in wellness_specialists)), "VACANT")
                    recep_list = [stf['name'] for stf in shift_data[s] if any(r in stf['name'] for r in receptionists_pool)][:2]
                    guard_pool = [stf for stf in shift_data[s] if stf['name'] != wellness_person and stf['name'] not in recep_list]

                    rotated = []
                    for idx, point in enumerate(regular_duty_points):
                        staff = guard_pool[idx % len(guard_pool)]['name'] if guard_pool else "VACANT"
                        rotated.append({"Point": point, "Staff Name": staff})
                    
                    # HEADER
                    st.markdown(f'<div class="shift-header shift-{s.lower()}">📅 {s} SHIFT - {selected_date.strftime("%d-%b-%Y")}</div>', unsafe_allow_html=True)
                    
                    # SUMMARY BOX (Supervisor + Reception + Wellness)
                    st.markdown(f"""
                    <div class="summary-box">
                        <b>👨‍💼 Supervisor:</b> {", ".join(supervisors_by_shift[s]) if supervisors_by_shift[s] else "N/A"} | 
                        <b>🛎️ Reception:</b> {", ".join(recep_list) if recep_list else "N/A"} | 
                        <b>🏥 Wellness:</b> {wellness_person}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # MAIN TABLE
                    st.table(pd.DataFrame(rotated))
                    
                    # LEAVE INFO
                    st.markdown(f"""
                    <div class="leave-box">
                        <b>🏖️ Week Off:</b> {", ".join(week_offs) if week_offs else "None"} | 
                        <b>🏥 On Leave:</b> {", ".join(on_leave) if on_leave else "None"}
                    </div>
                    """, unsafe_allow_html=True)
                    st.divider()
            else: st.error("Date column not found!")
        except Exception as e: st.error(f"Error: {e}")
