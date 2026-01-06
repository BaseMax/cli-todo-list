
from typing import TypedDict, List

class Task(TypedDict):
    """Represents a single todo task."""
    title: str
    done: bool
    priority: int

tasks: List[Task] = []


def print_menu() -> None:
    print("\n--- Daily Task Manager (oT-oT) ---")
    print("1 - Add new task")
    print("2 - Show all tasks")
    print("3 - Toggle task status")
    print("4 - Delete a task")
    print("5 - Report (done/undone count)")
    print("6 - Search tasks")
    print("0 - Exit")


def input_priority() -> int:
    """Get a valid priority from user."""
    while True:
        try:
            p = int(input("Enter priority (1=High, 2=Medium, 3=Low): "))
            if p in (1, 2, 3):
                return p
            print("Invalid priority. Try again.")
        except ValueError:
            print("Please enter a number (1-3).")


def add_task() -> None:
    """Add a new task, prevent duplicate titles."""
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    if any(task["title"].lower() == title.lower() for task in tasks):
        print("Task with this title already exists.")
        return
    priority = input_priority()
    tasks.append({"title": title, "done": False, "priority": priority})
    print("Task added.")


def show_tasks() -> None:
    """Show all tasks, sorted by priority."""
    if not tasks:
        print("No tasks found.")
        return
    print("\nTasks:")
    sorted_tasks = sorted(tasks, key=lambda t: t["priority"])
    for idx, task in enumerate(sorted_tasks, 1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{idx}. {status} {task['title']} (Priority: {task['priority']})")


def toggle_task() -> None:
    """Toggle the done status of a task."""
    if not tasks:
        print("No tasks to toggle.")
        return
    try:
        idx = int(input("Enter task number to toggle: "))
        if 1 <= idx <= len(tasks):
            tasks[idx-1]["done"] = not tasks[idx-1]["done"]
            print("Task status updated.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task() -> None:
    """Delete a task by its number."""
    if not tasks:
        print("No tasks to delete.")
        return
    try:
        idx = int(input("Enter task number to delete: "))
        if 1 <= idx <= len(tasks):
            del tasks[idx-1]
            print("Task deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def report() -> None:
    """Show count of done and undone tasks."""
    done_count = sum(1 for t in tasks if t["done"])
    undone_count = len(tasks) - done_count
    print(f"Done: {done_count} | Undone: {undone_count}")

def search_tasks() -> None:
    """Search tasks by keyword."""
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("Keyword cannot be empty.")
        return
    found = [task for task in tasks if keyword in task["title"].lower()]
    if not found:
        print("No tasks found for this keyword.")
        return
    print("\nSearch results:")
    for idx, task in enumerate(found, 1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{idx}. {status} {task['title']} (Priority: {task['priority']})")


def main() -> None:
    """Main loop for the CLI todo manager."""
    while True:
        print_menu()
        try:
            choice = int(input("Select an option (0-6): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if choice == 1:
            add_task()
        elif choice == 2:
            show_tasks()
        elif choice == 3:
            toggle_task()
        elif choice == 4:
            delete_task()
        elif choice == 5:
            report()
        elif choice == 6:
            search_tasks()
        elif choice == 0:
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
