# -----------------------------------------
# Additional Advanced MikroTik SSH Tasks
# -----------------------------------------

###################
# Show per-interface bandwidth usage and optionally reset counters
###################
def task_bandwidth_accounting(client, router_name=None):
    """Show per-interface bandwidth usage and reset counters optionally."""
    label = f"[{router_name}]" if router_name else ""
    try:
        output = client.call("/interface/monitor-traffic all once")
        print(f"\n{label} Interface Traffic:\n{output}")
        reset = input(f"{label} Reset counters? (y/n): ").strip().lower()
        if reset == "y":
            client.call("/interface/reset-counters all")
            print(f"{label} Counters reset successfully.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show connected hotspot users and optionally disconnect a user
###################
def task_hotspot_users(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        users = client.call("/ip/hotspot/active/print without-paging detail")
        print(f"\n{label} Hotspot Users:\n{users}")
        disconnect = input(f"{label} Disconnect user by IP (ENTER to skip): ").strip()
        if disconnect:
            client.call(f"/ip/hotspot/active/remove [find address={disconnect}]")
            print(f"{label} User {disconnect} disconnected.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show DNS cache and optionally flush it
###################
def task_dns_cache(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        cache = client.call("/ip/dns/cache/print without-paging detail")
        print(f"\n{label} DNS Cache:\n{cache}")
        flush = input(f"{label} Flush DNS cache? (y/n): ").strip().lower()
        if flush == "y":
            client.call("/ip/dns/cache/flush")
            print(f"{label} DNS cache flushed.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show system logs and optionally export to file
###################
def task_logs_export(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        logs = client.call("/log/print without-paging count=50")
        print(f"\n{label} Recent Logs:\n{logs}")
        export = input(f"{label} Export logs to file? Enter filename or ENTER to skip: ").strip()
        if export:
            client.call(f"/log/save name={export}")
            print(f"{label} Logs saved as {export}.rsc")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show installed certificates and optionally remove one
###################
def task_certificates(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        certs = client.call("/certificate/print without-paging detail")
        print(f"\n{label} Certificates:\n{certs}")
        remove = input(f"{label} Remove certificate by name (ENTER to skip): ").strip()
        if remove:
            client.call(f"/certificate/remove [find name={remove}]")
            print(f"{label} Certificate {remove} removed.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Run a bandwidth test to another MikroTik host
###################
def task_bandwidth_test(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        target = input(f"{label} Enter target IP for bandwidth test: ").strip()
        result = client.call(f"/tool/bandwidth-test address={target} duration=5s")
        print(f"{label} Bandwidth Test Result:\n{result}")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show CAPsMAN AP and client status
###################
def task_capsman_status(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        aps = client.call("/caps-man/registration-table/print without-paging detail")
        print(f"\n{label} CAPsMAN Registered APs:\n{aps}")
        radios = client.call("/interface/wireless/print without-paging detail")
        print(f"\n{label} Wireless Radios:\n{radios}")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show Netwatch hosts and optionally toggle one
###################
def task_netwatch(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        hosts = client.call("/tool/netwatch/print without-paging detail")
        print(f"\n{label} Netwatch Hosts:\n{hosts}")
        toggle = input(f"{label} Enable/disable host by number (ENTER to skip): ").strip()
        if toggle:
            action = input(f"{label} Enable or Disable? (e/d): ").strip().lower()
            disabled = "no" if action == "e" else "yes"
            client.call(f"/tool/netwatch/set numbers={toggle} disabled={disabled}")
            print(f"{label} Host {toggle} {'enabled' if action=='e' else 'disabled'}.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show SNMP configuration and optionally enable/disable it
###################
def task_snmp_status(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        snmp = client.call("/snmp/print detail without-paging")
        print(f"\n{label} SNMP Config:\n{snmp}")
        toggle = input(f"{label} Enable/disable SNMP? (e/d/ENTER to skip): ").strip().lower()
        if toggle in ["e", "d"]:
            disabled = "no" if toggle == "e" else "yes"
            client.call(f"/snmp/set disabled={disabled}")
            print(f"{label} SNMP {'enabled' if toggle=='e' else 'disabled'}.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# List scripts and optionally run one
###################
def task_script_management(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        scripts = client.call("/system/script/print without-paging detail")
        print(f"\n{label} Scripts:\n{scripts}")
        run = input(f"{label} Run script by name (ENTER to skip): ").strip()
        if run:
            client.call(f"/system/script/run [find name={run}]")
            print(f"{label} Script {run} executed.")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show Queue Tree status
###################
def task_queue_tree(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        qt = client.call("/queue/tree/print without-paging detail")
        print(f"\n{label} Queue Tree:\n{qt}")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show current Traffic Flow / NetFlow info
###################
def task_traffic_flow(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        flow = client.call("/tool/traffic-flow/print without-paging detail")
        print(f"\n{label} Traffic Flow Info:\n{flow}")
    except Exception as e:
        print(f"{label} Error: {e}")


###################
# Show VPN users and optionally disconnect them
###################
def task_vpn_user_management(client, router_name=None):
    label = f"[{router_name}]" if router_name else ""
    try:
        vpn = client.call("/ppp/active/print without-paging detail")
        print(f"\n{label} Active VPN Users:\n{vpn}")
        disconnect = input(f"{label} Disconnect user by name (ENTER to skip): ").strip()
        if disconnect:
            client.call(f"/ppp/active/remove [find name={disconnect}]")
            print(f"{label} VPN user {disconnect} disconnected.")
    except Exception as e:
        print(f"{label} Error: {e}")
