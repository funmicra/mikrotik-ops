from registry import TASKS
import math

def show_menu(columns=3):
    print("\nAvailable tasks:\n")

    # Prepare task strings with optional read-only note
    task_list = [
        f"{idx}. {task['name']}{' (read-only)' if task.get('read_only') else ''}"
        for idx, task in TASKS.items()
    ]

    # Determine number of rows needed
    rows = math.ceil(len(task_list) / columns)

    # Pad the list to fill complete grid
    while len(task_list) < rows * columns:
        task_list.append("")

    # Split tasks into columns
    columns_data = [
        task_list[r*columns:(r+1)*columns]
        for r in range(rows)
    ]

    # Transpose to print row by row
    for r in range(rows):
        row_items = []
        for c in range(columns):
            # Calculate max width per column
            col_tasks = [task_list[i + rows * c] for i in range(rows)]
            width = max(len(t) for t in col_tasks) + 2
            row_items.append(task_list[r + rows * c].ljust(width))
        print("".join(row_items))

    print("\n0. Exit")


def get_user_choice():
    try:
        return int(input("\nSelect task: ").strip())
    except ValueError:
        return -1


def select_routers(clients):
    if not clients:
        print("No routers available.")
        return {}

    names = list(clients.keys())

    print("\nAvailable routers (SSH):")
    for idx, name in enumerate(names, start=1):
        print(f"{idx}. {name}")

    selection = input(
        "\nSelect routers by index (comma-separated), "
        "ENTER for ALL, or 0 to cancel:\n> "
    ).strip()

    if selection == "0":
        return {}

    if not selection:
        return clients  # ALL routers

    indices = set()
    for i in selection.split(","):
        i = i.strip()
        if i.isdigit():
            indices.add(int(i))

    return {
        names[i - 1]: clients[names[i - 1]]
        for i in indices
        if 1 <= i <= len(names)
    }
