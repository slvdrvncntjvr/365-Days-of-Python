import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/tasks/"

st.title("PyProd AI - Your Productivity Assistant")

task_title = st.text_input("Enter a task")
task_description = st.text_area("Task Description")

if st.button("Add Task"):
    response = requests.post(API_URL, json={"title": task_title, "description": task_description})
    st.success(response.json()["message"])

st.write("Upcoming Features: Task Analytics, AI Recommendations")
