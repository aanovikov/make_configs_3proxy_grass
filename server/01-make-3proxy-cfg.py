import glob
import re

def read_details():
    with open('details.txt', 'r') as file:
        details = file.readlines()
    return [detail.strip().split(':') for detail in details]

def generate_3proxy_config():
    details = read_details()
    country_codes = {detail[0] for detail in details}
    print("Available country codes:", ', '.join(country_codes))
    
    country_code = input("Enter a country code: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    selected_details = [detail for detail in details if detail[0] == country_code]

    if not selected_details:
        print("No details found for the selected country code.")
        return

    config_lines = [f"#### {country_code.upper()}"]
    for detail in selected_details:
        _, address, login, password = detail
        for port in range(start_port, end_port + 1):
            config_lines.append("auth iponly")
            config_lines.append("allow * 127.0.0.1,172.0.0.0/8,49.12.86.244")
            config_lines.append(f"parent 1000 http {address} {port} {login} {password}")
            config_lines.append(f"proxy -n -a -p{port}")
            config_lines.append("flush")

    config_content = '\n'.join(config_lines)
    config_filename = f"{country_code.lower()}_3proxy.cfg"
    
    # Записываем конфигурацию в файл
    with open(config_filename, 'w') as file:
        file.write(config_content)
    
    print(f"Configuration has been saved to {config_filename}")

generate_3proxy_config()