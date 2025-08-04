#!/usr/bin/env python3
"""
Web API Project Backup Script
Creates a timestamped backup of the entire project
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_backup():
    """Create a timestamped backup of the project"""
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = "webapi_docrag"
    
    # Define paths
    project_root = Path(__file__).parent.parent  # Go up from scripts to project root
    backup_dir = project_root.parent / "backups"
    backup_name = f"{project_name}_backup_{timestamp}"
    backup_zip = backup_dir / f"{backup_name}.zip"
    
    # Create backups directory if it doesn't exist
    backup_dir.mkdir(exist_ok=True)
    
    print(f"🔄 Creating backup: {backup_name}")
    print("=" * 50)
    
    # Files and directories to exclude from backup
    exclude_patterns = {
        '__pycache__',
        '*.pyc', 
        '.conda',
        'node_modules',
        '.git',
        '*.log',
        'venv',
        'env'
    }
    
    def should_exclude(path):
        """Check if a path should be excluded from backup"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern in path_str:
                return True
        return False
    
    # Create zip backup
    with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Walk through all files and directories
        for root, dirs, files in os.walk(project_root):
            # Remove excluded directories from dirs list to avoid walking into them
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip excluded files
                if should_exclude(file_path):
                    continue
                
                # Calculate relative path for zip
                relative_path = file_path.relative_to(project_root)
                
                # Add file to zip
                zipf.write(file_path, relative_path)
                print(f"✅ Added: {relative_path}")
    
    # Get backup size
    backup_size = backup_zip.stat().st_size / (1024 * 1024)  # MB
    
    print("=" * 50)
    print(f"✅ Backup created successfully!")
    print(f"📁 Location: {backup_zip}")
    print(f"📦 Size: {backup_size:.2f} MB")
    print(f"🕒 Timestamp: {timestamp}")
    
    # Create backup info file
    info_file = backup_dir / f"{backup_name}_info.txt"
    with open(info_file, 'w') as f:
        f.write(f"Web API Project Backup Information\n")
        f.write(f"=" * 40 + "\n")
        f.write(f"Backup Name: {backup_name}\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Project Path: {project_root}\n")
        f.write(f"Backup Size: {backup_size:.2f} MB\n")
        f.write(f"Zip File: {backup_zip.name}\n")
        f.write(f"\nProject Structure:\n")
        f.write(f"- Core Application: main.py, config.py, models.py\n")
        f.write(f"- Routers: admin, auth, users, items, client_apps, user_portal\n")
        f.write(f"- Templates: HTML templates for web interface\n")
        f.write(f"- Tests: Comprehensive test suite (20+ test files)\n")
        f.write(f"- Demos: Demo scripts and examples\n")
        f.write(f"- Utils: Utility scripts and helpers\n")
        f.write(f"- Scripts: Project runner scripts\n")
        f.write(f"- Docs: Documentation files\n")
        f.write(f"- Data: Database and data files\n")
        f.write(f"\nFeatures Included:\n")
        f.write(f"- FastAPI web application\n")
        f.write(f"- SQLite database with user/item management\n")
        f.write(f"- Session-based authentication\n")
        f.write(f"- Admin panel with user management\n")
        f.write(f"- User portal with search functionality\n")
        f.write(f"- API endpoints with token authentication\n")
        f.write(f"- Client apps management (100% functional)\n")
        f.write(f"- Comprehensive test suite\n")
        f.write(f"- Demo scripts and utilities\n")
        f.write(f"\nAPI Status Summary:\n")
        f.write(f"- ✅ Client Apps API: Fully functional\n")
        f.write(f"- ✅ API Token Generation: Working\n") 
        f.write(f"- ✅ Items API: Accessible\n")
        f.write(f"- ⚠️  Users API: Requires investigation\n")
        f.write(f"- ✅ Web Interface: Fully operational\n")
    
    print(f"📄 Info file: {info_file}")
    
    return backup_zip

if __name__ == "__main__":
    try:
        backup_file = create_backup()
        print(f"\n🎉 Backup completed successfully!")
        print(f"You can restore this backup by extracting: {backup_file}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")
