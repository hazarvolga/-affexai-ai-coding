# Troubleshooting Guide

## Quick Diagnostics

Run the system health check first:
```bash
bash ~/health-check-system.sh
```

This will identify most common issues automatically.

## Common Issues

### 1. OpenHands UI Not Accessible

#### Symptoms
- Cannot access https://ai.fpvlovers.com.tr
- Browser shows "Connection refused" or timeout
- 502 Bad Gateway error

#### Diagnosis
```bash
# Check if OpenHands container is running
sudo docker ps | grep openhands

# Check OpenHands logs
sudo docker logs openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Test local access
curl -I http://localhost:3000
```

#### Solutions

**Container not running:**
```bash
# Restart via Coolify UI (recommended)
# Or manually:
sudo docker start openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

**Container running but not responding:**
```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Restart OpenHands
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

**DNS/Domain issues:**
```bash
# Verify DNS resolution
nslookup ai.fpvlovers.com.tr

# Should return: 161.118.171.201
# If not, update DNS A record
```

**SSL Certificate issues:**
```bash
# Check certificate in Coolify UI
# Navigate to: Application → Domains → Check SSL status
# If expired, click "Renew Certificate"
```

---

### 2. Ollama Not Responding

#### Symptoms
- OpenHands shows "Cannot connect to LLM"
- AI responses timeout
- Model loading errors

#### Diagnosis
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Check container
sudo docker ps | grep ollama

# View logs
sudo docker logs ollama-kogccog8g0ok80w0kgcoc4ck-112840189768
```

#### Solutions

**Container not running:**
```bash
# Start Ollama
sudo docker start ollama-kogccog8g0ok80w0kgcoc4ck-112840189768
```

**Model not loaded:**
```bash
# List available models
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list

# Pull model if missing
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama pull deepseek-coder-v2:16b
```

**Out of memory:**
```bash
# Check memory usage
free -h

# If memory is full, restart Ollama
sudo docker restart ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# Consider using smaller model
# Edit environment: LLM_MODEL=ollama/qwen2.5-coder:7b
```

---

### 3. GitHub Integration Not Working

#### Symptoms
- "GitHub authentication failed" error
- Cannot push to repositories
- Token validation fails

#### Diagnosis
```bash
# Check if token is set
echo $GITHUB_TOKEN

# Test token validity
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check OpenHands environment
sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 env | grep GITHUB
```

#### Solutions

**Token not set:**
```bash
# Set in Coolify UI:
# 1. Go to Application → Environment Variables
# 2. Add GITHUB_TOKEN with your token
# 3. Restart application

# Or set in .env file:
echo "GITHUB_TOKEN=ghp_your_token_here" >> ~/.env
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

**Token expired or invalid:**
```bash
# Generate new token at: https://github.com/settings/tokens
# Required scopes: repo, workflow
# Update in Coolify or .env
# Restart OpenHands
```

**Token has insufficient permissions:**
```bash
# Go to: https://github.com/settings/tokens
# Edit token
# Ensure these scopes are checked:
#   - repo (all)
#   - workflow
# Save and restart OpenHands
```

---

### 4. Slow AI Responses

#### Symptoms
- AI takes very long to respond
- Timeouts during code generation
- High CPU/memory usage

#### Diagnosis
```bash
# Check system resources
htop  # or: top

# Check Docker stats
sudo docker stats

# Check model size
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list
```

#### Solutions

**High memory usage:**
```bash
# Switch to smaller model
# In Coolify, set: LLM_MODEL=ollama/qwen2.5-coder:7b
# Restart OpenHands

# Or pull and use smaller model
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama pull qwen2.5-coder:7b
```

**CPU bottleneck:**
```bash
# Check if other processes are consuming CPU
ps aux --sort=-%cpu | head -10

# Stop unnecessary services
# Upgrade to instance with more CPU cores
```

**Disk I/O issues:**
```bash
# Check disk usage
df -h

# Check I/O wait
iostat -x 1 5

# Clean up if needed
sudo docker system prune -a
```

---

### 5. Workspace Files Not Persisting

#### Symptoms
- Projects disappear after restart
- Cannot find previously created files
- Workspace appears empty

#### Diagnosis
```bash
# Check volume mounts
sudo docker inspect openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 | grep -A 10 Mounts

# Check workspace directory
sudo ls -la /var/lib/docker/volumes/openhands-workspace/_data/

# Check disk space
df -h
```

#### Solutions

**Volume not mounted:**
```bash
# Verify in docker-compose.yml or Coolify config
# Should have: /opt/workspace mounted to volume

# Recreate container with proper mounts via Coolify
```

**Disk full:**
```bash
# Check space
df -h

# Clean up Docker
sudo docker system prune -a

# Remove old images
sudo docker image prune -a
```

**Permission issues:**
```bash
# Fix permissions
sudo chown -R 1000:1000 /var/lib/docker/volumes/openhands-workspace/_data/
```

---

### 6. SSL Certificate Issues

#### Symptoms
- Browser shows "Not Secure"
- Certificate expired warning
- HTTPS not working

#### Diagnosis
```bash
# Check certificate
openssl s_client -connect ai.fpvlovers.com.tr:443 -servername ai.fpvlovers.com.tr

# Check in Coolify UI
# Navigate to: Application → Domains
```

#### Solutions

**Certificate expired:**
```bash
# In Coolify UI:
# 1. Go to Application → Domains
# 2. Click "Renew Certificate"
# 3. Wait for renewal to complete
```

**Certificate not generated:**
```bash
# Verify DNS points to correct IP
nslookup ai.fpvlovers.com.tr

# In Coolify, regenerate certificate:
# 1. Remove domain
# 2. Re-add domain
# 3. Enable SSL
# 4. Wait for Let's Encrypt
```

---

### 7. High Disk Usage

#### Symptoms
- Disk space warning
- Services failing to start
- Cannot create new files

#### Diagnosis
```bash
# Check disk usage
df -h

# Find large directories
du -sh /* | sort -h

# Check Docker usage
sudo docker system df
```

#### Solutions

**Clean Docker resources:**
```bash
# Remove unused containers
sudo docker container prune

# Remove unused images
sudo docker image prune -a

# Remove unused volumes (CAREFUL!)
sudo docker volume prune

# Complete cleanup
sudo docker system prune -a --volumes
```

**Clean Ollama models:**
```bash
# List models
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list

# Remove unused models
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama rm <model-name>
```

**Clean logs:**
```bash
# Truncate Docker logs
sudo truncate -s 0 /var/lib/docker/containers/*/*-json.log

# Or configure log rotation in /etc/docker/daemon.json:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

---

### 8. Container Keeps Restarting

#### Symptoms
- Container status shows "Restarting"
- Services unavailable
- Logs show crash loop

#### Diagnosis
```bash
# Check container status
sudo docker ps -a | grep -E "openhands|ollama"

# View recent logs
sudo docker logs --tail 100 <container-name>

# Check exit code
sudo docker inspect <container-name> | grep -A 5 State
```

#### Solutions

**Out of memory:**
```bash
# Check memory
free -h

# Increase swap if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

**Configuration error:**
```bash
# Check environment variables in Coolify
# Verify all required variables are set
# Check for typos in variable names

# View container environment
sudo docker inspect <container-name> | grep -A 20 Env
```

**Port conflict:**
```bash
# Check if port is already in use
sudo netstat -tulpn | grep -E "3000|11434"

# Stop conflicting service or change port
```

---

## Debugging Commands

### View Logs
```bash
# OpenHands logs (last 100 lines)
sudo docker logs --tail 100 openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Ollama logs (follow in real-time)
sudo docker logs -f ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# All containers
sudo docker logs --tail 50 $(sudo docker ps -q)
```

### Check Service Status
```bash
# List all containers
sudo docker ps -a

# Check specific service
sudo docker ps | grep openhands

# Check restart count
sudo docker inspect <container-name> | grep RestartCount
```

### Network Debugging
```bash
# Test internal connectivity
sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 curl http://ollama:11434/api/tags

# Check network
sudo docker network inspect ai-coding-network

# Test external access
curl -I https://ai.fpvlovers.com.tr
```

### Resource Monitoring
```bash
# Real-time resource usage
sudo docker stats

# System resources
htop

# Disk I/O
iostat -x 1

# Network traffic
iftop
```

---

## Performance Optimization

### Optimize Ollama
```bash
# Use smaller model for faster responses
# Set in Coolify: LLM_MODEL=ollama/qwen2.5-coder:7b

# Preload model to reduce first-request latency
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama run qwen2.5-coder:7b "test"
```

### Optimize Docker
```bash
# Enable BuildKit
echo '{"features": {"buildkit": true}}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker

# Limit log size
echo '{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

### Optimize System
```bash
# Increase file descriptors
echo "fs.file-max = 65536" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Optimize network
echo "net.core.somaxconn = 1024" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## Emergency Recovery

### Complete System Reset
```bash
# ⚠️ WARNING: This will delete all data!

# Stop all services
sudo docker stop $(sudo docker ps -q)

# Remove containers
sudo docker rm $(sudo docker ps -a -q)

# Remove volumes (DELETES ALL DATA!)
sudo docker volume rm ollama-data openhands-workspace

# Redeploy via Coolify
# Or: docker-compose up -d
```

### Backup Before Reset
```bash
# Backup workspace
sudo tar -czf workspace-backup-$(date +%Y%m%d).tar.gz /var/lib/docker/volumes/openhands-workspace/

# Backup Ollama models
sudo tar -czf ollama-backup-$(date +%Y%m%d).tar.gz /var/lib/docker/volumes/ollama-data/

# Copy backups to safe location
scp workspace-backup-*.tar.gz user@backup-server:/backups/
```

### Restore from Backup
```bash
# Stop services
sudo docker stop openhands-* ollama-*

# Restore workspace
sudo tar -xzf workspace-backup-YYYYMMDD.tar.gz -C /

# Restore Ollama
sudo tar -xzf ollama-backup-YYYYMMDD.tar.gz -C /

# Start services
sudo docker start ollama-* openhands-*
```

---

## Getting Help

### Information to Collect
When reporting issues, include:
1. Output of `bash ~/health-check-system.sh`
2. Recent logs: `sudo docker logs --tail 100 <container-name>`
3. System info: `uname -a && free -h && df -h`
4. Docker info: `sudo docker ps && sudo docker version`

### Log Locations
- **OpenHands**: `sudo docker logs openhands-*`
- **Ollama**: `sudo docker logs ollama-*`
- **Coolify**: Coolify UI → Logs tab
- **System**: `/var/log/syslog`

### Useful Commands Reference
```bash
# Quick health check
bash ~/health-check-system.sh

# View all containers
sudo docker ps -a

# Restart service
sudo docker restart <container-name>

# View logs
sudo docker logs -f <container-name>

# Check resources
sudo docker stats

# Clean up
sudo docker system prune -a
```

---
**Requirements Validated**: 10.3
**Last Updated**: 2025-11-29
