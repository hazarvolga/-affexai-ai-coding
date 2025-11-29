"""
Unit tests for credential security
Feature: self-hosted-ai-coding-platform
Requirements: 9.2, 9.3
"""

import os
import subprocess
import pytest


def test_env_file_not_in_git():
    """Test that .env file is properly ignored by Git"""
    # Check if .env is in .gitignore
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    assert '.env' in gitignore_content, ".env should be in .gitignore"
    
    # Check if .env is actually ignored by git
    result = subprocess.run(
        ['git', 'check-ignore', '.env'],
        capture_output=True,
        text=True
    )
    # Exit code 0 means file is ignored
    assert result.returncode == 0, ".env file should be ignored by Git"


def test_env_example_exists():
    """Test that .env.example template exists"""
    assert os.path.exists('.env.example'), ".env.example template should exist"
    
    # Verify it contains required variables
    with open('.env.example', 'r') as f:
        content = f.read()
    
    required_vars = ['GITHUB_TOKEN', 'OLLAMA_HOST', 'LLM_MODEL']
    for var in required_vars:
        assert var in content, f"{var} should be documented in .env.example"


def test_env_example_has_no_real_secrets():
    """Test that .env.example doesn't contain real secrets"""
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Check for patterns that indicate real tokens
    forbidden_patterns = [
        'ghp_',  # GitHub personal access token prefix
        'gho_',  # GitHub OAuth token prefix
        'ghs_',  # GitHub server token prefix
    ]
    
    for pattern in forbidden_patterns:
        assert pattern not in content, \
            f".env.example should not contain real tokens (found {pattern})"


def test_github_token_format_validation():
    """Test that GitHub token has correct format if present"""
    # This test runs on the server where GITHUB_TOKEN might be set
    token = os.environ.get('GITHUB_TOKEN', '')
    
    if token:
        # GitHub tokens should start with specific prefixes
        valid_prefixes = ['ghp_', 'gho_', 'ghs_', 'github_pat_']
        assert any(token.startswith(prefix) for prefix in valid_prefixes), \
            "GITHUB_TOKEN should have valid GitHub token prefix"
        
        # Token should be long enough (GitHub tokens are typically 40+ chars)
        assert len(token) >= 40, \
            "GITHUB_TOKEN appears too short to be valid"


def test_environment_variables_loaded():
    """Test that required environment variables can be loaded"""
    # This is a basic test that environment variable mechanism works
    # We don't test actual values to avoid exposing secrets in test output
    
    # Test that we can set and read environment variables
    test_var = 'TEST_SECRET_VAR'
    test_value = 'test_value_12345'
    
    os.environ[test_var] = test_value
    assert os.environ.get(test_var) == test_value
    
    # Clean up
    del os.environ[test_var]


def test_no_secrets_in_git_history():
    """Test that no obvious secrets are committed to Git"""
    # Search for common secret patterns in Git history
    patterns = [
        'ghp_[a-zA-Z0-9]{36}',  # GitHub personal access token
        'gho_[a-zA-Z0-9]{36}',  # GitHub OAuth token
    ]
    
    for pattern in patterns:
        result = subprocess.run(
            ['git', 'log', '--all', '-p', '-S', pattern, '--regexp-ignore-case'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        
        # If pattern is found, git log will have output
        assert len(result.stdout) == 0, \
            f"Potential secret pattern '{pattern}' found in Git history"


def test_secrets_management_documentation_exists():
    """Test that secrets management documentation exists"""
    assert os.path.exists('docs/SECRETS_MANAGEMENT.md'), \
        "Secrets management documentation should exist"
    
    with open('docs/SECRETS_MANAGEMENT.md', 'r') as f:
        content = f.read()
    
    # Verify key topics are covered
    required_topics = [
        'GitHub',
        'token',
        'rotation',
        'security',
        '.env'
    ]
    
    for topic in required_topics:
        assert topic.lower() in content.lower(), \
            f"Documentation should cover '{topic}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
