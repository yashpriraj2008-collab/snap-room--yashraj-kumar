import streamlit as st
from src.database.db import get_all_students, get_manual_attendance_logs

def _safe_summary():
    try:
        students = get_all_students()
        logs = get_manual_attendance_logs()
        total_students = len(students)
        total_records = len(logs)
        present = sum(1 for log in logs if (log or {}).get('is_present') or (log or {}).get('status') == 'Present')
        absent = total_records - present
        rate = (present / total_records * 100) if total_records > 0 else 0
        
        summary = f"""
**Attendance Summary:**
- Total Students: {total_students}
- Total Records: {total_records}
- Present: {present}
- Absent: {absent}
- Rate: {rate:.1f}%

**Per Student Breakdown:**
"""
        for student in students:
            student_logs = [log for log in logs if (log or {}).get('student_id') == student['student_id']]
            student_present = sum(1 for log in student_logs if (log or {}).get('is_present') or (log or {}).get('status') == 'Present')
            student_rate = (student_present / len(student_logs) * 100) if student_logs else 0
            summary += f"- {student['name']}: {student_rate:.1f}% ({student_present}/{len(student_logs)})\\n"
        return summary
    except Exception:
        return "**Error:** Unable to generate summary."

def chatbot_tab():
    st.header("🤖 Attendance Chatbot")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about attendance..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        if any(word in prompt.lower() for word in ["hi", "hello", "hey"]):
            response = "Hello! I can help with attendance questions like number of students or attendance summary."
        elif "help" in prompt.lower():
            response = """
**What I can do:**
- List all students or count them
- Show attendance summary and rates
- Per student attendance
- Today's attendance
            """
        elif any(word in prompt.lower() for word in ["student", "list", "how many"]):
            students = get_all_students()
            if students:
                names = ", ".join(s['name'] for s in students)
                response = f"There are {len(students)} students:\\n{names}"
            else:
                response = "No students registered yet."
        elif any(word in prompt.lower() for word in ["attendance", "present", "absent", "rate", "summary", "report"]):
            response = _safe_summary()
        else:
            response = "I can only answer attendance related questions. Try 'students', 'attendance summary', or 'help'."
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Clear chat
    if st.session_state.chat_history and st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
