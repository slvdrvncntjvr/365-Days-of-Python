import requests

API_URL = "http://127.0.0.1:8000/tasks/"

def add_task():
    title = input("Task Title: ")
    description = input("Task Description: ")
    response = requests.post(API_URL, json={"title": title, "description": description})
    print(response.json())

if __name__ == "__main__":
    add_task()
