# GitHub Integration Setup Guide

This guide walks you through setting up GitHub integration for the AI Coding Platform.

## Overview

GitHub integration allows OpenHands to:
- Create and initialize Git repositories
- Commit code changes with descriptive messages
- Push code to GitHub repositories
- Clone existing repositories for modification

## Step 1: Create a GitHub Personal Access Token

### 1.1 Navigate to GitHub Token Settings

1. Log in to your GitHub account
2. Click your profile picture in the top-right corner
3. Select **Settings** from the dropdown menu
4. Scroll down and click **Developer settings** in the left sidebar
5. Click **Personal access tokens** → **Tokens (classic)**
6. Click **Generate new token** → **Generate new token (classic)**

**Direct link**: https://github.com/settings/tokens/new

### 1.2 Configure Token Settings

**Token Name**: Enter a descriptive name
- Example: `AffexAI AI Coding Platform - OpenHands`

**Expiration**: Choose an expiration period
- Recommended: 90 days (for security)
- You can select "No expiration" but this is less secure

### 1.3 Select Required Permissions

Check the following scopes (permissions):

#### Required Scopes:

- ✅ **repo** (Full control of private repositories)
  - This includes:
    - `repo:status` - Access commit status
    - `repo_deployment` - Access deployment status
    - `public_repo` - Access public repositories
    - `repo:invite` - Access repository invitations
    - `security_events` - Read and write security events

- ✅ **workflow** (Update GitHub Action workflows)
  - Allows OpenHands to create and modify GitHub Actions workflows

#### Optional Scopes (for advanced features):

- `read:org` - Read organization membership (if working with organization repos)
- `gist` - Create gists (if you want OpenHands to create gists)

### 1.4 Generate and Copy Token

1. Scroll to the bottom and click **Generate token**
2. **IMPORTANT**: Copy the token immediately - you won't be able to see it again!
3. Store it securely (you'll need it in the next step)

**Token format**: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Configure Token in the Platform

### 2.1 Create .env File

In the root directory of the project, create a `.env` file:

```bash
# Copy the example file
cp .env.example .env
```

### 2.2 Add Your Token

Edit the `.env` file and replace `your_github_token_here` with your actual token:

```bash
# GitHub Integration
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Security Notes**:
- ⚠️ Never commit the `.env` file to Git (it's already in `.gitignore`)
- ⚠️ Never share your token publicly
- ⚠️ Treat it like a password

### 2.3 Restart Services

For the token to take effect, restart the OpenHands container:

```bash
docker-compose down
docker-compose up -d
```

Or if using Coolify:
1. Update the environment variable in Coolify dashboard
2. Redeploy the service

## Step 3: Verify Integration

### 3.1 Check Container Logs

Verify the token is loaded:

```bash
docker-compose logs openhands | grep -i github
```

You should not see any authentication errors.

### 3.2 Test in OpenHands UI

1. Access OpenHands at http://your-domain:3000
2. Ask the AI to create a new project
3. Request to initialize a Git repository
4. Ask to push to GitHub

Example prompt:
```
Create a simple Node.js hello world application, initialize a Git repository, 
and push it to a new GitHub repository called "test-openhands-integration"
```

## Troubleshooting

### Token Not Working

**Symptoms**: Authentication errors when pushing to GitHub

**Solutions**:
1. Verify token has correct permissions (repo, workflow)
2. Check token hasn't expired
3. Ensure token is correctly set in `.env` file (no extra spaces)
4. Restart OpenHands container after updating token

### Permission Denied Errors

**Symptoms**: "Permission denied" when pushing to repositories

**Solutions**:
1. Verify the `repo` scope is enabled
2. Check you have write access to the target repository
3. For organization repos, ensure token has `read:org` scope

### Token Expired

**Symptoms**: Authentication suddenly stops working

**Solutions**:
1. Generate a new token following Step 1
2. Update `.env` file with new token
3. Restart services

## Security Best Practices

### Token Rotation

Rotate your GitHub token regularly:
- **Recommended**: Every 90 days
- Set expiration when creating token
- Create calendar reminder to regenerate

### Token Scope Minimization

Only grant the minimum required permissions:
- For read-only operations: Use `public_repo` instead of full `repo`
- For specific repositories: Use fine-grained tokens (beta feature)

### Token Storage

- ✅ Store in `.env` file (not committed to Git)
- ✅ Use environment variables in production
- ✅ Use secrets management in Coolify
- ❌ Never hardcode in source code
- ❌ Never commit to version control
- ❌ Never share in chat/email

### Revoke Compromised Tokens

If your token is exposed:
1. Go to https://github.com/settings/tokens
2. Find the compromised token
3. Click **Delete** or **Revoke**
4. Generate a new token immediately
5. Update your `.env` file

## Advanced Configuration

### Using Fine-Grained Tokens (Beta)

GitHub now offers fine-grained personal access tokens with more granular permissions:

1. Go to https://github.com/settings/tokens?type=beta
2. Click **Generate new token**
3. Select specific repositories instead of all repositories
4. Choose granular permissions (Contents, Metadata, etc.)
5. Set expiration and generate

**Note**: OpenHands may require classic tokens for full compatibility.

### Organization Access

For organization repositories:

1. Generate token with `read:org` scope
2. Ensure your organization allows personal access tokens
3. Organization admins may need to approve token usage

### Multiple Tokens

For different projects or security levels:

1. Create separate tokens for different purposes
2. Use different `.env` files or environment configurations
3. Rotate tokens independently

## Reference

### Required Permissions Summary

| Scope | Purpose | Required |
|-------|---------|----------|
| `repo` | Full repository access | ✅ Yes |
| `workflow` | GitHub Actions workflows | ✅ Yes |
| `read:org` | Organization membership | ⚪ Optional |
| `gist` | Create gists | ⚪ Optional |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub personal access token | Yes (for GitHub features) |
| `LLM_MODEL` | AI model identifier | Yes |
| `LLM_BASE_URL` | Ollama API endpoint | Yes |
| `WORKSPACE_DIR` | OpenHands workspace path | Yes |

## Support

For issues with GitHub integration:

1. Check OpenHands logs: `docker-compose logs openhands`
2. Verify token permissions on GitHub
3. Test token with GitHub API:
   ```bash
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
   ```
4. Consult OpenHands documentation: https://github.com/All-Hands-AI/OpenHands

## Additional Resources

- [GitHub Personal Access Tokens Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub Token Scopes](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps)
- [OpenHands Documentation](https://github.com/All-Hands-AI/OpenHands)
