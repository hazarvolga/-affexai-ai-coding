# Maintenance Procedures

## Overview
This document outlines regular maintenance tasks to keep the AI Coding Platform running smoothly and securely.

## Maintenance Schedule

### Daily (Automated)
- ✅ Service health monitoring (via restart policies)
- ✅ Automatic service restart on failure
- ✅ SSL certificate auto-renewal checks

### Weekly (Manual - 15 minutes)
- [ ] Run system health check
- [ ] Review service logs for errors
- [ ] Check disk space usage
- [ ] Verify backup completion

### Monthly (Manual - 30 minutes)
- [ ] Update Docker images
- [ ] Review and rotate access logs
- [ ] Check for security updates
- [ ] Test backup restoration
- [ ] Review GitHub token expiration

### Quarterly (Manual - 1 hour)
- [ ] Rotate GitHub tokens
- [ ] Full system backup
- [ ] Performance review and optimization
- [ ] Security audit
- [ ] Update documentation

---

## Daily Maintenance

### Automated Tasks

These tasks are handled automatically by the system:

**Service Monitoring:**
- Docker restart policy: `unless-stopped`
- Automatic container restart on failure
- Health checks via Docker

**SSL Certificates:**
- Let's Encrypt auto-renewal via Coolify
- Certificate expiration monitoring
- Automatic HTTPS enforcement

**Verification:**
```bash
# Verify services are running
sudo docker ps | grep -E "openhands|ollama"

# Should show both containers with "Up" status
```

---

## Weekly Maintenance

### 1. System Health Check (5 minutes)

Run the comprehensive health check:
```bash
ssh ubuntu@161.118.171.201
bash ~/health-check-system.sh
```

**Expected output:**
- ✅ Ollama service is healthy
- ✅ OpenHands UI is healthy
- ✅ Disk usage < 80%
- ✅ Memory usage < 90%
- ✅ Docker is running
- ✅ System Status: HEALTHY

**If issues found:**
- Review [Troubleshooting Guide](TROUBLESHOOTING.md)
- Check service logs
- Restart affected services

### 2. Review Logs (5 minutes)

Check for errors or warnings:
```bash
# OpenHands logs (last 100 lines)
sudo docker logs --tail 100 openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 | grep -i error

# Ollama logs
sudo docker logs --tail 100 ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 | grep -i error

# System logs
sudo journalctl -u docker --since "1 week ago" | grep -i error
```

**Action items:**
- Document any recurring errors
- Investigate critical errors immediately
- Plan fixes for non-critical issues

### 3. Check Disk Space (2 minutes)

Monitor disk usage:
```bash
# Overall disk usage
df -h /

# Docker disk usage
sudo docker system df

# Large directories
du -sh /var/lib/docker/volumes/* | sort -h | tail -5
```

**Thresholds:**
- ⚠️ Warning: > 70% used
- 🚨 Critical: > 85% used

**If high usage:**
```bash
# Clean up Docker
sudo docker system prune -a

# Remove old logs
sudo journalctl --vacuum-time=7d
```

### 4. Verify Backups (3 minutes)

Check that backups are current:
```bash
# List recent backups
ls -lh ~/backups/ | tail -5

# Check backup age
find ~/backups/ -name "*.tar.gz" -mtime -7
```

**Expected:**
- At least one backup from last 7 days
- Backup size > 0 bytes

**If no recent backup:**
- Run manual backup (see Monthly Maintenance)

---

## Monthly Maintenance

### 1. Update Docker Images (10 minutes)

Keep services up to date:

**Via Coolify (Recommended):**
1. Login to https://coolify.fpvlovers.com.tr
2. Navigate to AI Coding Platform application
3. Click "Check for Updates"
4. Review changelog
5. Click "Update" if available
6. Monitor deployment logs
7. Verify services are healthy

**Manual Update:**
```bash
# Pull latest images
sudo docker pull ollama/ollama:latest
sudo docker pull ghcr.io/all-hands-ai/openhands:latest

# Restart services via Coolify
# Or manually:
sudo docker restart ollama-kogccog8g0ok80w0kgcoc4ck-112840189768
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Verify
bash ~/health-check-system.sh
```

**Rollback if issues:**
```bash
# Via Coolify: Click "Rollback" button
# Or manually restore from backup
```

### 2. Rotate Access Logs (5 minutes)

Manage log file sizes:
```bash
# Archive old logs
sudo journalctl --rotate
sudo journalctl --vacuum-time=30d

# Compress Docker logs
sudo find /var/lib/docker/containers -name "*.log" -exec gzip {} \;

# Clean old compressed logs
sudo find /var/lib/docker/containers -name "*.log.gz" -mtime +30 -delete
```

### 3. Security Updates (10 minutes)

Apply system security patches:
```bash
# Update package list
sudo apt update

# List available updates
sudo apt list --upgradable

# Apply security updates
sudo apt upgrade -y

# Reboot if kernel updated
sudo reboot  # Only if necessary
```

**After reboot:**
```bash
# Verify all services started
bash ~/health-check-system.sh
```

### 4. Test Backup Restoration (5 minutes)

Verify backups are valid:
```bash
# Create test directory
mkdir -p ~/backup-test

# Extract recent backup
tar -xzf ~/backups/workspace-backup-YYYYMMDD.tar.gz -C ~/backup-test

# Verify contents
ls -la ~/backup-test/var/lib/docker/volumes/openhands-workspace/_data/

# Clean up
rm -rf ~/backup-test
```

---

## Quarterly Maintenance

### 1. Rotate GitHub Tokens (15 minutes)

**Create new token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Set expiration: 90 days
4. Select scopes: `repo`, `workflow`
5. Generate and copy token

**Update token:**
```bash
# Via Coolify:
# 1. Go to Application → Environment Variables
# 2. Update GITHUB_TOKEN
# 3. Restart application

# Or update .env:
nano ~/.env
# Update GITHUB_TOKEN=new_token_here

# Restart OpenHands
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

**Verify:**
```bash
# Test new token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

**Revoke old token:**
1. Go to https://github.com/settings/tokens
2. Find old token
3. Click "Delete"

### 2. Full System Backup (20 minutes)

Create comprehensive backup:
```bash
# Create backup directory
mkdir -p ~/backups/quarterly-$(date +%Y%m%d)

# Backup workspace
sudo tar -czf ~/backups/quarterly-$(date +%Y%m%d)/workspace.tar.gz \
  /var/lib/docker/volumes/openhands-workspace/

# Backup Ollama models
sudo tar -czf ~/backups/quarterly-$(date +%Y%m%d)/ollama.tar.gz \
  /var/lib/docker/volumes/ollama-data/

# Backup configuration
cp ~/.env ~/backups/quarterly-$(date +%Y%m%d)/env.backup
cp ~/health-check-*.sh ~/backups/quarterly-$(date +%Y%m%d)/

# Backup documentation
tar -czf ~/backups/quarterly-$(date +%Y%m%d)/docs.tar.gz \
  ~/instance-hulyaekiz/docs/

# Create backup manifest
cat > ~/backups/quarterly-$(date +%Y%m%d)/MANIFEST.txt << EOF
Backup Date: $(date)
Server: instance-hulyaekiz (161.118.171.201)
Contents:
- workspace.tar.gz: OpenHands projects
- ollama.tar.gz: AI models
- env.backup: Environment variables
- health-check-*.sh: Health check scripts
- docs.tar.gz: Documentation
EOF

# Verify backup
ls -lh ~/backups/quarterly-$(date +%Y%m%d)/
```

**Store backup securely:**
```bash
# Copy to external storage
# Option 1: SCP to backup server
scp -r ~/backups/quarterly-$(date +%Y%m%d)/ user@backup-server:/backups/

# Option 2: Upload to cloud storage
# (Configure rclone or similar tool)

# Option 3: Download to local machine
# From your local machine:
scp -r ubuntu@161.118.171.201:~/backups/quarterly-$(date +%Y%m%d)/ ./backups/
```

### 3. Performance Review (15 minutes)

Analyze system performance:
```bash
# Collect metrics
echo "=== CPU Usage ===" > ~/performance-report.txt
top -bn1 | head -20 >> ~/performance-report.txt

echo -e "\n=== Memory Usage ===" >> ~/performance-report.txt
free -h >> ~/performance-report.txt

echo -e "\n=== Disk Usage ===" >> ~/performance-report.txt
df -h >> ~/performance-report.txt

echo -e "\n=== Docker Stats ===" >> ~/performance-report.txt
sudo docker stats --no-stream >> ~/performance-report.txt

echo -e "\n=== Network Connections ===" >> ~/performance-report.txt
sudo netstat -an | grep ESTABLISHED | wc -l >> ~/performance-report.txt

# Review report
cat ~/performance-report.txt
```

**Optimization opportunities:**
- High CPU: Consider smaller AI model
- High memory: Add swap or upgrade instance
- High disk: Clean up old data
- Slow responses: Review AI model choice

### 4. Security Audit (10 minutes)

Review security posture:
```bash
# Check open ports
sudo netstat -tulpn | grep LISTEN

# Expected ports:
# - 80, 443, 8000 (public)
# - 11434, 3000 (internal only)

# Check firewall rules
sudo iptables -L -n

# Review active tokens
# Go to: https://github.com/settings/tokens
# Verify only current token is active

# Check for security updates
sudo apt update
sudo apt list --upgradable | grep -i security

# Review Docker security
sudo docker scan ollama/ollama:latest
sudo docker scan ghcr.io/all-hands-ai/openhands:latest
```

**Security checklist:**
- [ ] Only necessary ports open
- [ ] HTTPS enforced on all web interfaces
- [ ] GitHub tokens rotated and valid
- [ ] No secrets in Git history
- [ ] System packages up to date
- [ ] Docker images up to date
- [ ] Firewall rules correct
- [ ] SSL certificates valid

---

## Backup Procedures

### Automated Backup Script

Create automated backup script:
```bash
cat > ~/backup-script.sh << 'EOF'
#!/bin/bash
# Automated backup script for AI Coding Platform

BACKUP_DIR=~/backups
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_PATH=$BACKUP_DIR/$DATE

# Create backup directory
mkdir -p $BACKUP_PATH

# Backup workspace
echo "Backing up workspace..."
sudo tar -czf $BACKUP_PATH/workspace.tar.gz \
  /var/lib/docker/volumes/openhands-workspace/ 2>/dev/null

# Backup Ollama (optional - large)
# echo "Backing up Ollama models..."
# sudo tar -czf $BACKUP_PATH/ollama.tar.gz \
#   /var/lib/docker/volumes/ollama-data/ 2>/dev/null

# Backup configuration
echo "Backing up configuration..."
cp ~/.env $BACKUP_PATH/env.backup 2>/dev/null

# Create manifest
cat > $BACKUP_PATH/MANIFEST.txt << MANIFEST
Backup Date: $(date)
Server: $(hostname)
IP: $(hostname -I | awk '{print $1}')
Disk Usage: $(df -h / | awk 'NR==2 {print $5}')
MANIFEST

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

echo "Backup completed: $BACKUP_PATH"
ls -lh $BACKUP_PATH/
EOF

chmod +x ~/backup-script.sh
```

**Schedule automated backups:**
```bash
# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-script.sh >> ~/backup.log 2>&1") | crontab -

# Verify crontab
crontab -l
```

### Restore Procedures

**Restore workspace:**
```bash
# Stop OpenHands
sudo docker stop openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Restore from backup
sudo tar -xzf ~/backups/YYYYMMDD/workspace.tar.gz -C /

# Start OpenHands
sudo docker start openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Verify
bash ~/health-check-system.sh
```

**Restore Ollama models:**
```bash
# Stop Ollama
sudo docker stop ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# Restore from backup
sudo tar -xzf ~/backups/YYYYMMDD/ollama.tar.gz -C /

# Start Ollama
sudo docker start ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# Verify models
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list
```

---

## Update Procedures

### Updating OpenHands

**Via Coolify (Recommended):**
1. Login to Coolify dashboard
2. Navigate to AI Coding Platform
3. Click "Check for Updates"
4. Review changelog
5. Click "Update"
6. Monitor deployment
7. Verify health check

**Manual update:**
```bash
# Pull latest image
sudo docker pull ghcr.io/all-hands-ai/openhands:latest

# Stop current container
sudo docker stop openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Remove old container
sudo docker rm openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Redeploy via Coolify
# Or manually with docker-compose
```

### Updating Ollama

```bash
# Pull latest image
sudo docker pull ollama/ollama:latest

# Restart container
sudo docker restart ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# Verify
curl http://localhost:11434/api/tags
```

### Updating AI Models

```bash
# Pull updated model
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 \
  ollama pull deepseek-coder-v2:16b

# Verify
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 \
  ollama list
```

---

## Rollback Procedures

### Rollback OpenHands

**Via Coolify:**
1. Go to Application → Deployments
2. Find previous successful deployment
3. Click "Rollback"
4. Confirm rollback
5. Monitor deployment
6. Verify health

**Manual rollback:**
```bash
# Stop current version
sudo docker stop openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Pull specific version
sudo docker pull ghcr.io/all-hands-ai/openhands:v0.x.x

# Update docker-compose.yml with specific version
# Redeploy
```

### Rollback Ollama

```bash
# Pull specific version
sudo docker pull ollama/ollama:0.x.x

# Update docker-compose.yml
# Restart service
```

---

## Monitoring and Alerts

### Set Up Monitoring

**Basic monitoring with cron:**
```bash
# Create monitoring script
cat > ~/monitor.sh << 'EOF'
#!/bin/bash
# Simple monitoring script

# Run health check
HEALTH=$(bash ~/health-check-system.sh 2>&1)

# Check if unhealthy
if echo "$HEALTH" | grep -q "DEGRADED"; then
    # Send alert (configure email or webhook)
    echo "ALERT: System unhealthy at $(date)" >> ~/alerts.log
    echo "$HEALTH" >> ~/alerts.log
fi
EOF

chmod +x ~/monitor.sh

# Run every 15 minutes
(crontab -l 2>/dev/null; echo "*/15 * * * * ~/monitor.sh") | crontab -
```

### Log Rotation

Configure log rotation:
```bash
sudo cat > /etc/logrotate.d/ai-coding-platform << 'EOF'
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
EOF
```

---

## Emergency Procedures

### Service Down

```bash
# Quick restart
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
sudo docker restart ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# Verify
bash ~/health-check-system.sh
```

### System Unresponsive

```bash
# Via Oracle Cloud Console:
# 1. Login to Oracle Cloud
# 2. Navigate to Compute → Instances
# 3. Select instance-hulyaekiz
# 4. Click "Reboot"
# 5. Wait for reboot
# 6. Verify services started
```

### Data Corruption

```bash
# Restore from latest backup
bash ~/restore-from-backup.sh YYYYMMDD

# Verify integrity
bash ~/health-check-system.sh
```

---

## Maintenance Checklist

### Weekly Checklist
- [ ] Run `bash ~/health-check-system.sh`
- [ ] Review logs for errors
- [ ] Check disk space (`df -h`)
- [ ] Verify backups exist

### Monthly Checklist
- [ ] Update Docker images
- [ ] Rotate access logs
- [ ] Apply security updates
- [ ] Test backup restoration
- [ ] Review GitHub token expiration

### Quarterly Checklist
- [ ] Rotate GitHub tokens
- [ ] Full system backup
- [ ] Performance review
- [ ] Security audit
- [ ] Update documentation
- [ ] Review and optimize resources

---
**Requirements Validated**: 10.4
**Last Updated**: 2025-11-29
