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

# Список начальных подсетей
start_subnets = [
    "10.10.240.0/29",
    "10.10.224.0/29", 
    "10.10.208.0/29", 
    "10.10.192.0/29", 
    "10.10.176.0/29"
]

ports = 16  # Количество PON портов
subscribers_per_port = 32  # Количество абонентов на порт

for i, start_subnet in enumerate(start_subnets, start=1):
    if start_subnet:
        subnets = calculate_subnets(start_subnet, ports, subscribers_per_port)
        file_name = f'Bel-SUM-IX_olt_{i}.yaml'
        with open(file_name, 'w') as file:
            yaml.dump(subnets, file, default_flow_style=False)
        print(f"Субсети были успешно записаны в файл '{file_name}'")
