# -----------------------------------------
# Additional Advanced MikroTik SSH Tasks
# -----------------------------------------




###################
# Reboot the router after confirmation
###################
def task_reboot_router(client, router_name=None, *args, **kwargs):
    confirm = input(f"{router_name}: Type YES to reboot: ").strip()
    if confirm != "YES":
        print(f"{router_name}: Reboot cancelled")
        return

    try:
        client.call("/system reboot")
        print(f"{router_name}: Reboot triggered (SSH session may drop)")
    except Exception as e:
        print(f"{router_name}: Failed to trigger reboot: {e}")

import subprocess
###################
# Open an interactive SSH shell to the router
###################
def task_ssh_shell(client, router_name):
    host = client.host
    user = client.username
    ssh_key = getattr(client, "ssh_key", None)

    print(f"Opening SSH shell to {router_name} ({host})...\n"
          f"Press Ctrl+D or type 'exit' to return.\n")

    ssh_cmd = ["ssh", f"{user}@{host}"]

    if ssh_key:
        ssh_cmd.extend(["-i", ssh_key])

    try:
        subprocess.run(ssh_cmd)
    except KeyboardInterrupt:
        print("\nSSH session interrupted by user.")
    except Exception as e:
        print(f"Failed to open SSH session: {e}")

###################
# List all scheduled tasks in RouterOS CLI style
###################
def task_scheduler(client, router_name=None):
    router_label = f"[{router_name}]" if router_name else ""
    try:
        output = client.call("/system/scheduler/print without-paging detail")
        print(f"\n--- Scheduled Tasks on {router_label} ---\n")
        print(output)
    except Exception as e:
        print(f"{router_label} Error retrieving scheduler: {e}")

import os
###################
# Import SSH public keys for a given user
###################
import os
import glob

def task_import_ssh_keys(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""

    # Fetch all users from router
    try:
        users_output = client.call("/user/print detail without-paging")
    except Exception as e:
        print(f"{label} Failed to fetch users: {e}")
        return

    # Parse users (assuming RouterOS returns key=value format)
    users = []
    for line in users_output.splitlines():
        parts = dict(kv.split("=", 1) for kv in line.split() if "=" in kv)
        if "name" in parts:
            users.append(parts["name"])

    if not users:
        print(f"{label} No users found on router. Aborting.")
        return

    # Show users with index
    print(f"\n{label} Available users:")
    for idx, u in enumerate(users, 1):
        print(f"{idx}. {u}")

    # Select user by index
    selection = input(f"{label} Enter user number to import keys for: ").strip()
    if not selection.isdigit() or int(selection) < 1 or int(selection) > len(users):
        print(f"{label} Invalid selection. Aborting.")
        return

    username = users[int(selection) - 1]
    print(f"{label} Selected user: {username}")

    # Ask for folder with .pub keys
    key_folder = input(f"{label} Enter folder to search for .pub keys (default ~/.ssh/): ").strip() or os.path.expanduser("~/.ssh/")
    if not os.path.exists(key_folder):
        print(f"{label} Folder '{key_folder}' does not exist. Aborting.")
        return

    # List .pub files in folder (non-recursive)
    key_files = [f for f in os.listdir(key_folder) if f.endswith(".pub") and os.path.isfile(os.path.join(key_folder, f))]
    if not key_files:
        print(f"{label} No .pub keys found in '{key_folder}'. Aborting.")
        return

    print(f"\n{label} Available keys:")
    for idx, k in enumerate(key_files, 1):
        print(f"{idx}. {k}")

    # Default to first key
    selected_indices = input(f"{label} Enter comma-separated numbers of keys to import (default first key): ").strip() or "1"
    selected_indices = [int(i) for i in selected_indices.split(",") if i.isdigit() and 1 <= int(i) <= len(key_files)]

    for i in selected_indices:
        key_file = key_files[i - 1]
        key_path = os.path.join(key_folder, key_file)
        with open(key_path, "r") as f:
            pubkey_content = f.read().strip()

        cmd = f'/user ssh-keys add user={username} public-key="{pubkey_content}"'
        try:
            client.call(cmd)
            print(f"{label} Key '{key_file}' imported for user '{username}'")
        except Exception as e:
            print(f"{label} Failed to import key '{key_file}': {e}")




###################
# Create a new RouterOS user interactively
###################
def task_create_user(client, router_name=None, *args, **kwargs):
    username = input("Enter new username: ").strip()
    if not username:
        print(f"{router_name}: Aborted. Username cannot be empty.")
        return

    output = client.call('/user print')
    existing_users = []
    for line in output.splitlines():
        if "name:" in line:
            name = line.split("name:", 1)[1].strip()
            existing_users.append(name)

    if username in existing_users:
        print(f"{router_name}: User '{username}' already exists")
        return

    password = input(f"Enter password for user '{username}' on {router_name}: ").strip()
    if not password:
        print(f"{router_name}: Aborted. Password cannot be empty.")
        return

    cmd = f"/user add name={username} password={password} group=full disabled=no"

    try:
        client.call(cmd)
        print(f"{router_name}: User '{username}' created successfully")
    except Exception as e:
        print(f"{router_name}: Failed to create user '{username}': {e}")

###################
# Manage RouterOS services (enable/disable) interactively
###################
def task_services(client, router_name=None):
    router_label = f"[{router_name}]" if router_name else ""

    try:
        output = client.call("/ip/service/print without-paging detail")
        print(f"\n{router_label} Services on Router:\n")
        print(output)

        while True:
            service_id = input(f"\n{router_label} Enter service number to toggle enable/disable (ENTER to finish): ").strip()
            if not service_id:
                break

            action = input(f"{router_label} Enable or Disable service {service_id}? (e/d): ").strip().lower()
            if action not in ["e", "d"]:
                print(f"{router_label} Invalid choice, skipping.")
                continue

            disabled_value = "no" if action == "e" else "yes"
            cmd = f"/ip/service/set numbers={service_id} disabled={disabled_value}"
            client.call(cmd)
            print(f"{router_label} Service {service_id} {'enabled' if action=='e' else 'disabled'} successfully.")

    except Exception as e:
        print(f"{router_label} Error managing services: {e}")

###################
# Fetch and display recent system logs
###################
def task_system_logs(client, router_name, limit=20, *args, **kwargs):
    try:
        raw = client.call("/log/print detail without-paging")
        if isinstance(raw, bytes):
            raw = raw.decode()
        lines = raw.splitlines() if isinstance(raw, str) else [str(raw)]
        if not lines:
            print(f"{router_name}: No logs found")
            return
    except Exception as e:
        print(f"{router_name}: Failed to fetch logs: {e}")
        return

    print(f"\n--- Recent Logs on {router_name} ---")
    for line in lines[-limit:]:
        print(line.strip().strip('"'))
    print("\nTask completed.")

###################
# Show detailed IP addresses on the router
###################
def task_ip_addresses(client, router_name, *args, **kwargs):
    try:
        raw = client.call("/ip/address/print detail without-paging")
        if isinstance(raw, bytes):
            raw = raw.decode()
        lines = raw.splitlines()
    except Exception as e:
        print(f"{router_name}: Failed to fetch IP addresses: {e}")
        return

    if not lines:
        print(f"{router_name}: No IP addresses found")
        return

    print(f"\n--- IP Addresses on {router_name} ---\n")
    print(f"{'FLAGS':<3} {'ADDRESS':<18} : {'NETWORK':<18} : {'INTERFACE':<20} : {'ACTUAL-IF':<20} : COMMENT")
    print("-" * 95)

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Flags:"):
            continue

        parts = line.split()
        flags = ""
        idx = 0
        if len(parts) > 1 and parts[1] in ('X', 'I', 'D', 'S'):
            flags = parts[1]
            idx = 2
        else:
            idx = 1

        comment = ""
        if ';;;' in line:
            comment_index = line.index(';;;') + 3
            comment = line[comment_index:].strip()

        kv = {}
        for token in parts[idx:]:
            if '=' in token:
                k, v = token.split('=', 1)
                kv[k] = v.strip('"')

        address = kv.get('address', '—')
        network = kv.get('network', '—')
        interface = kv.get('interface', '—')
        actual = kv.get('actual-interface', '—')

        print(f"{flags:<3} {address:<18} : {network:<18} : {interface:<20} : {actual:<20} : {comment}")

    print("\nTask completed.")

###################
# Show firewall filter rules with details
###################
def task_firewall_rules(client, router_name=None, *args, **kwargs):
    try:
        raw = client.call('/ip/firewall/filter/print detail without-paging')
        lines = raw.splitlines() if isinstance(raw, str) else [str(l) for l in raw]
    except Exception as e:
        print(f"{router_name}: Failed to fetch firewall rules: {e}")
        return

    if not lines:
        print(f"{router_name}: No firewall rules found")
        return

    print(f"\n--- Firewall Rules on {router_name} ---")

    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        flags = ""
        tokens = line.split()
        if len(tokens) > 1 and tokens[1].startswith(('X','D','I')):
            flags = tokens[1]
            tokens = tokens[2:]
        else:
            tokens = tokens[1:]

        comment = ""
        if ';;;' in line:
            comment_index = line.index(';;;') + 3
            comment = line[comment_index:].strip()

        kv_pairs = []
        for t in tokens:
            if '=' in t:
                k, v = t.split('=', 1)
                kv_pairs.append(f"{k}={v.strip('\"')}")
            else:
                kv_pairs.append(t)

        line_out = " ".join(kv_pairs)
        if comment:
            line_out = f"{line_out} ;;; {comment}"
        print(f"{idx:<2} {flags} {line_out}".rstrip())

    print("\nTask completed.")

###################
# Show interface status along with assigned IP addresses
###################
def task_interfaces_status(client, router_name=None, *args, **kwargs):
    try:
        intf_data = client.call("/interface print")
        ip_data = client.call("/ip address print")
    except Exception as e:
        print(f"{router_name}: Failed to fetch interface or IP data: {e}")
        return

    print(f"\n--- DEBUG: /interface print on {router_name} ---")
    print(intf_data)
    print(f"\n--- DEBUG: /ip address print on {router_name} ---")
    print(ip_data)

    ip_map = {}
    for line in ip_data.splitlines():
        parts = {}
        for kv in line.split():
            if "=" in kv:
                k, v = kv.split("=", 1)
                parts[k.strip()] = v.strip()
        iface = parts.get("interface")
        addr = parts.get("address")
        if iface and addr:
            ip_map.setdefault(iface, []).append(addr)

    print(f"\n--- Interfaces on {router_name} ---")
    for line in intf_data.splitlines():
        parts = {}
        for kv in line.split():
            if "=" in kv:
                k, v = kv.split("=", 1)
                parts[k.strip()] = v.strip()

        if not parts.get("name"):
            continue

        name = parts.get("name")
        intf_type = parts.get("type", "")
        disabled = parts.get("disabled", "no").lower() in ["yes", "true"]
        running = parts.get("running", "no").lower() in ["yes", "true"]

        if intf_type in ["ether", "sfp", "sfpplus"]:
            status = "UP" if running and not disabled else "DOWN"
        elif intf_type == "cap":
            status = "UP" if not disabled else "DOWN"
        elif intf_type == "bridge":
            status = "UP"
        elif intf_type in ["wg", "zerotier", "loopback"]:
            status = "UP"
        else:
            status = "DOWN" if parts.get("link-down", "false").lower() in ["yes", "true"] else "UP"

        ips = ", ".join(ip_map.get(name, [])) if ip_map.get(name) else "—"
        print(f"{name:20} : {status:4} : {ips}")

###################
# Backup router configuration to a file
###################
def task_backup_config(client, router_name=None, *args, **kwargs):
    if not router_name:
        router_name = "router"

    filename = f"{router_name}_backup.backup"
    cmd = f'/system backup save name={filename}'

    try:
        client.call(cmd)
        print(f"{router_name}: Backup saved as {filename}")
    except Exception as e:
        print(f"{router_name}: Failed to save backup: {e}")
