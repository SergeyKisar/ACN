import yaml
from ipaddress import ip_network

def calculate_subnets(start_subnet, ports, subscribers_per_port):
    start_net = ip_network(start_subnet)
    subnet_size = start_net.num_addresses
    current_address = start_net.network_address

    subnets = {}
    for port in range(1, ports + 1):
        for subscriber in range(1, subscribers_per_port + 1):
            key = f"Pon_{port}_{subscriber}"
            new_subnet = ip_network(f"{current_address}/{start_net.prefixlen}")
            subnets[key] = str(new_subnet)
            current_address += subnet_size

    return subnets

start_subnet = "10.2.176.0/29"  # Начальная подсеть
ports = 16  # Количество PON портов
subscribers_per_port = 32  # Количество абонентов на порт

subnets = calculate_subnets(start_subnet, ports, subscribers_per_port)

with open('Bel-TOL-IX_olt_5.yaml', 'w') as file:
    yaml.dump(subnets, file, default_flow_style=False)
