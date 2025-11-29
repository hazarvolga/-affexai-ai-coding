# Oracle Cloud Instance Status - instance-hulyaekiz

## Instance Details
- **Instance Name**: instance-hulyaekiz
- **Public IP**: 161.118.171.201
- **SSH Key**: `ssh-key-2025-09-20.key`
- **SSH Command**: `ssh -i instance-hulya/ssh-key-2025-09-20.key ubuntu@161.118.171.201`

## Prerequisites Verification (Completed)

### ✓ Docker Installation
- **Version**: Docker version 28.4.0, build d8eb465
- **Status**: Installed and operational
- **Verification**: `docker --version`

### ✓ Disk Space
- **Total**: 78GB
- **Used**: 20GB
- **Available**: 58GB (26% used)
- **Status**: Exceeds minimum requirement of 30GB
- **Verification**: `df -h /`

### ✓ Docker Compose
- **Version**: Docker Compose version v2.39.4
- **Status**: Installed and operational
- **Verification**: `docker compose version`

### ✓ Docker Network
- **Network Name**: ai-coding-network
- **Driver**: bridge
- **Subnet**: 10.0.5.0/24
- **Status**: Network exists and is ready for use
- **Verification**: `sudo docker network ls | grep ai-coding-network`

## Existing Services
The instance already has Coolify installed and running:
- **Coolify Dashboard**: http://161.118.171.201:8000
- **Domain**: coolify.fpvlovers.com.tr

## Next Steps
The instance is ready for AI Coding Platform deployment:
1. Deploy Ollama service (Task 2)
2. Deploy OpenHands service (Task 3)
3. Configure GitHub integration (Task 4)
4. Configure Traefik reverse proxy and domain (Task 5)

## Verification Script
A verification script has been created at `~/verify-prerequisites.sh` on the instance.
Run it anytime to verify prerequisites: `./verify-prerequisites.sh`

---
**Last Updated**: 2025-11-29
**Verified By**: Kiro AI Agent
**Requirements Validated**: 8.1, 8.3
