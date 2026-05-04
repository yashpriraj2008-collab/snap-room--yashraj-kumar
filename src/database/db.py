import streamlit as st
from src.database.config import supabase, supabase_admin, ensure_tables
import bcrypt
import traceback

def init_session_db():
    """Initialize local_db - called from app.py after session_state ready."""
    if "local_db" not in st.session_state:
        st.session_state.local_db = {
            'teachers': [],
            'students': [],
            'subjects': [],
            'subject_students': [],
            'attendance_logs': []
        }
    # Ensure tables exist
    ensure_tables()
    st.success("✅ Local DB & tables initialized")

def _handle_db_error():
    if not st.session_state.offline_error:
        st.session_state.offline_error = True
        st.error("Database connection failed (check internet/VPN). Running in offline mode with mock data.")
    return True

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def check_teacher_exists(username):
    try:
        response = supabase.table("teachers").select("username").eq("username", username).execute()
        return len(response.data) > 0
    except Exception:
        _handle_db_error()
        for t in st.session_state.local_db['teachers']:
            if t['username'] == username:
                return True
        return False

def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    try:
        response = supabase.table("teachers").insert(data).execute()
        if response.data:
            for t in response.data:
                t['teacher_id'] = t['id']
                t['local_id'] = len(st.session_state.local_db['teachers']) + 1
                st.session_state.local_db['teachers'].append(t)
        return response.data
    except Exception:
        _handle_db_error()
        if check_teacher_exists(username):
            return []
        new_id = len(st.session_state.local_db['teachers']) + 1
        data['id'] = new_id
        data['teacher_id'] = new_id
        st.session_state.local_db['teachers'].append(data)
        return [data]

def teacher_login(username, password):
    try:
        response = supabase.table("teachers").select("*").eq("username", username).execute()
        if response.data:
            teacher = response.data[0]
            if check_pass(password, teacher['password']):
                teacher['teacher_id'] = teacher['id']
                return teacher
        return None
    except Exception:
        _handle_db_error()
        for t in st.session_state.local_db['teachers']:
            if t['username'] == username and check_pass(password, t['password']):
                t['teacher_id'] = t['id'] if 'id' in t else t.get('teacher_id')
                return t
        return None

def get_all_students():
    try:
        response = supabase.table('students').select("*").execute()
        return response.data
    except Exception:
        _handle_db_error()
        return st.session_state.local_db['students']

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
    try:
        response = supabase_admin.table('students').insert(data).execute()
        if response.data:
            for s in response.data:
                s['student_id'] = s['id']
            st.session_state.local_db['students'].extend(response.data)
        return response.data
    except Exception:
        print(f"Create student DB error: {traceback.format_exc()}")
        _handle_db_error()
        new_id = len(st.session_state.local_db['students']) + 1
        data['id'] = new_id
        data['student_id'] = new_id
        st.session_state.local_db['students'].append(data)
        return [data]

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    try:
        response = supabase.table("subjects").insert(data).execute()
        st.session_state.local_db['subjects'].extend(response.data or [])
        return response.data
    except Exception:
        _handle_db_error()
        # Offline create
        new_id = len(st.session_state.local_db['subjects']) + 1
        data['id'] = new_id
        st.session_state.local_db['subjects'].append(data)
        return [data]

def get_teacher_subjects(teacher_id):
    try:
        response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
        subjects = response.data or []
    except Exception:
        _handle_db_error()
        subjects = [s for s in st.session_state.local_db['subjects'] if s.get('teacher_id') == teacher_id]

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance)) if attendance else 0
        sub['total_classes'] = unique_sessions
        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)
    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    try:
        response = supabase.table('subject_students').insert(data).execute()
        return response.data
    except Exception:
        _handle_db_error()
        # Offline
        new_id = len(st.session_state.local_db['subject_students']) + 1
        data['id'] = new_id
        st.session_state.local_db['subject_students'].append(data)
        return [data]

def unenroll_student_to_subject(student_id, subject_id):
    try:
        response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
        return response.data
    except Exception:
        _handle_db_error()
        st.session_state.local_db['subject_students'] = [sp for sp in st.session_state.local_db['subject_students'] if not (sp.get('student_id') == student_id and sp.get('subject_id') == subject_id)]
        return []

def get_student_subjects(student_id):
    try:
        response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data
    except Exception:
        _handle_db_error()
        return [sp for sp in st.session_state.local_db['subject_students'] if sp.get('student_id') == student_id]

def get_student_attendance(student_id):
    try:
        response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data
    except Exception:
        _handle_db_error()
        return [log for log in st.session_state.local_db['attendance_logs'] if log.get('student_id') == student_id]

def create_attendance(logs):
    try:
        response = supabase.table('attendance_logs').insert(logs).execute()
        st.session_state.local_db['attendance_logs'].extend(response.data or [])
        return response.data
    except Exception:
        _handle_db_error()
        st.session_state.local_db['attendance_logs'].extend(logs)
        return logs

def get_attendance_for_teacher(teacher_id):
    try:
        response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
        return response.data
    except Exception:
        _handle_db_error()
        return [log for log in st.session_state.local_db['attendance_logs'] if log.get('subject_id') in [s['id'] for s in st.session_state.local_db['subjects'] if s.get('teacher_id') == teacher_id]]

