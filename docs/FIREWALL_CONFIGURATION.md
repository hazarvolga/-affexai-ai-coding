# Firewall Configuration

## Overview
This document describes the firewall configuration for the AI Coding Platform on Oracle Cloud instance-hulyaekiz.

## Port Configuration

### Public Ports (Exposed to Internet)
- **80 (HTTP)**: Handled by Traefik/Coolify proxy, redirects to HTTPS
- **443 (HTTPS)**: Handled by Traefik/Coolify proxy for secure web access
- **8000 (HTTP)**: Coolify dashboard access

### Internal Ports (Docker Network Only)
- **11434**: Ollama API (accessible only within ai-coding-network)
- **3000**: OpenHands UI (proxied through Traefik)

## Current Firewall Rules

### Oracle Cloud Security List
The following ports are allowed in the Oracle Cloud VCN Security List:
- Ingress: 80, 443, 8000 (TCP)
- Egress: All traffic allowed

### iptables Rules
```bash
# View current rules
sudo iptables -L -n

# Key rules:
# - Port 80: ACCEPT (HTTP)
# - Port 443: ACCEPT (HTTPS)
# - Port 8000: ACCEPT (Coolify)
# - Port 11434: ACCEPT from Docker network only
# - Port 3000: ACCEPT from Docker network only
```

## Security Best Practices

### ✅ Implemented
1. **HTTPS Enforcement**: All web traffic uses HTTPS via Let's Encrypt
2. **Internal Services**: Ollama and OpenHands are not directly exposed
3. **Reverse Proxy**: Traefik handles all external traffic
4. **Docker Network Isolation**: Services communicate via internal Docker network

### 🔒 Recommendations
1. **Restrict Coolify Access**: Consider IP whitelisting for port 8000
2. **SSH Key Only**: Disable password authentication (already configured)
3. **Regular Updates**: Keep Docker and system packages updated
4. **Monitoring**: Use health check scripts to detect anomalies

## Verification Commands

```bash
# Check open ports
sudo netstat -tulpn | grep LISTEN

# Check iptables rules
sudo iptables -L -n -v

# Check Docker network
sudo docker network inspect ai-coding-network

# Test external access
curl -I https://ai.fpvlovers.com.tr
curl -I https://coolify.fpvlovers.com.tr
```

## Firewall Management

### Oracle Cloud Console
1. Navigate to: Networking → Virtual Cloud Networks
2. Select your VCN
3. Click on Security Lists
4. Modify ingress/egress rules as needed

### iptables (Server Level)
```bash
# Add rule to allow port
sudo iptables -A INPUT -p tcp --dport PORT -j ACCEPT

# Save rules (Ubuntu)
sudo netfilter-persistent save

# Reload rules
sudo netfilter-persistent reload
```

## Emergency Access

If you get locked out:
1. Access via Oracle Cloud Console → Instance → Console Connection
2. Login with SSH key
3. Review and fix iptables rules
4. Restart networking: `sudo systemctl restart networking`

---
**Requirements Validated**: 9.1, 9.4
**Last Updated**: 2025-11-29
