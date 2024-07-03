import glob
import re

def read_logopass():
    with open('logopass.txt', 'r') as file:
        data = [line.strip().split(':') for line in file.readlines()]
    return data

def select_login():
    logopass = read_logopass()
    print("Available logins:")
    for entry in logopass:
        print(f"{entry[0]}: {entry[1]}")
    num = input("Enter the number for login: ")
    selected = next((item for item in logopass if item[0] == num), None)
    return selected

def read_details():
    with open('details.txt', 'r') as file:
        details = file.read().strip().split()
    countries = set(detail.split(':')[0] for detail in details)
    print("Available country codes:", ', '.join(countries))
    return details

def get_ports_for_country(country_code):
    with open(f"{country_code.lower()}_3proxy.cfg", 'r') as file:
        content = file.readlines()
    ports = [re.search(r'-p(\d+)', line).group(1) for line in content if line.startswith('proxy')]
    return ports

def generate_docker_compose(login, ports, country_code):
    filename = f"{country_code.lower()}_{login[1]}_{ports[0]}-{ports[-1]}.yml"
    with open(filename, 'w') as file:
        file.write('version: "3.8"\n')
        file.write('services:\n')
        for port in ports:
            service_name = f"{country_code.lower()}{port}"
            file.write(f"  {service_name}:\n")
            file.write("    image: grass:latest\n")
            file.write(f"    container_name: {service_name}\n")
            file.write("    environment:\n")
            file.write(f"      - HTTP_PROXY=http://host.docker.internal:{port}\n")
            file.write(f"      - HTTPS_PROXY=http://host.docker.internal:{port}\n")
            file.write("      - NO_PROXY=localhost,127.0.0.0/8\n")
            file.write(f"      - LOGIN={login[1]}\n")
            file.write(f"      - PASS={login[2]}\n")
            file.write(f"      - NODE_ID={service_name}\n")
            file.write("    mem_limit: 500m\n")
            file.write("    restart: on-failure:5\n")
            file.write("    logging:\n")
            file.write("      driver: json-file\n")
            file.write("      options:\n")
            file.write("        max-size: '20m'\n")
            file.write("        max-file: '3'\n")
            file.write("    networks:\n")
            file.write("      - grass\n")
            file.write("    extra_hosts:\n")
            file.write("      - host.docker.internal:host-gateway\n")
        file.write("networks:\n")
        file.write("  grass:\n")
        file.write("    external: true\n")
    print(f"Docker compose file created: {filename}")

def main():
    login = select_login()
    if login:
        details = read_details()
        country_code = input("Enter the country code: ")
        ports = get_ports_for_country(country_code)
        generate_docker_compose(login, ports, country_code)
    else:
        print("No valid login selected.")

if __name__ == "__main__":
    main()