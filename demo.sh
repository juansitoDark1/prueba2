#!/bin/bash

# Educational C2 Framework Demo Script
# This script demonstrates the C2 framework in action

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        Educational C2 Framework - Demo Script            ║"
echo "║              For Educational Purposes Only                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "[-] Python 3 is required but not installed."
    exit 1
fi

echo "[+] Python 3 found: $(python3 --version)"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "[!] Cleaning up processes..."
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
    fi
    if [ ! -z "$AGENT_PID" ]; then
        kill $AGENT_PID 2>/dev/null
    fi
    echo "[+] Cleanup complete"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

echo "Demo Options:"
echo "1. Start C2 Server only"
echo "2. Start C2 Agent only (requires server IP)"
echo "3. Full demo (server + local agent)"
echo ""
read -p "Select option (1-3): " option

case $option in
    1)
        echo ""
        echo "[*] Starting C2 Server..."
        python3 c2_server.py
        ;;
    2)
        echo ""
        read -p "Enter C2 Server IP [127.0.0.1]: " server_ip
        server_ip=${server_ip:-127.0.0.1}
        read -p "Enter C2 Server Port [4444]: " server_port
        server_port=${server_port:-4444}
        echo ""
        echo "[*] Starting C2 Agent connecting to $server_ip:$server_port..."
        python3 c2_agent.py $server_ip $server_port
        ;;
    3)
        echo ""
        echo "[*] Starting Full Demo..."
        echo "[*] This will start both server and agent on localhost"
        echo ""
        
        # Start server in background
        echo "[+] Starting C2 Server..."
        python3 c2_server.py > /tmp/c2_server.log 2>&1 &
        SERVER_PID=$!
        echo "[+] Server PID: $SERVER_PID"
        
        # Wait for server to start
        sleep 2
        
        # Start agent in background
        echo "[+] Starting C2 Agent..."
        python3 c2_agent.py 127.0.0.1 4444 > /tmp/c2_agent.log 2>&1 &
        AGENT_PID=$!
        echo "[+] Agent PID: $AGENT_PID"
        
        # Wait for connection
        sleep 2
        
        echo ""
        echo "[+] Demo is running!"
        echo "[+] Server log: /tmp/c2_server.log"
        echo "[+] Agent log: /tmp/c2_agent.log"
        echo ""
        echo "To interact with the server, run in another terminal:"
        echo "  tail -f /tmp/c2_server.log"
        echo ""
        echo "Press Ctrl+C to stop the demo"
        
        # Keep script running
        wait
        ;;
    *)
        echo "[-] Invalid option"
        exit 1
        ;;
esac
