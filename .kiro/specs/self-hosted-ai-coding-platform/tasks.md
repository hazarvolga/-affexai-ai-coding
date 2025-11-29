# Implementation Plan

**IMPORTANT NOTE:** This project is deployed on Oracle Cloud via Coolify
- Server: instance-hulyaekiz (IP: 161.118.171.201)
- Coolify Dashboard: https://coolify.fpvlovers.com.tr
- OpenHands UI: https://ai.fpvlovers.com.tr
- All tasks must be executed on the Oracle Cloud server, NOT locally
- SSH access: `ssh ubuntu@161.118.171.201`

- [x] 1. Prepare Oracle Cloud instance and verify prerequisites
  - SSH into the instance and verify Docker is installed
  - Check available disk space (minimum 30GB required)
  - Verify Docker Compose is installed
  - Confirm ai-coding-network exists
  - _Requirements: 8.1, 8.3_

- [x] 2. Deploy Ollama service
  - [x] 2.1 Create Docker Compose configuration for Ollama
    - Write docker-compose.yml with Ollama service definition
    - Configure volume mounts for model storage
    - Set up network connectivity to ai-coding-network
    - Configure restart policy
    - _Requirements: 2.1, 2.4_

  - [x] 2.2 Deploy Ollama container
    - Start Ollama service using Docker Compose
    - Verify container is running
    - Check Ollama API is accessible on port 11434
    - _Requirements: 2.1_

  - [x] 2.3 Download DeepSeek Coder V2 16B model
    - Execute ollama pull command for deepseek-coder-v2:16b
    - Monitor download progress
    - Verify model is loaded successfully
    - _Requirements: 2.2_

  - [x] 2.4 Write unit test for Ollama service health
    - Create test script to verify Ollama API responds
    - Test model listing endpoint
    - Test simple inference request
    - _Requirements: 2.1, 2.2_

- [x] 3. Deploy OpenHands service
  - [x] 3.1 Update Docker Compose with OpenHands configuration
    - Add OpenHands service to docker-compose.yml
    - Configure environment variables (LLM_MODEL, LLM_BASE_URL)
    - Set up workspace volume mount
    - Configure Docker socket mount for container management
    - _Requirements: 1.1, 3.1_

  - [x] 3.2 Configure OpenHands to connect to Ollama
    - Set LLM_BASE_URL to http://ollama:11434
    - Set LLM_MODEL to ollama/deepseek-coder-v2:16b
    - Configure workspace directory
    - _Requirements: 2.3, 3.1_

  - [x] 3.3 Deploy OpenHands container
    - Start OpenHands service
    - Verify container is running
    - Check OpenHands UI is accessible on port 3000
    - _Requirements: 1.1_

  - [x] 3.4 Write unit test for OpenHands UI accessibility
    - Create test to verify HTTP 200 response from UI
    - Test chat interface loads correctly
    - Verify connection to Ollama backend
    - _Requirements: 1.1, 3.1_

- [x] 4. Configure GitHub integration
  - [x] 4.1 Create GitHub personal access token
    - Document steps for user to create token
    - Specify required permissions (repo, workflow)
    - Create .env file template for token storage
    - _Requirements: 5.1_

  - [x] 4.2 Configure GitHub token in OpenHands
    - Add GITHUB_TOKEN environment variable to docker-compose.yml
    - Update OpenHands service configuration
    - Restart OpenHands container
    - _Requirements: 5.1_

  - [x] 4.3 Write property test for Git repository initialization
    - **Property 3: Git Repository Initialization**
    - **Validates: Requirements 5.2**
    - Test that new projects create valid .git directory
    - Verify required Git files exist (HEAD, config, objects, refs)

  - [x] 4.4 Write property test for commit message validation
    - **Property 4: Commit Message Non-Empty**
    - **Validates: Requirements 5.3**
    - Test that commits have non-empty descriptive messages
    - Verify messages contain at least 2 words

- [x] 5. Configure Traefik reverse proxy and domain
  - [x] 5.1 Set up DNS record for OpenHands subdomain
    - Document DNS configuration steps
    - Create A record pointing ai.fpvlovers.com.tr to 161.118.171.201
    - Wait for DNS propagation
    - _Requirements: 1.1, 9.1_

  - [x] 5.2 Configure Coolify to route subdomain to OpenHands
    - Access Coolify dashboard at coolify.fpvlovers.com.tr
    - Add new service for OpenHands in affexai-ai-coding project
    - Configure domain: ai.fpvlovers.com.tr
    - Set target port to 3000
    - Enable HTTPS with Let's Encrypt
    - _Requirements: 1.1, 9.1_

  - [x] 5.3 Generate SSL certificate
    - Trigger Let's Encrypt certificate generation in Coolify
    - Verify certificate is issued successfully
    - Test HTTPS access to ai.fpvlovers.com.tr
    - _Requirements: 9.1, 9.2_

  - [x] 5.4 Write property test for HTTPS enforcement
    - **Property 6: HTTPS Enforcement**
    - **Validates: Requirements 9.1**
    - Test that HTTP requests redirect to HTTPS
    - Verify redirect status codes (301, 302, 307, 308)
    - Confirm Location header starts with https://

- [x] 6. Implement file system operations
  - [x] 6.1 Configure workspace directory structure
    - Create /opt/workspace/projects directory
    - Create /opt/workspace/temp directory
    - Set appropriate permissions
    - _Requirements: 4.1_

  - [x] 6.2 Write property test for file creation
    - **Property 1: File Creation Preserves Structure**
    - **Validates: Requirements 4.1**
    - Test that files are created at correct paths
    - Verify directory hierarchy is created properly

  - [x] 6.3 Write property test for file permission preservation
    - **Property 2: File Modification Preserves Permissions**
    - **Validates: Requirements 4.2**
    - Test that file modifications preserve original permissions
    - Verify ownership remains unchanged

- [x] 7. Configure service auto-restart and monitoring
  - [x] 7.1 Set restart policies for all services
    - Update docker-compose.yml with restart: unless-stopped
    - Apply to Ollama and OpenHands services
    - Redeploy services with new configuration
    - _Requirements: 8.1, 8.2_

  - [x] 7.2 Implement health check scripts
    - Create health check script for Ollama
    - Create health check script for OpenHands
    - Create combined system health check
    - _Requirements: 8.3_

  - [x] 7.3 Write property test for service auto-restart
    - **Property 5: Service Auto-Restart**
    - **Validates: Requirements 8.2**
    - Test that stopped services restart automatically
    - Verify restart happens within reasonable time window

- [ ] 8. Create deployment integration with Coolify
  - [ ] 8.1 Document Coolify deployment workflow
    - Write guide for deploying OpenHands-created apps
    - Document GitHub repository connection
    - Explain automatic deployment triggers
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 8.2 Create sample application deployment
    - Use OpenHands to create a simple web application
    - Push application to GitHub repository
    - Configure Coolify to deploy from GitHub
    - Verify application is accessible
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 8.3 Write integration test for deployment pipeline
    - Test end-to-end workflow from code generation to deployment
    - Verify GitHub push succeeds
    - Verify Coolify deployment completes
    - Verify deployed application is accessible

- [x] 9. Implement security configurations
  - [x] 9.1 Configure firewall rules
    - Verify ports 80, 443, 8000 are open
    - Verify port 11434 is internal only
    - Verify port 3000 is internal only
    - Document firewall configuration
    - _Requirements: 9.1, 9.4_

  - [x] 9.2 Implement secrets management
    - Create .env.example template file
    - Document all required environment variables
    - Add .env to .gitignore
    - Implement secure token storage
    - _Requirements: 9.2, 9.3_

  - [x] 9.3 Write unit test for credential encryption
    - Test that stored credentials are not in plaintext
    - Verify environment variables are properly loaded
    - Test GitHub token authentication

- [x] 10. Create documentation and usage guide
  - [x] 10.1 Write comprehensive README
    - Document system architecture
    - Provide installation instructions
    - Include usage examples
    - Add troubleshooting section
    - _Requirements: 10.1, 10.2_

  - [x] 10.2 Create configuration reference
    - Document all environment variables
    - Explain Docker Compose configuration
    - Provide network architecture diagram
    - _Requirements: 10.2_

  - [x] 10.3 Write troubleshooting guide
    - Document common issues and solutions
    - Explain how to access logs
    - Provide debugging commands
    - Include performance optimization tips
    - _Requirements: 10.3_

  - [x] 10.4 Create maintenance procedures
    - Document backup procedures
    - Explain update process
    - Provide rollback instructions
    - Include monitoring guidelines
    - _Requirements: 10.4_

- [-] 11. Install and configure MCP servers
  - [x] 11.1 Install Node.js on Oracle Instance
    - SSH to server and check if Node.js is installed
    - Install Node.js 20.x LTS if not present
    - Verify npm is available
    - Test npx command works
    - _Requirements: 11.1, 11.2, 11.3_

  - [x] 11.2 Install MCP server packages globally
    - Install @modelcontextprotocol/server-filesystem
    - Install @modelcontextprotocol/server-github
    - Install @modelcontextprotocol/server-brave-search
    - Install @modelcontextprotocol/server-docker
    - Verify all packages are installed correctly
    - _Requirements: 11.1, 11.2, 11.3_

  - [ ] 11.3 Configure filesystem MCP server in OpenHands
    - Access OpenHands UI at https://ai.fpvlovers.com.tr
    - Navigate to Settings → MCP Settings
    - Add filesystem MCP server configuration
    - Set workspace path to /opt/workspace
    - Test filesystem operations work
    - _Requirements: 11.1, 11.4_

  - [ ] 11.4 Configure GitHub MCP server in OpenHands
    - Add GitHub MCP server configuration in UI
    - Configure GITHUB_PERSONAL_ACCESS_TOKEN environment variable
    - Test GitHub operations (list repos, create repo)
    - Verify authentication works
    - _Requirements: 11.2, 11.4, 11.6_

  - [ ] 11.5 Configure Brave Search MCP server in OpenHands
    - Obtain Brave Search API key
    - Add Brave Search MCP server configuration in UI
    - Configure BRAVE_API_KEY environment variable
    - Test web search functionality
    - _Requirements: 11.3, 11.4, 11.6_

  - [ ] 11.6 Configure Docker MCP server in OpenHands
    - Add Docker MCP server configuration in UI
    - Verify Docker socket access from OpenHands container
    - Test container listing and inspection
    - _Requirements: 11.4_

  - [ ] 11.7 Document MCP configuration and usage
    - Update MCP_SETUP_GUIDE.md with actual configurations
    - Document how to add/remove MCP servers
    - Provide usage examples for each MCP server
    - Add troubleshooting section for common MCP issues
    - _Requirements: 11.5, 10.1_

  - [ ] 11.8 Test MCP integration end-to-end
    - Test filesystem operations via chat
    - Test GitHub operations via chat
    - Test web search via chat
    - Test Docker operations via chat
    - Verify MCP servers reload without restart
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 12. Final checkpoint - Verify complete system
  - Ensure all tests pass, ask the user if questions arise
  - Verify all services are running
  - Test complete workflow from UI access to deployment
  - Confirm HTTPS access works
  - Validate GitHub integration
  - Check system resource usage
  - Review logs for any errors
  - _Requirements: All_
