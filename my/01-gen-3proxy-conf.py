def generate_3proxy_configs(file_path):
    initial_port = 10000  # Начальный порт для первого хоста
    ports_per_host = 40   # Количество портов выделенных для каждого хоста

    # Читаем данные из файла
    try:
        with open(file_path, 'r') as file:
            hosts_data = file.read().splitlines()
    except FileNotFoundError:
        print(f"Ошибка: файл не найден - {file_path}")
        return

    # Создаем словарь для хранения информации о хостах и интерфейсах
    host_interfaces = {}
    for entry in hosts_data:
        host, interface_id = entry.split(';')
        if host not in host_interfaces:
            host_interfaces[host] = []
        host_interfaces[host].append(interface_id)

    port_start = initial_port  # Инициализируем начальный порт для первого хоста

    # Генерируем и сохраняем конфигурационные файлы для каждого хоста
    for host, interfaces in host_interfaces.items():
        config_lines = [
            "flush",
            "auth iponly",
            "allow * 192.168.1.70,192.168.1.65,192.168.1.5,192.168.1.14,127.0.0.1,172.0.0.0/8"
        ]  # Общие настройки только один раз в начале файла

        current_port = port_start  # Начальный порт для текущего хоста

        for interface_id in interfaces:
            config_lines.append(f"proxy -n -a -p{current_port} -Do{interface_id}")
            current_port += 1  # Увеличиваем порт на 1 для следующего интерфейса
        
        # Записываем конфигурацию в файл, специфичный для каждого хоста
        with open(f"{host}_config.txt", 'w') as config_file:
            config_file.write('\n'.join(config_lines))

        print(f"Конфигурация для {host} сохранена в файл {host}_config.txt")
        
        port_start += ports_per_host  # Увеличиваем начальный порт на количество портов на хост

# Путь к файлу с данными о хостах
file_path = 'hosts_data.txt'
generate_3proxy_configs(file_path)