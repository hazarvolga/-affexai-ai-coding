# Tests for AI Coding Platform

This directory contains tests for the self-hosted AI coding platform.

## Test Types

### 1. Unit Tests (Bash Scripts)
Simple health check scripts for services:
- `test_ollama_health.sh` - Verifies Ollama service is running and responding
- `test_openhands_ui.sh` - Verifies OpenHands UI is accessible

### 2. Property-Based Tests (Python)
Comprehensive tests using Hypothesis for property-based testing:
- `test_git_properties.py` - Git repository initialization and commit properties
- `test_file_properties.py` - File system operation properties (future)
- `test_service_properties.py` - Service restart and availability properties (future)

## Setup

### Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install -r requirements.txt
```

## Running Tests

### Run All Property-Based Tests

```bash
# From the tests directory
pytest -v

# Or from project root
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_git_properties.py -v
```

### Run Specific Test

```bash
pytest tests/test_git_properties.py::test_git_initialization_creates_valid_repository -v
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Run Health Check Scripts

```bash
# Test Ollama
bash tests/test_ollama_health.sh

# Test OpenHands UI
bash tests/test_openhands_ui.sh
```

## Property-Based Testing

Property-based tests verify that certain properties hold true across many randomly generated inputs. We use [Hypothesis](https://hypothesis.readthedocs.io/) for this.

### Key Properties Tested

**Property 3: Git Repository Initialization**
- For any valid project name, initializing a Git repository should create a valid .git directory
- Required files (HEAD, config, objects, refs) should exist
- Repository should be usable for Git operations

**Property 4: Commit Message Non-Empty** (in test_git_properties.py)
- For any set of changes, commits should have non-empty descriptive messages
- Messages should contain at least 2 words

### Test Configuration

Tests run with the following Hypothesis settings:
- **max_examples**: 100 (each property test runs 100 times with different inputs)
- **deadline**: None (no time limit per test)

These settings are configured in `pytest.ini`.

## Test Markers

Tests are marked with pytest markers for easy filtering:

```bash
# Run only property-based tests
pytest -m property

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Writing New Tests

### Property-Based Test Template

```python
from hypothesis import given, settings, strategies as st

# Feature: self-hosted-ai-coding-platform, Property X: Property Name
@settings(max_examples=100)
@given(input_data=st.text())
def test_property_name(input_data: str) -> None:
    """
    Property X: Property Name
    
    For any <input>, <operation> should <expected_behavior>.
    
    Validates: Requirements X.Y
    """
    # Arrange
    setup_test_environment()
    
    # Act
    result = perform_operation(input_data)
    
    # Assert
    assert property_holds(result), "Property violation message"
```

### Unit Test Template

```python
def test_specific_behavior() -> None:
    """Test that specific behavior works correctly."""
    # Arrange
    setup()
    
    # Act
    result = action()
    
    # Assert
    assert result == expected
```

## Continuous Integration

These tests should be run:
- Before committing changes
- In CI/CD pipeline
- After deploying to staging/production

## Troubleshooting

### Import Errors

If you get import errors, ensure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Git Tests Failing

Git tests require Git to be installed:
```bash
# Check Git installation
git --version

# Install Git if needed (Ubuntu/Debian)
sudo apt-get install git
```

### Docker Tests Failing

Some tests may require Docker to be running:
```bash
# Check Docker status
docker info
```

## References

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitPython Documentation](https://gitpython.readthedocs.io/)
