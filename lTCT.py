from typing import TypedDict, List, Dict, Callable

class Task(TypedDict):
    title: str
    done: bool
    priority: int

tasks: List[Task] = []


def print_menu() -> None:
    """Display the main menu options."""
    print("\n--- Daily Task Manager (oT-oT) ---")
    print("1 - Add new task")
    print("2 - Show all tasks")
    print("3 - Toggle task status")
    print("4 - Delete a task")
    print("5 - Report (done/undone count)")
    print("6 - Search tasks")
    print("0 - Exit")


def input_priority() -> int:
    """Prompt user for a valid priority value (1, 2, or 3)."""
    while True:
        try:
            p = int(input("Enter priority (1=High, 2=Medium, 3=Low): "))
            if p in (1, 2, 3):
                return p
            print("Invalid priority. Try again.")
        except ValueError:
            print("Please enter a number (1-3).")


def add_task() -> None:
    """Add a new task to the list, preventing duplicate titles and empty input."""
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    if title_exists(title):
        print("Task with this title already exists.")
        return
    priority = input_priority()
    tasks.append({"title": title, "done": False, "priority": priority})
    print("Task added.")


def title_exists(title: str) -> bool:
    """Return True if a task with the given title already exists (case-insensitive)."""
    return any(t["title"].lower() == title.lower() for t in tasks)


def get_display_index(prompt: str) -> int | None:
    """Ask user for a displayed task number and return the original task index, or None on error."""
    if not tasks:
        print("No tasks available.")
        return None
    mapping = build_display_mapping()
    try:
        idx = int(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None
    if 1 <= idx <= len(mapping):
        return mapping[idx - 1]
    print("Invalid task number.")
    return None


def find_matching_tasks(keyword: str) -> list[tuple[int, Task]]:
    """Return list of (orig_index, task) matching keyword sorted by priority."""
    matches = [(i, t) for i, t in enumerate(tasks) if keyword in t["title"].lower()]
    return sorted(matches, key=lambda pair: pair[1]["priority"])


def _indexed_tasks() -> List[tuple[int, Task]]:
    """Return list of (index, task) pairs for current tasks."""
    return list(enumerate(tasks))


def _sorted_indexed_by_priority(indexed: List[tuple[int, Task]] | None = None) -> List[tuple[int, Task]]:
    """Return indexed tasks sorted by priority (1 highest)."""
    if indexed is None:
        indexed = _indexed_tasks()
    return sorted(indexed, key=lambda pair: pair[1]["priority"])


def build_display_groups() -> tuple[list[tuple[int, Task]], list[tuple[int, Task]]]:
    """Split sorted indexed tasks into (undone, done) groups."""
    sorted_indexed = _sorted_indexed_by_priority()
    undone = [pair for pair in sorted_indexed if not pair[1]["done"]]
    done = [pair for pair in sorted_indexed if pair[1]["done"]]
    return undone, done


def build_display_mapping() -> list[int]:
    """Return a list mapping displayed numbers to original task indices."""
    undone, done = build_display_groups()
    return [orig for orig, _ in (undone + done)]


def format_task_line(index: int, task: Task) -> str:
    """Return a formatted single-line representation of a task for display."""
    status = "[x]" if task["done"] else "[ ]"
    return f"{index}. {status} {task['title']} (Priority: {task['priority']})"


def print_grouped_tasks() -> None:
    """Print tasks grouped by undone and done, both sorted by priority."""
    undone, done = build_display_groups()

    print("\nTasks:")
    if undone:
        print("\nUndone:")
        for i, (_, task) in enumerate(undone, 1):
            print(format_task_line(i, task))
    else:
        print("\nNo undone tasks.")

    if done:
        start = len(undone) + 1
        print("\nDone:")
        for offset, (_, task) in enumerate(done, start):
            print(format_task_line(offset, task))


def show_tasks() -> None:
    """Display all tasks, sorted by priority (1=High first)."""
    if not tasks:
        print("No tasks found.")
        return

    print_grouped_tasks()


def toggle_task() -> None:
    """Toggle the completion status of a selected task."""
    orig_idx = get_display_index("Enter task number to toggle: ")
    if orig_idx is None:
        return
    tasks[orig_idx]["done"] = not tasks[orig_idx]["done"]
    print("Task status updated.")


def delete_task() -> None:
    """Delete a task from the list by its number."""
    orig_idx = get_display_index("Enter task number to delete: ")
    if orig_idx is None:
        return
    del tasks[orig_idx]
    print("Task deleted.")


def report() -> None:
    """Display the count of completed and uncompleted tasks."""
    done_count = sum(1 for t in tasks if t["done"])
    undone_count = len(tasks) - done_count
    print(f"Done: {done_count} | Undone: {undone_count}")

def search_tasks() -> None:
    """Search for tasks by a keyword in their title."""
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("Keyword cannot be empty.")
        return
    sorted_found = find_matching_tasks(keyword)
    if not sorted_found:
        print("No tasks found for this keyword.")
        return

    print("\nSearch results:")
    for idx, (_, task) in enumerate(sorted_found, 1):
        print(format_task_line(idx, task))


def main() -> None:
    """Main loop for the CLI todo manager. Handles user input and menu navigation."""
    def get_int(prompt: str) -> int | None:
        """Read an int from input, returning None on invalid input."""
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            return None

    actions: Dict[int, Callable[[], None]] = {
        1: add_task,
        2: show_tasks,
        3: toggle_task,
        4: delete_task,
        5: report,
        6: search_tasks,
    }

    while True:
        print_menu()
        choice = get_int("Select an option (0-6): ")
        if choice is None:
            continue
        if choice == 0:
            print("Exiting. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
