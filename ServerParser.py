import requests

def get_server_status(server_name):
    mcs = "https://api.mcstatus.io/v2/status/java/"
    try:
        response = requests.get(mcs + server_name)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

def parse_server(server_name, depth=0, max_depth=5):
    if depth > max_depth:
        print("Reached maximum recursion depth, stopping parsing.")
        return

    data = get_server_status(server_name)

    if data:
        is_online = data.get('online')
        srv_record = data.get('srv_record')

        if is_online:
            print(f"Server {server_name} is online.")
            if srv_record is not None:
                host = srv_record.get('host', '')
                port = srv_record.get('port', '')
                print("Retrieved host:", host)
                print("Retrieved port:", port)
                parse_server(f"{host}:{port}", depth + 1, max_depth)
            else:
                print("srv_record is Null, stopping recursive parsing.")
                ip = data.get('ip_address', '')
                port = data.get('port', '')
                print(f"IP Address: {ip}, Port: {port}")

                return True
        else:
            print(f"Server {server_name} is offline or does not exist.")
    else:
        print("Unable to retrieve server status.")

def main():
    initial_server = "mc.incrafttime.top"
    parse_server(initial_server)

if __name__ == "__main__":
    main()
