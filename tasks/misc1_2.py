# -----------------------------------------
# Advanced MikroTik SSH Management Tasks
# -----------------------------------------



###################
# Retrieve system identity (router name)
###################
def get_system_identity(client):
    """
    Returns system identity (router name).
    """
    output = client.call("/system identity print")

    for line in output.splitlines():
        if "name:" in line:
            return line.split("name:", 1)[1].strip()

    return "unknown"

###################
# Retrieve system resources as a dictionary
###################
def get_system_resources(client):
    """
    Returns system resource info as a dict.
    """
    output = client.call("/system resource print")

    resources = {}
    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            resources[key.strip()] = value.strip()

    return resources

###################
# Display system information (identity and resources)
###################
def task_system_info(client, router_name=None):
    identity = get_system_identity(client)
    resources = get_system_resources(client)

    print(f"\n--- System Info for {identity} ({router_name}) ---\n")

    if not resources:
        print("No system resource data returned")
        return

    for key, value in resources.items():
        print(f"{key:>25}: {value}")

###################
# Check for available package updates and return info
###################
def check_updates(client):
    """
    Triggers update check and returns update info as dict.
    """
    try:
        # Trigger update check
        client.call("/system package update check-for-updates")

        # Fetch update status
        output = client.call("/system package update print")

        info = {}
        for line in output.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip()] = value.strip()

        return info

    except Exception as e:
        print(f"Error checking updates: {e}")
        return {}

###################
# Install available package updates
# Router may reboot after installation
###################
def install_updates(client):
    """
    Triggers package installation.
    Router may reboot.
    """
    try:
        client.call("/system package update install")
    except Exception as e:
        print(f"Error installing updates: {e}")

###################
# Task to display update status and optionally install updates
###################
def task_package_updates(client, router_name=None):
    info = check_updates(client)

    installed = info.get("installed-version", "unknown")
    latest = info.get("latest-version", "unknown")
    status = info.get("status", "")

    print(f"\n--- Package Update Status ({router_name}) ---")
    print(f"   Installed: {installed}")
    print(f"   Latest:    {latest}")
    print(f"   Status:    {status}")

    if installed == "unknown" or latest == "unknown":
        print("   Unable to determine update state, skipping.")
        return

    if installed == latest:
        print("   Router is already up to date.")
        return

    if "checking" in status.lower():
        print("   Update check still in progress, try again later.")
        return

    confirm = input(
        "\nType YES to install updates (router may reboot): "
    ).strip()

    if confirm != "YES":
        print("   Update cancelled.")
        return

    install_updates(client)
    print("   Update triggered successfully. Router may reboot.")
