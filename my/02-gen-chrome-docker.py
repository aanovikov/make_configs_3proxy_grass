import glob
import re

def read_login_password():
    # Читаем логин и пароль из файла 'logospass.txt'
    with open('logopass.txt', 'r') as file:
        login, password = file.read().strip().split(':')
    return login, password

def generate_individual_docker_composes():
    config_files = glob.glob('*_config.txt')  # Ищем все файлы конфигурации в текущей директории
    login, password = read_login_password()   # Читаем логин и пароль из файла

    for file in config_files:
        host_name = file.replace('_config.txt', '')  # Получаем имя хоста из имени файла
        docker_compose_filename = f"{host_name}_{login}.yml"  # Имя файла Docker Compose, включая логин пользователя

        compose_content = ['version: "3.8"', 'services:']  # Начинаем с версии и блока сервисов

        with open(file, 'r') as f:
            lines = f.readlines()

        # Фильтруем строки с прокси и извлекаем необходимую информацию
        proxy_lines = [line for line in lines if 'proxy' in line]

        for line in proxy_lines:
            port = re.search(r'-p(\d+)', line).group(1)
            interface_name = re.search(r'-Do(id\d+)', line).group(1)
            
            # Формируем конфигурацию Docker для каждого интерфейса и порта
            compose_content.append(f"  {interface_name}:")
            compose_content.append("    image: grass:latest")
            compose_content.append(f"    container_name: {interface_name}")
            compose_content.append("    environment:")
            compose_content.append(f"      - HTTP_PROXY=http://host:{port}")
            compose_content.append(f"      - HTTPS_PROXY=http://host:{port}")
            compose_content.append("      - NO_PROXY=localhost,127.0.0.0/8")
            compose_content.append(f"      - LOGIN={login}")
            compose_content.append(f"      - PASS={password}")
            compose_content.append(f"      - NODE_ID={interface_name}")
            compose_content.append("    mem_limit: 500m")
            compose_content.append("    restart: on-failure:5")
            compose_content.append("    logging:")
            compose_content.append("      driver: json-file")
            compose_content.append("      options:")
            compose_content.append("        max-size: '20m'")
            compose_content.append("        max-file: '3'")
            compose_content.append("    networks:")
            compose_content.append("      - grass")
            compose_content.append("    extra_hosts:")
            compose_content.append("      - host.docker.internal:host-gateway")

        # Добавляем блок networks в конце файла
        compose_content.extend([
            "networks:",
            "  grass:",
            "    external: true"
        ])

        # Записываем в файл docker-compose.yml, специфичный для каждого хоста
        with open(docker_compose_filename, 'w') as f:
            f.write('\n'.join(compose_content))
        print(f'Файл {docker_compose_filename} успешно создан.')

generate_individual_docker_composes()