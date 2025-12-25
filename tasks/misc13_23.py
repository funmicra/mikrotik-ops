# -----------------------------------------
# Additional Advanced MikroTik SSH Tasks
# -----------------------------------------




###################
# Backup or restore router configuration interactively
###################
def task_backup_restore(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        choice = input(f"{label} Backup or Restore config? (b/r): ").strip().lower()
        if choice == "b":
            name = input(f"{label} Enter backup name: ").strip()
            cmd = f"/system/backup/save name={name}"
            client.call(cmd)
            print(f"{label} Backup '{name}' saved successfully.")
        elif choice == "r":
            name = input(f"{label} Enter backup name to restore: ").strip()
            cmd = f"/system/backup/load name={name}"
            client.call(cmd)
            print(f"{label} Backup '{name}' restored successfully. Reboot may be required.")
        else:
            print(f"{label} Invalid choice, skipping.")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Display interface traffic statistics
###################
def task_interface_traffic(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        output = client.call("/interface monitor-traffic all once")
        print(f"\n{label} Interface Traffic:\n{output}")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# List DHCP leases and optionally remove one
###################
def task_dhcp_leases(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        leases = client.call("/ip/dhcp-server/lease/print without-paging")
        print(f"\n{label} DHCP Leases:\n{leases}")

        remove = input(f"{label} Remove a lease? Enter IP or ENTER to skip: ").strip()
        if remove:
            cmd = f"/ip/dhcp-server/lease/remove [find address={remove}]"
            client.call(cmd)
            print(f"{label} Lease {remove} removed.")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Show routing table and test next-hop connectivity
###################
def task_routes(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        routes = client.call("/ip/route/print detail without-paging")
        print(f"\n{label} Routing Table:\n{routes}")

        test = input(f"{label} Ping a destination? Enter IP or ENTER to skip: ").strip()
        if test:
            result = client.call(f"/ping {test} count=3")
            print(f"{label} Ping result:\n{result}")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Display firewall rules and allow interactive enable/disable
###################
def task_firewall_manage(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        rules = client.call("/ip/firewall/filter/print without-paging detail")
        print(f"\n{label} Firewall Rules:\n{rules}")

        choice = input(f"{label} Enter rule number to enable/disable (ENTER to skip): ").strip()
        if choice:
            action = input(f"{label} Enable or Disable rule {choice}? (e/d): ").strip().lower()
            disabled = "no" if action == "e" else "yes"
            client.call(f"/ip/firewall/filter/set numbers={choice} disabled={disabled}")
            print(f"{label} Rule {choice} {'enabled' if action=='e' else 'disabled'}.")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Show active VPN / tunnels: WireGuard, IPsec, ZeroTier
###################
def task_vpn_status(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        wg = client.call("/interface/wireguard/print detail without-paging")
        print(f"\n{label} WireGuard Interfaces:\n{wg}")
        ipsec = client.call("/ip/ipsec/active-peers/print detail without-paging")
        print(f"\n{label} IPsec Active Peers:\n{ipsec}")
        zerotier = client.call("/interface/zerotier-one/print detail without-paging")
        print(f"\n{label} ZeroTier Interfaces:\n{zerotier}")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Display simple queue / QoS status
###################
def task_queue_status(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        queues = client.call("/queue/simple/print without-paging detail")
        print(f"\n{label} Queue Status:\n{queues}")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# List users and optionally disable inactive ones
###################
def task_user_audit(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        users = client.call("/user/print detail without-paging")
        print(f"\n{label} Users:\n{users}")
        disable = input(f"{label} Disable a user? Enter name or ENTER to skip: ").strip()
        if disable:
            client.call(f"/user/set [find name={disable}] disabled=yes")
            print(f"{label} User {disable} disabled.")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Show system clock, NTP status, and optionally sync time
###################
def task_time_ntp(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        time = client.call("/system/clock/print detail without-paging")
        ntp = client.call("/system/ntp/client/print detail without-paging")
        print(f"\n{label} System Clock:\n{time}")
        print(f"\n{label} NTP Client:\n{ntp}")
        sync = input(f"{label} Sync time with NTP servers? (y/n): ").strip().lower()
        if sync == "y":
            client.call("/system/ntp/client/sync")
            print(f"{label} Time synchronized.")
    except Exception as e:
        print(f"{label} Error: {e}")

###################
# Display ARP table and neighbors
###################
def task_arp_neighbor(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        arp = client.call("/ip/arp/print detail without-paging")
        neighbor = client.call("/ip/neighbor/print detail without-paging")
        print(f"\n{label} ARP Table:\n{arp}")
        print(f"\n{label} Neighbors:\n{neighbor}")
    except Exception as e:
        print(f"{label} Error: {e}")
