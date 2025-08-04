# Demos and Utilities Documentation

This directory contains demo scripts, utilities, and sample files for the Web API application. These files are used for testing, debugging, demonstration, and development purposes.

## 📁 Directory Contents

### 🎯 Demo Scripts

#### **Admin Interface Demos**
- `admin_structure_demo.py` - Demonstrates the admin interface structure and navigation
- `user_portal_access_demo.py` - Shows user portal access patterns and functionality

#### **Authentication Demos**  
- `api_token_demo.py` - Demonstrates API token generation and usage
- `get_test_token_demo.py` - Simple script to get test tokens for API testing
- `swagger_demo.py` - Shows how to use Swagger UI with authentication
- `login_context_demo.py` - Demonstrates login context and session management
- `login_error_context_demo.py` - Shows login error handling scenarios

#### **Token Management Demos**
- `demo_token_creator.py` - Creates demo tokens for testing purposes
- `demo_credentials_fix.py` - Demonstrates credential management fixes
- `token_generator.py` - Utility for generating various types of tokens
- `get_bearer_token.py` - Script to obtain bearer tokens for API access
- `simple_token_guide.py` - Simple guide for token usage

### 🔧 Utility Scripts

#### **Debugging Tools**
- `debug_auth.py` - Authentication debugging utilities
- `debug_client_apps.py` - Client app debugging and troubleshooting
- `check_db_users.py` - Database user verification and debugging
- `auth_fix_summary.py` - Summary of authentication fixes and improvements

#### **Development Tools**
- `run.py` - Alternative application runner script

### 📄 Sample Files

#### **HTML Samples**
- `error_page_sample.html` - Sample error page output for testing
- `test_login.html` - Test login page for debugging

#### **Shell Scripts**
- `curl_examples.sh` - cURL command examples for API testing

## 🚀 Usage Examples

### Running Demo Scripts

```bash
# Run from the demos directory
cd demos
python admin_structure_demo.py

# Or run from the main directory  
python demos/api_token_demo.py
```

### Common Demo Workflows

#### **1. API Token Demo**
```bash
python demos/api_token_demo.py
```
- Shows complete API token workflow
- Demonstrates token creation and usage
- Tests API endpoints with authentication

#### **2. Admin Structure Demo**
```bash
python demos/admin_structure_demo.py
```
- Shows admin interface navigation
- Demonstrates admin functionality
- Tests admin access patterns

#### **3. Authentication Testing**
```bash
python demos/get_test_token_demo.py
python demos/swagger_demo.py
```
- Creates test tokens
- Shows Swagger UI authentication
- Tests various auth scenarios

### Utility Scripts

#### **Token Generation**
```bash
python demos/token_generator.py
python demos/get_bearer_token.py
```

#### **Debugging**
```bash
python demos/debug_auth.py
python demos/check_db_users.py
```

## 📋 Requirements

Most demo scripts require:
- The Web API server running on `http://127.0.0.1:8000`
- Default demo users (admin/admin123, user/user123)
- Python packages: `requests`, `beautifulsoup4` (for some scripts)

## 🎯 Purpose

### **For Developers**
- **Learning**: Understand how different components work
- **Testing**: Quick scripts to test functionality
- **Debugging**: Tools to diagnose issues
- **Examples**: Reference implementations

### **For Users**
- **Demonstration**: See features in action
- **Tutorials**: Step-by-step guides
- **Validation**: Verify system functionality

### **For Documentation**
- **Samples**: Generated sample outputs
- **Examples**: Working code examples
- **References**: Quick reference scripts

## 🔄 Development Workflow

1. **Create Feature** → Write demo script to test it
2. **Find Bug** → Create debug script to isolate it  
3. **Add Authentication** → Update auth demo scripts
4. **Update API** → Update API demo scripts
5. **Document Feature** → Create sample files

## 📝 Notes

- Demo scripts are meant for development and testing
- They may create temporary data or files
- Sample files show expected outputs
- Utility scripts help with common development tasks
- All scripts are self-contained and documented

## 🛠️ Maintenance

- Demo scripts should be updated when features change
- Sample files should reflect current application output
- Utility scripts should be kept current with the main codebase
- Documentation should be updated with new demos

---

*This directory helps maintain a clean main project structure while providing comprehensive development and demonstration resources.*
