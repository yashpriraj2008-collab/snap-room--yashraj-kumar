import streamlit as st

# CENTRALIZED SESSION STATE INITIALIZATION - FIXES AttributeError
def init_session_state():
    """Initialize ALL session_state keys used across the app."""
    keys = {
        'login_type': None,
        'is_logged_in': False,
        'user_role': None,
        'teacher_data': None,
        'student_data': None,
        'offline_error': False,
        'local_db': {
            'teachers': [],
            'students': [],
            'subjects': [],
            'subject_students': [],
            'attendance_logs': []
        },
        'current_teacher_tab': 'take_attendance',
        'teacher_login_type': 'login',
        'attendance_images': [],
        'photo_tab': 'camera',
        'voice_attendance_results': None,
        # Add more as discovered
    }
    for key, default in keys.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Initialize before any imports/screens
init_session_state()

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.database.db import init_session_db  # New func
from src.database.config import test_connection

# Test Supabase connection & create tables if needed
def setup_db():
    if test_connection():
        st.success("✅ Supabase connected successfully!")
        init_session_db()  # Sync local_db if online
    else:
        st.session_state.offline_error = True
        st.error("⚠️ Supabase offline - using local mock data")

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )
    
    setup_db()
    
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()

