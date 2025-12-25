from tasks.misc1_2 import task_system_info, task_package_updates
from tasks.misc3_13 import task_reboot_router, task_ssh_shell, task_scheduler, task_import_ssh_keys, task_create_user, task_services, task_system_logs, task_ip_addresses, task_firewall_rules, task_interfaces_status, task_backup_config
from tasks.misc13_23 import task_backup_restore, task_interface_traffic, task_dhcp_leases, task_routes, task_firewall_manage, task_vpn_status, task_queue_status, task_user_audit, task_time_ntp, task_arp_neighbor
from tasks.misc24_34 import task_bandwidth_accounting, task_hotspot_users, task_dns_cache, task_logs_export, task_certificates, task_bandwidth_test, task_capsman_status, task_netwatch, task_snmp_status, task_script_management, task_queue_tree, task_traffic_flow, task_vpn_user_management


TASKS = {
    1: {"name": "Show system information", "func": task_system_info},
    2: {"name": "Check & install RouterOS updates", "func": task_package_updates},
    3: {"name": "Create user", "func": task_create_user},
    4: {"name": "Import SSH keys for a user", "func": task_import_ssh_keys},
    5: {"name": "Backup Configuration", "func": task_backup_config},
    6: {"name": "Check Interface Status", "func": task_interfaces_status},
    7: {"name": "Reboot System", "func": task_reboot_router},
    8: {"name": "Firewall Rules", "func": task_firewall_rules},
    9: {"name": "IP Addresses", "func": task_ip_addresses},
    10: {"name": "System Logs", "func": task_system_logs},
    11: {"name": "Manage Services", "func": task_services},
    12: {"name": "Scheduled Tasks", "func": task_scheduler},
    13: {"name": "shell", "func": task_ssh_shell},
    14: {"name": "Backup & Restore Config", "func": task_backup_restore},
    15: {"name": "Interface Traffic", "func": task_interface_traffic},
    16: {"name": "DHCP Lease Management", "func": task_dhcp_leases},
    17: {"name": "Routing Table & Ping", "func": task_routes},
    18: {"name": "Firewall Management", "func": task_firewall_manage},
    19: {"name": "VPN / Tunnel Status", "func": task_vpn_status},
    20: {"name": "Queue / QoS Status", "func": task_queue_status},
    21: {"name": "User Audit", "func": task_user_audit},
    22: {"name": "Time & NTP Management", "func": task_time_ntp},
    23: {"name": "ARP / Neighbor Inspection", "func": task_arp_neighbor},
    24: {"name": "Bandwidth Accounting", "func": task_bandwidth_accounting},
    25: {"name": "Hotspot Users", "func": task_hotspot_users},
    26: {"name": "DNS Cache", "func": task_dns_cache},
    27: {"name": "Logs Export", "func": task_logs_export},
    28: {"name": "Certificates Management", "func": task_certificates},
    29: {"name": "Bandwidth Test", "func": task_bandwidth_test},
    30: {"name": "CAPsMAN Status", "func": task_capsman_status},
    31: {"name": "Netwatch Hosts", "func": task_netwatch},
    32: {"name": "SNMP Status", "func": task_snmp_status},
    33: {"name": "Script Management", "func": task_script_management},
    34: {"name": "Queue Tree Status", "func": task_queue_tree},
    35: {"name": "Traffic Flow Info", "func": task_traffic_flow},
    36: {"name": "VPN User Management", "func": task_vpn_user_management},
}
