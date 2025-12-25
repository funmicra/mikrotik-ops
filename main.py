# -----------------------------------------
# MikroTik SSH Task Runner / Inventory Tool
# -----------------------------------------
#
# This script provides a CLI interface to run advanced SSH tasks
# on multiple MikroTik routers. Features include:
#   - Displaying router inventory from config
#   - Selecting routers to target
#   - Running tasks defined in TASKS registry
#   - Managing SSH sessions (connect/close) safely
#   - Graceful handling of errors per router
#
# Dependencies:
#   - routers.py: get_router_clients() to return router SSH clients
#   - ui.py: CLI menu helpers (show_menu, get_user_choice, select_routers)
#   - registry.py: TASKS dict defining available tasks
#   - config.py: ROUTERS dict with router names and IPs
#
# Usage:
#   python3 task_runner.py
#   - Select a task from menu
#   - Choose one or more routers to execute the task
#   - Task output is displayed per router
# -----------------------------------------


from routers import get_router_clients
from ui import show_menu, get_user_choice, select_routers
from registry import TASKS
from config import ROUTERS

###################
# Run a given task on selected routers
###################
def run_task(task):
    print(f"\nExecuting task: {task['name']}\n")

    clients = get_router_clients()
    selected_clients = select_routers(clients)

    if not selected_clients:
        print("Task cancelled.\n")
        return

    for name, client in selected_clients.items():
        print(f"--- {name} ---")
        try:
            client.connect()                 # establish SSH session
            task["func"](client, name)       # run task payload
        except Exception as e:
            print(f"Error on {name}: {e}")
        finally:
            client.close()                   # enforce session cleanup

    print("\nTask completed.\n")


###################
# Print all routers from configuration inventory
###################
def print_inventory():
    print("\nLoaded router inventory:")
    for name, ip in ROUTERS.items():
        print(f" - {name} -> {ip}")
    print("")


###################
# Main program loop: show menu, select tasks, execute
###################
def main():
    print_inventory()

    while True:
        show_menu()
        choice = get_user_choice()

        if choice == 0:
            print("Exiting.")
            break

        task = TASKS.get(choice)
        if not task:
            print("Invalid selection.\n")
            continue

        run_task(task)



###################
# Entry point
###################
if __name__ == "__main__":
    main()