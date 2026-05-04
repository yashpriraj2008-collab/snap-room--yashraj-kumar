import streamlit as st
from src.database.db import get_all_students, create_student, delete_student

def student_management_tab():
    st.header("👨‍🎓 Student Management")
    
    # Section 1: Add Student
    with st.container(border=True):
        st.subheader("➕ Add New Student")
        name = st.text_input("Student Name", key="add_student_name_input")
        if st.button("➕ Add Student", type="primary"):
            if name.strip():
                try:
                    result = create_student(name.strip())
                    if result:
                        st.success(f"Student '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.warning("Failed to add student. Try again.")
                except Exception:
                    st.warning("Failed to add student. Try again.")
            else:
                st.warning("Please enter a name.")
    
    st.divider()
    
    # Section 2: All Students
    st.subheader("📋 All Students")
    students = get_all_students()
    if students:
        st.caption(f"Total students: {len(students)}")
        for student in students:
            col1, col2 = st.columns([3,1])
            with col1:
                st.write(f"**{student.get('name', 'Unknown')}** (ID: {student['student_id']})")
            with col2:
                if st.button("🗑️", key=f"del_student_{student['student_id']}"):
                    if delete_student(student['student_id']):
                        st.success("Student deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete student.")
    else:
        st.info("No students found.")


