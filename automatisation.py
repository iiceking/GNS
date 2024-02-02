import json
import os

# Fonction pour convertir la préférence en valeur numérique
def p_number(preference):
    if preference == "low":
        return 100
    elif preference == "medium":
        return 200
    elif preference == "high":
        return 300
    else:
        return 0

# Fonction pour générer la configuration Cisco pour un routeur
def generate_cisco_config(router):
    config = []
    config.append(f"hostname {router['router_id']}")
    config.append("!")
    config.append(f"interface Loopback0")
    config.append(f" ip address {router['loopback']} {router['loopback_masque']}")
    config.append("!")

    for interface in router['interfaces']:
        if interface['enable'] == '1':
            config.append(f"interface {interface['interface_name']}")
            config.append(f" ip address {interface['ip_address']} {interface['subnet_mask']}")
            if router['iBGP_protocol'] == "RIP":
                config.append(" ip rip send version 2")
                config.append(" ip rip receive version 2")
            config.append("!")

    if router['iBGP_protocol'] == "OSPF":
        config.append(f"router ospf {router['router_id'][-1]}")
        config.append(f" network {router['ip']} 0.0.0.255 area 0")
        config.append("!")

    if router['eBGP'] == '1':
        preference = p_number(router.get('preference', 'medium'))
        config.append(f"router bgp {preference}")
        for interface_index in router['eBGP_interface']:
            interface = router['interfaces'][interface_index]
            config.append(f" network {interface['ip_address']} mask {interface['subnet_mask']}")
        config.append("!")

    return "\n".join(config)

# Lecture du fichier JSON d'intention
intent_file_path = "/home/user/config.json" # Remplacer par le chemin de votre fichier d'intention
with open(intent_file_path, 'r') as file:
    data = json.load(file)

# Génération des configurations Cisco
cisco_configs = {}
for router in data['routers']:
    cisco_configs[router['router_id']] = generate_cisco_config(router)

# Écriture des configurations dans des fichiers
output_dir = "/home/user/json" # Remplacer par votre chemin de dossier de sortie
for router_id, config in cisco_configs.items():
    with open(os.path.join(output_dir, f"{router_id}_config.txt"), "w") as file:
        file.write(config)

print("Les configurations Cisco ont été générées avec succès.")
