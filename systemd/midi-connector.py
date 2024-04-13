#!/usr/bin/python
import subprocess
import time
import re

def connect(port):
    result = subprocess.run(["aconnect", "20:0", port], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = (result.stdout or "") + (result.stderr or "")

    print(f"output={output}")

    return result.returncode == 0 or "Connection is already subscribed" in output

def check_midi_connections(source_client, target_clients):
    result = subprocess.run(['aconnect', '-l'], stdout=subprocess.PIPE, text=True)
    output = result.stdout

    all_connected = True

    for client in target_clients:
        client_pattern = f"client {client}: .*?\n *0 .*\n(.*)"
        client_match = re.search(client_pattern, output)
        if client_match:
            connections = client_match.group(1)
            if not re.search(f"Connected From:.*{source_client}:0", connections):
                print(f"Client {client} is not connected from {source_client}:0")
                all_connected = False
                break
        else:
            print(f"Client {client} not found or has no connection details.")
            all_connected = False
            break

    return all_connected

def monitor_connection():
    connection_active = False
    while True:
        time.sleep(1)
        result = subprocess.check_output(["aconnect", "-l"])
        if check_midi_connections('20', ['128', '129']):
            if not connection_active:
                print("Connections are active 👍")
                connection_active = True
        else:
            print("Connection lost. Reconnecting...")
            break

while True:
    print("Starting MIDI connector")
    if connect("128:0") and connect("129:0"):
        print("Connected successfully to both.")
        monitor_connection()
    else:
        print("Failed to connect to one or both devices. Retrying in 1 second...")
        time.sleep(1)
