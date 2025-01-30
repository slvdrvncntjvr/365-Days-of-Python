import openai

openai.api_key = "your-openai-api-key"

def analyze_task(task_title):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Analyze the task: {task_title}"}]
    )
    return response['choices'][0]['message']['content']
