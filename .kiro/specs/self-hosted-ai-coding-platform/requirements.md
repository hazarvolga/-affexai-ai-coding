# Requirements Document

## Introduction

This document outlines the requirements for setting up a self-hosted AI coding platform on Oracle Cloud infrastructure. The system will provide a Vibe Coding-like experience using open-source tools, enabling autonomous code generation, GitHub integration, and deployment capabilities through Coolify, all without requiring any paid API services.

## Glossary

- **AI Coding Platform**: A web-based development environment that uses AI models to assist in code generation and modification
- **Ollama**: An open-source tool for running large language models locally
- **OpenHands**: An open-source autonomous AI coding agent with web interface
- **Coolify**: A self-hosted deployment platform for managing applications
- **DeepSeek Coder**: An open-source AI model specialized for code generation
- **Oracle Instance**: The Ubuntu server running on Oracle Cloud (instance-hulyaekiz, IP: 161.118.171.201)
- **GitHub Integration**: The ability to create, modify, and push code to GitHub repositories
- **Self-Hosted**: Running all services on the user's own infrastructure without external dependencies
- **MCP (Model Context Protocol)**: A standardized protocol that allows AI assistants to connect to external tools and data sources
- **MCP Server**: A service that implements the MCP protocol to provide specific capabilities (filesystem, GitHub, web search, etc.)

## Requirements

### Requirement 1

**User Story:** As a developer, I want to access an AI coding assistant through my web browser, so that I can develop applications without installing local software.

#### Acceptance Criteria

1. WHEN a user navigates to the platform URL THEN the system SHALL display a web-based interface accessible via standard web browsers
2. WHEN the web interface loads THEN the system SHALL provide authentication if configured
3. WHEN a user accesses the interface THEN the system SHALL maintain session state across page refreshes
4. WHEN multiple users access the system THEN the system SHALL handle concurrent sessions without performance degradation

### Requirement 2

**User Story:** As a developer, I want to use AI models running on my own server, so that I don't incur API costs and maintain data privacy.

#### Acceptance Criteria

1. WHEN the system starts THEN Ollama SHALL run as a service on the Oracle Instance
2. WHEN Ollama is running THEN the system SHALL load the DeepSeek Coder V2 16B model into memory
3. WHEN the AI model receives a coding request THEN the system SHALL generate responses using only local compute resources
4. WHEN the model is idle THEN the system SHALL maintain the model in memory for fast response times
5. WHEN system resources are constrained THEN the system SHALL manage memory allocation to prevent crashes

### Requirement 3

**User Story:** As a developer, I want to interact with the AI through a chat interface, so that I can describe what I want to build in natural language.

#### Acceptance Criteria

1. WHEN a user types a message in the chat interface THEN the system SHALL send the message to the AI model
2. WHEN the AI model processes a request THEN the system SHALL stream responses back to the user interface
3. WHEN the AI generates code THEN the system SHALL display it with syntax highlighting
4. WHEN a conversation has context THEN the system SHALL maintain conversation history for coherent multi-turn interactions

### Requirement 4

**User Story:** As a developer, I want the AI to create and modify files in a project structure, so that I can build complete applications.

#### Acceptance Criteria

1. WHEN the AI suggests file creation THEN the system SHALL create files in the appropriate directory structure
2. WHEN the AI modifies existing files THEN the system SHALL preserve file permissions and metadata
3. WHEN files are created or modified THEN the system SHALL track changes for version control
4. WHEN a project structure is created THEN the system SHALL organize files according to standard conventions

### Requirement 5

**User Story:** As a developer, I want to integrate with GitHub, so that I can version control my code and collaborate with others.

#### Acceptance Criteria

1. WHEN a user provides GitHub credentials THEN the system SHALL authenticate with GitHub API
2. WHEN the AI creates a project THEN the system SHALL initialize a Git repository
3. WHEN code changes are ready THEN the system SHALL commit changes with descriptive messages
4. WHEN a user requests THEN the system SHALL push commits to a GitHub repository
5. WHEN pushing to GitHub THEN the system SHALL handle authentication using personal access tokens

### Requirement 6

**User Story:** As a developer, I want to preview my applications, so that I can see changes in real-time.

#### Acceptance Criteria

1. WHEN a web application is created THEN the system SHALL provide a live preview URL
2. WHEN code changes are made THEN the system SHALL refresh the preview automatically
3. WHEN the preview server starts THEN the system SHALL expose it on an accessible port
4. WHEN multiple projects exist THEN the system SHALL manage separate preview instances

### Requirement 7

**User Story:** As a developer, I want to deploy applications to Coolify, so that I can make them publicly accessible.

#### Acceptance Criteria

1. WHEN a project is ready for deployment THEN the system SHALL integrate with Coolify API
2. WHEN deployment is triggered THEN the system SHALL create a new Coolify application
3. WHEN Coolify receives the application THEN the system SHALL configure environment variables and build settings
4. WHEN deployment completes THEN the system SHALL provide the public URL

### Requirement 8

**User Story:** As a system administrator, I want the platform to run reliably on Oracle Cloud, so that I can depend on it for daily development work.

#### Acceptance Criteria

1. WHEN the Oracle Instance starts THEN all services SHALL start automatically
2. WHEN a service crashes THEN the system SHALL restart it automatically
3. WHEN system resources are monitored THEN the system SHALL log resource usage
4. WHEN disk space is low THEN the system SHALL alert the administrator
5. WHEN network connectivity is lost THEN the system SHALL queue operations and retry when connection is restored

### Requirement 9

**User Story:** As a developer, I want the system to be secure, so that my code and credentials are protected.

#### Acceptance Criteria

1. WHEN services are exposed THEN the system SHALL use HTTPS for web interfaces
2. WHEN credentials are stored THEN the system SHALL encrypt sensitive data
3. WHEN API tokens are used THEN the system SHALL store them securely in environment variables
4. WHEN external access is configured THEN the system SHALL implement firewall rules
5. WHEN authentication is enabled THEN the system SHALL enforce strong password policies

### Requirement 10

**User Story:** As a developer, I want comprehensive documentation, so that I can troubleshoot issues and customize the system.

#### Acceptance Criteria

1. WHEN installation is complete THEN the system SHALL provide a README with usage instructions
2. WHEN configuration is needed THEN the system SHALL document all environment variables
3. WHEN troubleshooting THEN the system SHALL provide logs accessible via standard tools
4. WHEN customization is desired THEN the system SHALL document extension points

### Requirement 11

**User Story:** As a developer, I want to extend OpenHands capabilities with MCP servers, so that the AI can access external tools and services for enhanced functionality.

#### Acceptance Criteria

1. WHEN MCP servers are installed THEN the system SHALL provide filesystem access capabilities to OpenHands
2. WHEN MCP servers are configured THEN the system SHALL enable GitHub operations through MCP protocol
3. WHEN MCP servers are running THEN the system SHALL allow web search capabilities via Brave Search
4. WHEN OpenHands needs external tools THEN the system SHALL automatically utilize available MCP servers
5. WHEN MCP configuration changes THEN the system SHALL reload MCP servers without restarting OpenHands
6. WHEN MCP servers require authentication THEN the system SHALL securely store and manage API tokens
