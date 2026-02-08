import streamlit as st
import pandas as pd
import random
from datetime import datetime
import urllib.parse

# Google Sheet Settings
sheet_id = "1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ"
sheet_name = "FEBRUARY-2026" 
encoded_sheet_name = urllib.parse.quote(sheet_name)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

# Permanent Pools
receptionists_pool = ["KAVITHA", "SATHYA JOTHY", "MUTHUVADIVU", "SUBHASHINI", "MERLIN NIRMALA", "PETCHIYAMMAL"]
wellness_specialists = ["BALASUBRAMANIAN", "PONMARI", "POULSON"]

# Regular Points
regular_duty_points = [
    "1. MAIN GATE-1", "2. MAIN GATE-2", "3. SECOND GATE", "4. CAR PARKING", 
    "5. PATROLLING", "6. DG POWER ROOM", "7. C BLOCK", "8. B BLOCK", 
    "9. A BLOCK", "10. CAR PARKING ENTRANCE", "11. CIVIL MAIN GATE", "12. NEW CANTEEN"
]

def generate_shift_rotation(staff_with_ids, is_weekend):
    if not staff_with_ids: return [], [], "NOT ASSIGNED"
    
    random.shuffle(staff_with_ids)
    
    # 1. Wellness Duty Logic
    wellness_person = None
    present_specialists = [s for s in staff_with_ids if any(sp in s['name'] for sp in wellness_specialists)]
    
    if present_specialists:
        wellness_person = present_specialists[0]
    else:
        potential_guards = [s for s in staff_with_ids if not any(r in s['name'] for r in receptionists_pool)]
        if potential_guards:
            wellness_person = random.choice(potential_guards)
            
    pool_after_wellness = [s for s in staff_with_ids if s['id'] != (wellness_person['id'] if wellness_person else -1)]

    # 2. Reception Logic
    needed_reception = 1 if is_weekend else 2
    reception_pool = [s for s in pool_after_wellness if any(r in s['name'] for r in receptionists_pool)]
    
    selected_reception = random.sample(reception_pool, min(needed_reception, len(reception_pool)))
    
    # Pool after taking receptionists
    final_guard_pool = [s for s in pool_after_wellness if s not in selected_reception]
    random.shuffle(final_guard_pool)

    # 3. Sequential Vacant Logic
    staff_count = len(final_guard_pool)
    point_assignments = {}
    
    # Order of points to fill (priority points first, then low priority)
    # 1. First, we remove the lowest priorities from the fill list
    all_points = regular_duty_points.copy()
    
    # Points to fill in order of importance
    # Important points stay first, 3 and 9 go to the end
    priority_order = [p for p in all_points if p not in ["
