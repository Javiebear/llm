# File name: llm.py
# Date: March 26, 2025
# Author: Javier Chung
# Description:

from llama_cpp import Llama
import json
from datetime import datetime, timedelta

MODEL_PATH = "./llama.cpp/models/mistral-7b-v0.1.Q4_0.gguf"
SPECIFIED_LANG = "Make sure the refined goal is in english and keep it focused"
PROMPT_LANG = "The prompt is in english."

def prompt_llm(llm, prompt):
    response_text = ""
    print("Generating response...")
    
    # Initializing a streamed response from the prompt
    stream = llm(
        prompt,
        max_tokens=256,
        stream=True,
        temperature=0.7, # reducing hallucination
        stop=["\n\n", "###"]  # Stopping generation at newline or delimiter
    )
    
    # Generating a stream response
    for response in stream:
        chunk = response["choices"][0]["text"]
        response_text += chunk
        print(chunk, end="", flush=True)
    
    return response_text.strip()

# This is where the main code will run
if __name__ == "__main__":

    try:
        print("Loading model... This may take a few seconds.")
        llm = Llama(model_path=MODEL_PATH, n_gpu_layers=50)

        print("\nModel loaded successfully.\n")

    except Exception as e:
        print(f"Error loading model: {e}")

    # Once the model is loaded, we need to extract data from the user
    print("Welcome to the PPA, the Personal Productivity Assistant!")
    print("My goal is to help you organize your schedule, track your tasks, and provide you with reminders.")

    task_inputs = input("What tasks do you need help with?\nReply: ")

    prompt_retreive_tasks = f"""
    Convert this input into a JSON array of task objects with EXACTLY these fields:
    - task (string)
    - category (string: "exercise", "school", "work", or "other")
    - completed (boolean: false)

    USER INPUT: {task_inputs}
    TASKS:
    """

    tasks_refined = prompt_llm(llm, prompt_retreive_tasks)

    # Converting the tasks to a json file
    tasks = json.loads(tasks_refined)

    # Getting a due date for the tasks
    for task in tasks:
        task["due_date"] = input(f"""What is the due date for this task (date and time): {task['task']}?\n
                                 if this task repeats mention the day of the week and time or daily (eg. monday, friday 5:00PM)\n
                                 Reply: """)
        
    print(tasks)

    schedule_prompt = f"""
        Based on the following tasks and their due dates, create an optimized daily schedule for the user. 
        Consider time management best practices and prioritize urgent/important tasks.

        Guidelines:
        1. Group similar tasks together (e.g., work tasks, school tasks)
        2. Schedule cognitively demanding tasks during peak productivity hours (typically morning)
        3. Include short breaks between tasks (5-15 minutes)
        4. Schedule exercise at optimal times (morning or late afternoon)
        5. Ensure adequate time for meals and personal time
        6. If a task is marked 'daily', schedule it at the same time each day
        7. Allocate appropriate time blocks based on task complexity

        Format Requirements:
        - Return as a JSON array of schedule objects with EXACTLY these fields:
        - time (string in "HH:MM AM/PM" format)
        - duration (string in minutes)
        - task (string)
        - category (string)
        - notes (string with any relevant notes)

        User's Tasks:
        {tasks}

        Generate a well-balanced schedule that would help the user be productive while maintaining good work-life balance:
    """

    schedule = prompt_llm(llm, schedule_prompt)

    # Based on the response, ask for the tasks involved
    # task_input = input("What tasks are involved in this goal? ")
    # refined_tasks = prompt_llm(llm, f"From this user input, I just want you to extract: '{task_input}'. ")
    # print(f"PPA Assistant: {refined_tasks}")

    # # Plan the tasks based on the response
    # plan_response = prompt_llm(llm, f"{PROMPT_LANG}Break these tasks into a plan: {refined_tasks}.{SPECIFIED_LANG}")
    # print(f"PPA Assistant: {plan_response}")

