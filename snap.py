test={
    "general": {
        "created_at": "18/04/2024 13:51:01",
        "created_by": "amir@deltasase.com",
        "tenant_id": "112233",
        "tenant_name": "test Tenant",
        "customer_id": "556688",
        "customer_name": "TEST Customer",
        "products": [
            "SDWAN",
            "SASE_RU",
            "SASE_Branch"
        ],
        "licenses": {
            "SDWAN": {}
        }
    },
    "servers": {
        "dhcp_servers": {},
        "dns_servers": {},
        "syslog_servers": {},
        "ipfix_collectors": {},
        "snmp_servers": {},
        "ldap_servers": {},
        "active_directories": {},
        "file_servers": {}
    },
    "machine_groups": {
        "MachineGroup1_mobiles": {
            "machines": {
                "Machine1": {
                    "id": "111",
                    "type": "",
                    "vendor": "",
                    "model": "",
                    "os": "android",
                    "compliance": {},
                    "serial_number": "125ffe54",
                    "certificate": "",
                    "admins": "",
                    "users": ""
                }
            },
            "machine_compliance_policies": ""
        },
        "MachineGroup2_laptops": {
            "machines": {
                "Machine2": {
                    "id": "2222",
                    "model": "del 5440",
                    "os": "win11",
                    "compliance": {},
                    "serial_number": "ddd5ffde54",
                    "certificate": "",
                    "admins": "testadminuser",
                    "users": "testuser"
                }
            },
            "machine_compliance_policies": ""
        }
    },
    "objects": {},
    "profiles": {},
    "policies": {},
    "SASE": {},
    "SDWAN": {
        "transports": {
            "1": "Internet",
            "2": "MPLS1"
        },
        "providers": {
            "1": "ISP1",
            "2": "ISP2"
        },
        "hubs": {},
        "site_groups": {},
        "sites": {
            "Site1": {
                "id": "111",
                "address": {},
                "tags": [],
                "policies": {
                    "qos": "qos policy 1",
                    "security": "qos policy 1",
                    "route": "qos policy 1",
                    "nat": "qos policy 1"
                },
                "underlays": {
                    "circuit1": {
                        "description": "",
                        "up_bw": 10,
                        "down_bw": 50,
                        "shaping": true,
                        "metered": false,
                        "underlay template"
                    },
                },
            },
        },
    },
    "events": {},
    "integrations": {}
}