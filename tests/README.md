# Test Suite Documentation

This directory contains all test files for the Web API application. The tests are organized by functionality and purpose.

## Test Categories

### 🔐 Authentication & Authorization Tests
- `test_authorization_errors.py` - Tests authorization error handling
- `test_comprehensive_auth.py` - Comprehensive authorization testing
- `test_login_error.py` - Login process error testing
- `test_session_debug.py` - Session debugging tests
- `test_swagger_auth.py` - Swagger UI authentication tests

### 🔧 API Tests
- `test_api.py` - Basic API functionality tests
- `test_api_edge_cases.py` - API edge case and error handling tests
- `test_api_quick.py` - Quick API validation tests
- `test_api_token_error.py` - API token error testing
- `test_complete_flow.py` - End-to-end API workflow tests
- `test_create_app_and_test.py` - Client app creation and testing
- `test_end_to_end_api.py` - Complete API integration tests
- `test_improved_api.py` - Enhanced API testing with authentication
- `test_quick_api.py` - Fast API endpoint validation

### 👥 User Interface Tests
- `test_user_portal_admin_links.py` - User portal admin link testing
- `test_user_portal_redirect.py` - User portal redirect testing
- `test_user_search_access.py` - User search access tests
- `test_user_search_direct.py` - Direct user search tests

### 📊 Data Management Tests
- `test_item_edit.py` - Item editing functionality
- `test_item_management.py` - Item CRUD operations

### 🎨 UI & Error Page Tests
- `test_error_page_preview.py` - Error page display testing

### 🛠️ Admin Interface Tests
- `test_admin.py` - Admin interface functionality

## Running Tests

### Individual Test Files
```bash
# Run from the tests directory
cd tests
python test_authorization_errors.py

# Or run from the main directory
python tests/test_authorization_errors.py
```

### All Tests (if using pytest)
```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_api*.py
pytest tests/test_auth*.py
```

## Test Requirements

Most tests require:
- The Web API server running on `http://127.0.0.1:8000`
- Default test users:
  - Admin: `admin` / `admin123`
  - Regular user: `user` / `user123`

## Test Data

Tests create temporary data and should clean up after themselves. Some tests may:
- Create temporary client applications
- Generate test tokens
- Create test users/items
- Save sample output files

## Notes

- Tests are designed to be run individually or as a suite
- Each test file is self-contained with its own setup
- Output files (like `error_page_sample.html`) may be created during testing
- Tests include both positive and negative test cases
- Error handling and edge cases are thoroughly tested
