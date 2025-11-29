# Running Tests on Oracle Cloud Server

**IMPORTANT:** All tests must be run on the Oracle Cloud server, NOT locally.

## Server Information
- **Server:** instance-hulyaekiz
- **IP:** 161.118.171.201
- **Coolify Dashboard:** https://coolify.fpvlovers.com.tr
- **OpenHands UI:** https://ai.fpvlovers.com.tr

## SSH Access
```bash
ssh ubuntu@161.118.171.201
```

## Setup Workspace (One-time)
```bash
# Navigate to project directory
cd /path/to/project

# Run workspace setup script
./scripts/setup-workspace.sh
```

## Running Property-Based Tests

### File Operations Tests (Task 6.2 & 6.3)
```bash
# On the Oracle Cloud server
cd /path/to/project

# Install test dependencies if not already installed
pip3 install -r tests/requirements.txt

# Run file operations property tests
python3 -m pytest tests/test_file_operations.py -v

# Run specific test
python3 -m pytest tests/test_file_operations.py::test_file_creation_preserves_structure -v
python3 -m pytest tests/test_file_operations.py::test_file_modification_preserves_permissions -v
```

### All Property Tests
```bash
# Run all property-based tests
python3 -m pytest tests/ -v -m property

# Run all tests
python3 -m pytest tests/ -v
```

## Test Coverage

### Task 6.2: File Creation Property Test
- **Property 1:** File Creation Preserves Structure
- **Validates:** Requirements 4.1
- **Test File:** `tests/test_file_operations.py::test_file_creation_preserves_structure`

### Task 6.3: File Permission Property Test
- **Property 2:** File Modification Preserves Permissions
- **Validates:** Requirements 4.2
- **Test File:** `tests/test_file_operations.py::test_file_modification_preserves_permissions`

## Notes
- Tests use Hypothesis for property-based testing (100 examples per property)
- Tests create temporary workspaces and clean up automatically
- All tests validate behavior that will occur in the OpenHands container
- Tests can be run locally for development but must pass on the server for validation
