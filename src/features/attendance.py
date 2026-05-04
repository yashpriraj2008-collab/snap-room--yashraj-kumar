import streamlit as st
from src.database.db import get_all_students, get_attendance_for_date, mark_attendance_manual

def manual_attendance_tab():
    st.header("📋 Mark Attendance")
    
    students = get_all_students()
    if not students:
        st.warning("No students found. Add students in Students tab first.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        attend_date = st.date_input("Date", value=st.date_util.date.today(), key="attend_date")
    with col2:
        student_names = [s['name'] for s in students]
        selected_student_name = st.selectbox("Select Student", student_names, key="attend_student")
    
    selected_student_id = next((s['student_id'] for s in students if s['name'] == selected_student_name), None)
    
    existing = get_attendance_for_date(attend_date)
    already_marked = any(log['student_id'] == selected_student_id for log in existing)
    
    if already_marked:
        status = next((log['status'] for log in existing if log['student_id'] == selected_student_id), 'Unknown')
        st.info(f"Student '{selected_student_name}' already marked as **{status}** for {attend_date}")
        col1, col2 = st.columns(2)
        col1.button("✅ Present", disabled=True)
        col2.button("❌ Absent", disabled=True, type="secondary")
    else:
        col1, col2 = st.columns(2)
        if col1.button("✅ Mark Present", type="primary"):
            mark_attendance_manual(selected_student_id, "Present", attend_date)
            st.success("Marked present!")
            st.rerun()
        if col2.button("❌ Mark Absent", type="secondary"):
            mark_attendance_manual(selected_student_id, "Absent", attend_date)
            st.success("Marked absent!")
            st.rerun()
    
    st.divider()
    st.subheader("📄 Today's Attendance")
    todays_logs = get_attendance_for_date(st.date_util.date.today())
    if todays_logs:
        for log in todays_logs:
            student_name = log.get('students', {}).get('name', 'Unknown') if isinstance(log.get('students'), dict) else 'Unknown'
            status = log.get('status') or ('Present' if log.get('is_present') else 'Absent')
            icon = "✅" if status == "Present" else "❌"
            st.write(f"{icon} **{student_name}** - {status}")
    else:
        st.info("No attendance marked today.")

