# C2 Framework Architecture

## System Overview

This educational C2 (Command and Control) framework demonstrates the fundamental architecture used in red team operations and penetration testing.

## Components

### 1. C2 Server ([`c2_server.py`](c2_server.py:1))

The server is the central command hub that:
- Listens for incoming agent connections
- Manages multiple simultaneous agents
- Provides an interactive command interface
- Dispatches commands to agents
- Receives and displays command results

**Key Classes:**
- [`C2Server`](c2_server.py:13) - Main server class handling all operations

**Key Methods:**
- [`start()`](c2_server.py:23) - Initialize and start the server
- [`handle_new_client()`](c2_server.py:47) - Process new agent connections
- [`send_command()`](c2_server.py:77) - Send commands to specific agents
- [`command_interface()`](c2_server.py:127) - Interactive CLI for operators

### 2. C2 Agent ([`c2_agent.py`](c2_agent.py:1))

The agent is deployed on target systems and:
- Connects to the C2 server
- Sends system information beacon
- Receives commands from the server
- Executes commands on the local system
- Returns results to the server

**Key Classes:**
- [`C2Agent`](c2_agent.py:14) - Main agent class

**Key Methods:**
- [`connect()`](c2_agent.py:30) - Establish connection to C2 server
- [`execute_command()`](c2_agent.py:60) - Execute system commands
- [`run()`](c2_agent.py:93) - Main agent loop

## Communication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     C2 Communication Flow                       │
└─────────────────────────────────────────────────────────────────┘

1. INITIAL CONNECTION
   ┌─────────┐                                    ┌─────────┐
   │  Agent  │────────── TCP Connect ────────────►│ Server  │
   └─────────┘                                    └─────────┘

2. BEACON (System Info)
   ┌─────────┐                                    ┌─────────┐
   │  Agent  │────── JSON: System Info ──────────►│ Server  │
   └─────────┘                                    └─────────┘
                                                   │
                                                   ├─ Store agent info
                                                   └─ Assign agent ID

3. COMMAND EXECUTION
   ┌─────────┐                                    ┌─────────┐
   │  Agent  │◄────── JSON: Command ──────────────│ Server  │
   └─────────┘                                    └─────────┘
       │
       ├─ Parse command
       ├─ Execute on system
       └─ Capture output

4. RESULT RETURN
   ┌─────────┐                                    ┌─────────┐
   │  Agent  │────── JSON: Result ────────────────►│ Server  │
   └─────────┘                                    └─────────┘
                                                   │
                                                   └─ Display to operator
```

## Data Structures

### Beacon Message (Agent → Server)
```json
{
  "hostname": "target-machine",
  "platform": "Linux",
  "platform_release": "5.15.0",
  "platform_version": "#1 SMP",
  "architecture": "x86_64",
  "processor": "Intel Core i7",
  "username": "user",
  "timestamp": "2026-02-05T02:45:00.123456"
}
```

### Command Message (Server → Agent)
```json
{
  "command": "whoami",
  "timestamp": "2026-02-05T02:45:10.123456"
}
```

### Result Message (Agent → Server)
```json
{
  "success": true,
  "output": "username\n",
  "return_code": 0,
  "timestamp": "2026-02-05T02:45:10.234567"
}
```

## Network Protocol

### Transport Layer
- **Protocol**: TCP
- **Default Port**: 4444
- **Encoding**: UTF-8
- **Format**: JSON

### Connection Lifecycle

```
Agent Lifecycle:
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Connect    │◄──── Retry on failure (5 attempts)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Send Beacon  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Wait for    │
│  Command    │◄──────┐
└──────┬──────┘       │
       │              │
       ▼              │
┌─────────────┐       │
│  Execute    │       │
└──────┬──────┘       │
       │              │
       ▼              │
┌─────────────┐       │
│Send Result  │───────┘
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Disconnect  │
└─────────────┘
```

## Threading Model

### Server Threading
```
Main Thread
├── Accept Connections Loop
│   └── Spawn: Client Handler Thread (per agent)
│
└── Command Interface Thread
    └── Process operator commands
```

### Agent Threading
```
Main Thread
├── Connect to Server
├── Send Beacon
└── Command Loop
    ├── Receive Command
    ├── Execute Command
    └── Send Result
```

## Security Considerations

### Current Implementation (Educational)
- ❌ No encryption (plaintext communication)
- ❌ No authentication
- ❌ No obfuscation
- ❌ No persistence mechanisms
- ❌ No evasion techniques

### Production C2 Features
- ✅ TLS/SSL encryption
- ✅ Mutual authentication (certificates)
- ✅ Traffic obfuscation (HTTP/HTTPS/DNS)
- ✅ Jitter and sleep timers
- ✅ Domain fronting
- ✅ Payload encryption
- ✅ Anti-forensics
- ✅ Process injection
- ✅ Privilege escalation

## Extension Ideas

### 1. Enhanced Communication
```python
# Add encryption
from cryptography.fernet import Fernet

# Add HTTP/HTTPS protocol
# Add DNS tunneling
# Add WebSocket support
```

### 2. Advanced Features
```python
# File upload/download
def upload_file(self, local_path, remote_path):
    pass

# Screenshot capture
def capture_screenshot(self):
    pass

# Keylogging
def start_keylogger(self):
    pass

# Process management
def list_processes(self):
    pass
```

### 3. Persistence
```python
# Registry keys (Windows)
# Cron jobs (Linux)
# Launch agents (macOS)
# Service installation
```

### 4. Evasion
```python
# Process hollowing
# DLL injection
# Reflective loading
# Anti-VM detection
```

## Comparison with Real C2 Frameworks

| Feature | This Framework | Cobalt Strike | Metasploit | Sliver |
|---------|---------------|---------------|------------|--------|
| Encryption | ❌ | ✅ | ✅ | ✅ |
| Multi-protocol | ❌ | ✅ | ✅ | ✅ |
| GUI | ❌ | ✅ | ✅ | ✅ |
| Payload generation | ❌ | ✅ | ✅ | ✅ |
| Post-exploitation | ❌ | ✅ | ✅ | ✅ |
| Evasion | ❌ | ✅ | ✅ | ✅ |
| Team server | ❌ | ✅ | ❌ | ✅ |

## Learning Path

1. **Understand this basic framework**
2. **Add encryption** (TLS/SSL)
3. **Implement HTTP/HTTPS** protocol
4. **Add file transfer** capabilities
5. **Study real frameworks** (Metasploit, Sliver)
6. **Practice in labs** (HackTheBox, TryHackMe)
7. **Learn defense** (detection, prevention)

## References

- [MITRE ATT&CK - Command and Control](https://attack.mitre.org/tactics/TA0011/)
- [Cobalt Strike Documentation](https://www.cobaltstrike.com/help)
- [Metasploit Framework](https://www.metasploit.com/)
- [Sliver C2](https://github.com/BishopFox/sliver)

---

**Remember**: This is for educational purposes. Always practice ethical hacking! 🎓🔒
