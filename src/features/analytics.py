import streamlit as st
import plotly.express as px
import pandas as pd
from src.database.db import get_all_students, get_manual_attendance_logs

def analytics_tab():
    st.header("📊 Analytics")
    
    students = get_all_students()
    logs = get_manual_attendance_logs()
    
    if not logs:
        st.info("No attendance logs available yet.")
        return
    
    # Metric cards
    total_students = len(students)
    total_records = len(logs)
    present_count = sum(1 for log in logs if log.get('is_present') or log.get('status') == 'Present')
    attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Total Records", total_records)
    col3.metric("Attendance Rate", f"{attendance_rate:.1f}%")
    
    # DataFrame
    data = []
    for log in logs:
        student_info = log.get('students') or {}
        name = student_info.get('name', 'Unknown') if isinstance(student_info, dict) else 'Unknown'
        status = log.get('status') or ('Present' if log.get('is_present') else 'Absent')
        date = log.get('date') or log.get('timestamp', '').split('T')[0]
        data.append({'Name': name, 'Date': date, 'Status': status})
    
    df = pd.DataFrame(data)
    df = df.sort_values('Date', ascending=False)
    st.dataframe(df, use_container_width=True)
    
    # Charts
    if not df.empty:
        # Attendance % per student
        student_stats = df.groupby('Name')['Status'].apply(lambda x: (x == 'Present').mean() * 100).reset_index(name='Attendance %')
        fig_bar = px.bar(student_stats, x='Name', y='Attendance %', title="Attendance % per Student", color_continuous_scale='Blues', range_y=[0,100])
        fig_bar.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Pie chart
        status_counts = df['Status'].value_counts()
        fig_pie = px.pie(values=status_counts.values, names=status_counts.index, title="Present vs Absent", color_discrete_map={'Present': '#5865F2', 'Absent': '#EB459E'})
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

