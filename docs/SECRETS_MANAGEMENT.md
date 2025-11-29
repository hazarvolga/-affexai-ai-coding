# Secrets Management Guide

## Overview
This guide explains how to securely manage secrets and credentials for the AI Coding Platform.

## Environment Variables

### Setup Instructions

1. **Copy the template file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your actual values:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Set appropriate permissions:**
   ```bash
   chmod 600 .env
   ```

### Required Secrets

#### GitHub Personal Access Token
**Purpose**: Enables OpenHands to create repositories, commit code, and push changes

**How to create:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Set expiration (recommended: 90 days)
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. Copy the token immediately (you won't see it again!)
7. Add to `.env`: `GITHUB_TOKEN=ghp_your_token_here`

**Security notes:**
- Never commit tokens to Git
- Rotate tokens every 90 days
- Use fine-grained tokens when possible
- Revoke immediately if compromised

#### Coolify API Token (Optional)
**Purpose**: Automate deployments via Coolify API

**How to create:**
1. Login to Coolify dashboard
2. Go to Settings → API Tokens
3. Create new token with appropriate permissions
4. Add to `.env`: `COOLIFY_API_TOKEN=your_token_here`

## Secrets Storage Locations

### On Server (Production)
```
/home/ubuntu/.env          # Main environment file
/opt/workspace/.env        # Workspace-specific secrets (if needed)
```

### In Coolify
Coolify manages secrets through its UI:
1. Navigate to your application
2. Go to "Environment Variables" tab
3. Add secrets there (they're encrypted at rest)

### In Docker Containers
Environment variables are passed to containers via:
- Coolify's environment variable management
- Docker Compose env_file directive
- Direct environment variable injection

## Security Best Practices

### ✅ DO
- Use `.env` files for local development
- Use Coolify's environment variables for production
- Rotate secrets regularly (every 90 days)
- Use different tokens for different environments
- Set restrictive file permissions (600)
- Use fine-grained tokens with minimal permissions
- Monitor token usage in GitHub settings

### ❌ DON'T
- Commit `.env` files to Git
- Share tokens via email or chat
- Use the same token across multiple projects
- Give tokens more permissions than needed
- Store tokens in plaintext in documentation
- Use tokens that never expire

## Verifying Secrets

### Check if secrets are loaded:
```bash
# On server
ssh ubuntu@161.118.171.201
echo $GITHUB_TOKEN  # Should show your token
```

### Test GitHub authentication:
```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### Check Coolify environment variables:
1. Login to Coolify dashboard
2. Navigate to your application
3. Check "Environment Variables" tab

## Rotating Secrets

### GitHub Token Rotation
1. Create new token in GitHub
2. Update `.env` file with new token
3. Restart OpenHands container:
   ```bash
   # Via Coolify UI: Click "Restart" button
   # Or via SSH:
   sudo docker restart openhands-*
   ```
4. Verify new token works
5. Revoke old token in GitHub

### Emergency: Token Compromised
1. **Immediately revoke** the token in GitHub
2. Generate new token
3. Update all locations where token is used
4. Review GitHub audit log for suspicious activity
5. Consider rotating other secrets as precaution

## Backup and Recovery

### Backup Secrets (Encrypted)
```bash
# Create encrypted backup
gpg -c .env
# This creates .env.gpg (encrypted file)
# Store this in a secure location (password manager, encrypted USB)
```

### Restore from Backup
```bash
# Decrypt backup
gpg .env.gpg
# This creates .env file
# Set permissions
chmod 600 .env
```

## Troubleshooting

### "GitHub authentication failed"
- Check if `GITHUB_TOKEN` is set correctly
- Verify token hasn't expired
- Ensure token has required scopes
- Test token with curl command above

### "Environment variable not found"
- Check if `.env` file exists
- Verify file permissions (should be 600)
- Ensure container has access to environment variables
- Restart container after updating `.env`

### "Permission denied"
- Check file ownership: `ls -la .env`
- Fix ownership: `sudo chown ubuntu:ubuntu .env`
- Fix permissions: `chmod 600 .env`

## Compliance and Auditing

### Regular Security Audit Checklist
- [ ] Review all active tokens in GitHub settings
- [ ] Verify token expiration dates
- [ ] Check for unused tokens (revoke them)
- [ ] Review GitHub audit log for suspicious activity
- [ ] Verify `.env` is in `.gitignore`
- [ ] Confirm no secrets in Git history
- [ ] Test secret rotation procedure
- [ ] Update documentation if procedures changed

### Audit Schedule
- **Weekly**: Check for expired tokens
- **Monthly**: Review active tokens and their usage
- **Quarterly**: Rotate all tokens
- **Annually**: Full security audit

---
**Requirements Validated**: 9.2, 9.3
**Last Updated**: 2025-11-29
