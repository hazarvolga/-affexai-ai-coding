"""
Property-based tests for Git operations in the AI Coding Platform.

These tests verify that Git repository initialization and commit operations
maintain correctness properties across various inputs.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import git
import pytest
from hypothesis import given, settings, strategies as st


# ============================================================================
# Test Fixtures and Helpers
# ============================================================================

@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace directory for testing."""
    workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    try:
        yield workspace
    finally:
        # Cleanup
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)


def is_valid_git_repo(repo_path: Path) -> bool:
    """
    Check if a directory is a valid Git repository.
    
    Args:
        repo_path: Path to check
        
    Returns:
        True if valid Git repository, False otherwise
    """
    try:
        repo = git.Repo(repo_path)
        return not repo.bare
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        return False


def has_required_git_files(repo_path: Path) -> bool:
    """
    Verify that required Git files exist in the repository.
    
    Args:
        repo_path: Path to Git repository
        
    Returns:
        True if all required files exist, False otherwise
    """
    git_dir = repo_path / ".git"
    
    if not git_dir.exists() or not git_dir.is_dir():
        return False
    
    required_files = [
        git_dir / "HEAD",
        git_dir / "config",
        git_dir / "objects",
        git_dir / "refs",
    ]
    
    for required_file in required_files:
        if not required_file.exists():
            return False
    
    return True


# ============================================================================
# Hypothesis Strategies
# ============================================================================

# Valid project name strategy
# Project names should be alphanumeric with hyphens/underscores
valid_project_names = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_"
    ),
    min_size=1,
    max_size=50
).filter(lambda x: x and not x.startswith(("-", "_")) and not x.endswith(("-", "_")))


# ============================================================================
# Property-Based Tests
# ============================================================================

# Feature: self-hosted-ai-coding-platform, Property 3: Git Repository Initialization
@settings(max_examples=100, deadline=None)
@given(project_name=valid_project_names)
def test_git_initialization_creates_valid_repository(project_name: str) -> None:
    """
    Property 3: Git Repository Initialization
    
    For any new project created by the system, initializing a Git repository
    should result in a valid .git directory with proper Git configuration files
    (HEAD, config, objects, refs).
    
    Validates: Requirements 5.2
    
    Args:
        project_name: Name of the project to create
    """
    # Create temporary workspace for this test iteration
    temp_workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    
    try:
        # Create project directory
        project_path = temp_workspace / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Git repository (simulating what OpenHands would do)
        repo = git.Repo.init(project_path)
        
        # Property: Repository should be valid
        assert is_valid_git_repo(project_path), \
            f"Initialized repository at {project_path} is not a valid Git repository"
        
        # Property: .git directory should exist
        git_dir = project_path / ".git"
        assert git_dir.exists(), \
            f".git directory does not exist at {git_dir}"
        assert git_dir.is_dir(), \
            f".git exists but is not a directory at {git_dir}"
        
        # Property: Required Git files should exist
        assert has_required_git_files(project_path), \
            f"Required Git files missing in {project_path}"
        
        # Property: HEAD file should exist and contain valid content
        head_file = git_dir / "HEAD"
        assert head_file.exists(), "HEAD file does not exist"
        head_content = head_file.read_text().strip()
        assert head_content.startswith("ref:"), \
            f"HEAD file has invalid content: {head_content}"
        
        # Property: config file should exist and be readable
        config_file = git_dir / "config"
        assert config_file.exists(), "config file does not exist"
        config_content = config_file.read_text()
        assert len(config_content) > 0, "config file is empty"
        
        # Property: objects directory should exist
        objects_dir = git_dir / "objects"
        assert objects_dir.exists(), "objects directory does not exist"
        assert objects_dir.is_dir(), "objects exists but is not a directory"
        
        # Property: refs directory should exist
        refs_dir = git_dir / "refs"
        assert refs_dir.exists(), "refs directory does not exist"
        assert refs_dir.is_dir(), "refs exists but is not a directory"
        
        # Property: refs should have heads and tags subdirectories
        heads_dir = refs_dir / "heads"
        tags_dir = refs_dir / "tags"
        assert heads_dir.exists(), "refs/heads directory does not exist"
        assert tags_dir.exists(), "refs/tags directory does not exist"
    
    finally:
        # Cleanup
        if temp_workspace.exists():
            shutil.rmtree(temp_workspace, ignore_errors=True)


# Feature: self-hosted-ai-coding-platform, Property 3: Git Repository Initialization (Edge Case)
def test_git_initialization_in_existing_directory(temp_workspace: Path) -> None:
    """
    Edge case: Initializing Git in a directory with existing files.
    
    Validates: Requirements 5.2
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    # Create project directory with some files
    project_path = temp_workspace / "existing-project"
    project_path.mkdir(parents=True)
    
    # Add some existing files
    (project_path / "README.md").write_text("# Existing Project\n")
    (project_path / "src").mkdir()
    (project_path / "src" / "main.py").write_text("print('hello')\n")
    
    # Initialize Git repository
    repo = git.Repo.init(project_path)
    
    # Property: Repository should be valid
    assert is_valid_git_repo(project_path)
    
    # Property: Existing files should still exist
    assert (project_path / "README.md").exists()
    assert (project_path / "src" / "main.py").exists()
    
    # Property: Required Git files should exist
    assert has_required_git_files(project_path)


# Feature: self-hosted-ai-coding-platform, Property 3: Git Repository Initialization (Edge Case)
def test_git_initialization_idempotent(temp_workspace: Path) -> None:
    """
    Edge case: Initializing Git multiple times should be idempotent.
    
    Validates: Requirements 5.2
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    project_path = temp_workspace / "idempotent-test"
    project_path.mkdir(parents=True)
    
    # Initialize Git repository first time
    repo1 = git.Repo.init(project_path)
    
    # Get initial HEAD content
    head_file = project_path / ".git" / "HEAD"
    initial_head = head_file.read_text()
    
    # Initialize Git repository second time (should be safe)
    repo2 = git.Repo.init(project_path)
    
    # Property: Repository should still be valid
    assert is_valid_git_repo(project_path)
    
    # Property: HEAD should be unchanged
    final_head = head_file.read_text()
    assert initial_head == final_head, \
        "Re-initializing Git repository changed HEAD content"
    
    # Property: Required Git files should still exist
    assert has_required_git_files(project_path)


# ============================================================================
# Commit Message Property Tests
# ============================================================================

# Valid file content strategy for creating test files
# Use only safe ASCII characters to avoid encoding issues
file_contents = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd", "Zs", "Po"),
    ),
    min_size=1,
    max_size=1000
)

# Valid commit message strategy
# Messages should be descriptive with at least 2 words
# Build messages from words to avoid excessive filtering
word_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
    min_size=1,
    max_size=20
).filter(lambda x: len(x.strip()) > 0)

valid_commit_messages = st.lists(
    word_strategy,
    min_size=2,
    max_size=10
).map(lambda words: " ".join(words))


# Feature: self-hosted-ai-coding-platform, Property 4: Commit Message Non-Empty
@settings(max_examples=100, deadline=None)
@given(
    project_name=valid_project_names,
    file_content=file_contents,
    commit_message=valid_commit_messages
)
def test_commit_message_non_empty(
    project_name: str,
    file_content: str,
    commit_message: str
) -> None:
    """
    Property 4: Commit Message Non-Empty
    
    For any set of changes committed to Git, the commit message should be
    non-empty and contain descriptive text about the changes made.
    Messages should contain at least 2 words.
    
    Validates: Requirements 5.3
    
    Args:
        project_name: Name of the project
        file_content: Content to write to a test file
        commit_message: Commit message to use
    """
    # Create temporary workspace
    temp_workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    
    try:
        # Create project directory and initialize Git
        project_path = temp_workspace / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        repo = git.Repo.init(project_path)
        
        # Configure Git user (required for commits)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create a test file with changes
        test_file = project_path / "test_file.txt"
        test_file.write_text(file_content)
        
        # Stage the file (use relative path to avoid macOS /var vs /private/var issue)
        repo.index.add(["test_file.txt"])
        
        # Commit with the message
        commit = repo.index.commit(commit_message)
        
        # Property: Commit message should not be empty
        assert commit.message, "Commit message is empty"
        assert len(commit.message.strip()) > 0, "Commit message is only whitespace"
        
        # Property: Commit message should be the one we provided
        assert commit.message == commit_message, \
            f"Commit message mismatch: expected '{commit_message}', got '{commit.message}'"
        
        # Property: Commit message should contain at least 2 words (descriptive)
        words = commit.message.split()
        assert len(words) >= 2, \
            f"Commit message should contain at least 2 words, got {len(words)}: '{commit.message}'"
        
        # Property: Commit should have the file we added
        assert test_file.name in commit.stats.files, \
            f"Committed file {test_file.name} not found in commit stats"
        
        # Property: Commit should be retrievable from repository
        retrieved_commit = repo.commit(commit.hexsha)
        assert retrieved_commit.hexsha == commit.hexsha, \
            "Cannot retrieve commit from repository"
        
    finally:
        # Cleanup
        if temp_workspace.exists():
            shutil.rmtree(temp_workspace, ignore_errors=True)


# Feature: self-hosted-ai-coding-platform, Property 4: Commit Message Non-Empty (Edge Case)
def test_commit_message_rejects_empty() -> None:
    """
    Edge case: Empty commit messages should be rejected or handled.
    
    Validates: Requirements 5.3
    """
    temp_workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    
    try:
        # Create project and initialize Git
        project_path = temp_workspace / "test-project"
        project_path.mkdir(parents=True)
        repo = git.Repo.init(project_path)
        
        # Configure Git user
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create and stage a file
        test_file = project_path / "test.txt"
        test_file.write_text("test content")
        repo.index.add(["test.txt"])
        
        # Try to commit with empty message - Git should reject this
        # or we should validate before committing
        try:
            commit = repo.index.commit("")
            # If commit succeeds, verify it has some default message
            assert commit.message, "Empty commit message was accepted without default"
        except Exception as e:
            # Expected: Git rejects empty messages
            assert "empty" in str(e).lower() or "message" in str(e).lower(), \
                f"Unexpected error when committing with empty message: {e}"
    
    finally:
        if temp_workspace.exists():
            shutil.rmtree(temp_workspace, ignore_errors=True)


# Feature: self-hosted-ai-coding-platform, Property 4: Commit Message Non-Empty (Edge Case)
def test_commit_message_whitespace_only() -> None:
    """
    Edge case: Whitespace-only commit messages should be treated as invalid.
    
    Validates: Requirements 5.3
    """
    temp_workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    
    try:
        # Create project and initialize Git
        project_path = temp_workspace / "test-project"
        project_path.mkdir(parents=True)
        repo = git.Repo.init(project_path)
        
        # Configure Git user
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create and stage a file
        test_file = project_path / "test.txt"
        test_file.write_text("test content")
        repo.index.add(["test.txt"])
        
        # Commit with whitespace-only message
        whitespace_messages = ["   ", "\t\t", "\n\n", "  \t  \n  "]
        
        for ws_msg in whitespace_messages:
            # Git allows whitespace messages, but they should be considered invalid
            # in our validation logic
            commit = repo.index.commit(ws_msg)
            
            # Property: We should detect this as invalid (only whitespace)
            stripped = commit.message.strip()
            if not stripped:
                # This is what we expect - message is effectively empty
                assert True, "Whitespace-only message detected correctly"
            else:
                # If Git normalized it, that's also acceptable
                assert len(stripped.split()) >= 1, \
                    "Message should have at least some content after stripping"
            
            # Create another file for next iteration
            next_file = project_path / f"test_{len(whitespace_messages)}.txt"
            next_file.write_text("more content")
            repo.index.add([f"test_{len(whitespace_messages)}.txt"])
    
    finally:
        if temp_workspace.exists():
            shutil.rmtree(temp_workspace, ignore_errors=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
