"""
Property-based tests for file system operations in the AI Coding Platform.

These tests verify that file creation and modification operations maintain
correctness properties across various inputs.

NOTE: This project runs on Oracle Cloud via Coolify (instance-hulyaekiz)
Tests can be run locally but validate behavior for the remote deployment.
"""

import os
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Generator

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


def create_file_at_path(file_path: Path, content: str) -> None:
    """
    Create a file at the specified path with given content.
    Creates parent directories if they don't exist.
    
    Args:
        file_path: Path where file should be created
        content: Content to write to the file
    """
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content to file
    file_path.write_text(content, encoding='utf-8')


def modify_file_content(file_path: Path, new_content: str) -> None:
    """
    Modify the content of an existing file.
    
    Args:
        file_path: Path to the file to modify
        new_content: New content to write
    """
    file_path.write_text(new_content, encoding='utf-8')


# ============================================================================
# Hypothesis Strategies
# ============================================================================

# Valid file path components (safe characters for file/directory names)
safe_path_component = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_."
    ),
    min_size=1,
    max_size=30
).filter(
    lambda x: x and 
    not x.startswith('.') and 
    not x.endswith('.') and
    x not in ['.', '..'] and
    '/' not in x and
    '\\' not in x
)

# Generate valid relative file paths (1-3 levels deep)
@st.composite
def valid_relative_paths(draw):
    """Generate valid relative file paths for testing."""
    depth = draw(st.integers(min_value=1, max_value=3))
    components = [draw(safe_path_component) for _ in range(depth)]
    
    # Last component is the filename, ensure it has an extension
    filename = components[-1]
    if '.' not in filename:
        extension = draw(st.sampled_from(['txt', 'py', 'js', 'md', 'json']))
        filename = f"{filename}.{extension}"
        components[-1] = filename
    
    return Path(*components)


# File content strategy
file_content = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd", "Zs", "Po"),
    ),
    min_size=0,
    max_size=1000
)


# ============================================================================
# Property-Based Tests
# ============================================================================

# Feature: self-hosted-ai-coding-platform, Property 1: File Creation Preserves Structure
@settings(max_examples=100, deadline=None)
@given(
    relative_path=valid_relative_paths(),
    content=file_content
)
def test_file_creation_preserves_structure(
    relative_path: Path,
    content: str
) -> None:
    """
    Property 1: File Creation Preserves Structure
    
    For any valid file path within the workspace, when the system creates a file
    at that path, the file should exist at exactly that location with the correct
    directory hierarchy created.
    
    Validates: Requirements 4.1
    
    Args:
        relative_path: Relative path where file should be created
        content: Content to write to the file
    """
    # Create temporary workspace
    temp_workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    
    try:
        # Construct full file path
        file_path = temp_workspace / relative_path
        
        # Property: Before creation, file should not exist
        assert not file_path.exists(), \
            f"File already exists before creation: {file_path}"
        
        # Create file at the specified path
        create_file_at_path(file_path, content)
        
        # Property: File should exist at exact location
        assert file_path.exists(), \
            f"File was not created at expected path: {file_path}"
        
        # Property: File should be a file, not a directory
        assert file_path.is_file(), \
            f"Path exists but is not a file: {file_path}"
        
        # Property: File should contain the expected content
        actual_content = file_path.read_text(encoding='utf-8')
        assert actual_content == content, \
            f"File content mismatch. Expected: '{content}', Got: '{actual_content}'"
        
        # Property: All parent directories should exist
        current = file_path.parent
        while current != temp_workspace:
            assert current.exists(), \
                f"Parent directory does not exist: {current}"
            assert current.is_dir(), \
                f"Parent path exists but is not a directory: {current}"
            current = current.parent
        
        # Property: Directory hierarchy should match the relative path
        expected_parts = list(relative_path.parts)
        actual_relative = file_path.relative_to(temp_workspace)
        actual_parts = list(actual_relative.parts)
        
        assert expected_parts == actual_parts, \
            f"Directory hierarchy mismatch. Expected: {expected_parts}, Got: {actual_parts}"
        
    finally:
        # Cleanup
        if temp_workspace.exists():
            shutil.rmtree(temp_workspace, ignore_errors=True)


# Feature: self-hosted-ai-coding-platform, Property 1: File Creation Preserves Structure (Edge Case)
def test_file_creation_in_nested_directories(temp_workspace: Path) -> None:
    """
    Edge case: Creating files in deeply nested directory structures.
    
    Validates: Requirements 4.1
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    # Create a deeply nested path
    deep_path = temp_workspace / "level1" / "level2" / "level3" / "level4" / "test.txt"
    
    # Create file
    create_file_at_path(deep_path, "deep content")
    
    # Property: File should exist
    assert deep_path.exists()
    assert deep_path.is_file()
    
    # Property: All intermediate directories should exist
    assert (temp_workspace / "level1").is_dir()
    assert (temp_workspace / "level1" / "level2").is_dir()
    assert (temp_workspace / "level1" / "level2" / "level3").is_dir()
    assert (temp_workspace / "level1" / "level2" / "level3" / "level4").is_dir()


# Feature: self-hosted-ai-coding-platform, Property 1: File Creation Preserves Structure (Edge Case)
def test_file_creation_with_existing_parent_dirs(temp_workspace: Path) -> None:
    """
    Edge case: Creating files when parent directories already exist.
    
    Validates: Requirements 4.1
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    # Create parent directories first
    parent_dir = temp_workspace / "existing" / "parent"
    parent_dir.mkdir(parents=True)
    
    # Create file in existing directory structure
    file_path = parent_dir / "newfile.txt"
    create_file_at_path(file_path, "content in existing dir")
    
    # Property: File should exist
    assert file_path.exists()
    assert file_path.is_file()
    
    # Property: Parent directories should still exist
    assert parent_dir.exists()
    assert parent_dir.is_dir()


# ============================================================================
# File Permission Property Tests
# ============================================================================

# Feature: self-hosted-ai-coding-platform, Property 2: File Modification Preserves Permissions
@settings(max_examples=100, deadline=None)
@given(
    relative_path=valid_relative_paths(),
    initial_content=file_content,
    new_content=file_content
)
def test_file_modification_preserves_permissions(
    relative_path: Path,
    initial_content: str,
    new_content: str
) -> None:
    """
    Property 2: File Modification Preserves Permissions
    
    For any existing file in the workspace, when the system modifies the file
    content, the file permissions and ownership should remain unchanged unless
    explicitly modified.
    
    Validates: Requirements 4.2
    
    Args:
        relative_path: Relative path for the test file
        initial_content: Initial content to write
        new_content: New content to write (modification)
    """
    # Create temporary workspace
    temp_workspace = Path(tempfile.mkdtemp(prefix="test_workspace_"))
    
    try:
        # Create file with initial content
        file_path = temp_workspace / relative_path
        create_file_at_path(file_path, initial_content)
        
        # Get original file permissions and metadata
        original_stat = file_path.stat()
        original_mode = original_stat.st_mode
        original_uid = original_stat.st_uid
        original_gid = original_stat.st_gid
        
        # Modify file content
        modify_file_content(file_path, new_content)
        
        # Get new file permissions and metadata
        new_stat = file_path.stat()
        new_mode = new_stat.st_mode
        new_uid = new_stat.st_uid
        new_gid = new_stat.st_gid
        
        # Property: File permissions should be unchanged
        assert new_mode == original_mode, \
            f"File permissions changed after modification. " \
            f"Original: {oct(original_mode)}, New: {oct(new_mode)}"
        
        # Property: File ownership should be unchanged
        assert new_uid == original_uid, \
            f"File UID changed after modification. Original: {original_uid}, New: {new_uid}"
        
        assert new_gid == original_gid, \
            f"File GID changed after modification. Original: {original_gid}, New: {new_gid}"
        
        # Property: File content should be updated
        actual_content = file_path.read_text(encoding='utf-8')
        assert actual_content == new_content, \
            f"File content was not updated correctly"
        
        # Property: File should still exist at same location
        assert file_path.exists(), \
            f"File no longer exists after modification"
        
    finally:
        # Cleanup
        if temp_workspace.exists():
            shutil.rmtree(temp_workspace, ignore_errors=True)


# Feature: self-hosted-ai-coding-platform, Property 2: File Modification Preserves Permissions (Edge Case)
def test_file_modification_with_custom_permissions(temp_workspace: Path) -> None:
    """
    Edge case: Modifying files with custom permissions should preserve them.
    
    Validates: Requirements 4.2
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    # Create file
    file_path = temp_workspace / "custom_perms.txt"
    create_file_at_path(file_path, "initial content")
    
    # Set custom permissions (read-only for owner, no access for others)
    custom_mode = stat.S_IRUSR | stat.S_IRGRP
    os.chmod(file_path, custom_mode)
    
    # Get original permissions
    original_mode = file_path.stat().st_mode
    
    # Modify file (need to temporarily make it writable)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
    modify_file_content(file_path, "modified content")
    
    # Restore original permissions
    os.chmod(file_path, custom_mode)
    
    # Property: Permissions should match what we set
    final_mode = file_path.stat().st_mode
    assert stat.S_IMODE(final_mode) == stat.S_IMODE(custom_mode), \
        f"Custom permissions not preserved"


# Feature: self-hosted-ai-coding-platform, Property 2: File Modification Preserves Permissions (Edge Case)
def test_multiple_modifications_preserve_permissions(temp_workspace: Path) -> None:
    """
    Edge case: Multiple modifications should consistently preserve permissions.
    
    Validates: Requirements 4.2
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    # Create file
    file_path = temp_workspace / "multi_mod.txt"
    create_file_at_path(file_path, "version 1")
    
    # Get original permissions
    original_mode = file_path.stat().st_mode
    
    # Perform multiple modifications
    for i in range(2, 6):
        modify_file_content(file_path, f"version {i}")
        
        # Property: Permissions should remain unchanged after each modification
        current_mode = file_path.stat().st_mode
        assert current_mode == original_mode, \
            f"Permissions changed after modification {i}. " \
            f"Original: {oct(original_mode)}, Current: {oct(current_mode)}"


# Feature: self-hosted-ai-coding-platform, Property 2: File Modification Preserves Permissions (Edge Case)
def test_empty_file_modification_preserves_permissions(temp_workspace: Path) -> None:
    """
    Edge case: Modifying empty files should preserve permissions.
    
    Validates: Requirements 4.2
    
    Args:
        temp_workspace: Temporary workspace directory
    """
    # Create empty file
    file_path = temp_workspace / "empty.txt"
    create_file_at_path(file_path, "")
    
    # Get original permissions
    original_mode = file_path.stat().st_mode
    
    # Modify with content
    modify_file_content(file_path, "now has content")
    
    # Property: Permissions should be unchanged
    new_mode = file_path.stat().st_mode
    assert new_mode == original_mode, \
        f"Permissions changed when adding content to empty file"
    
    # Modify back to empty
    modify_file_content(file_path, "")
    
    # Property: Permissions should still be unchanged
    final_mode = file_path.stat().st_mode
    assert final_mode == original_mode, \
        f"Permissions changed when emptying file"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
