import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"
version = "0.0.1"
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()

parser.add_argument("yay", type=str, nargs='?')
if len(sys.argv) > 1 and sys.argv[1] == "yay":
    print("You found the easter egg!")
    sys.exit(0)

parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-v", "--version", action="version", version=f"{version}")
parser.add_argument("-e", "--edit", type=int, help="Edit a task by ID")

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
if args.list:
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        sys.exit(0)
    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}: {task['task']}")
    sys.exit(0)

elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            if task["done"]:
                task["done"] = False
                save_task(tasks)
                print(f"Task {args.complete} marked as incomplete")
                break
            else:
                task["done"] = True
                save_task(tasks)
                print(f"Task {args.complete} marked as complete")
                break

elif args.delete:
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != args.delete]
    save_task(new_tasks)
    print(f"Task {args.delete} deleted")

elif args.edit:
    tasks = load_tasks()
    new_tasks = []
    for task in tasks:
        if task["id"] == args.edit:
            task["task"] = input("Enter the new task: ")
            new_tasks.append(task)
            save_task(new_tasks)
            print(f"Task {args.edit} edited")
            break

elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1
    tasks.append({"id": new_id, "task": args.task, "done": False})
    save_task(tasks)

    print(f"Task {args.task} added with ID of {new_id}")