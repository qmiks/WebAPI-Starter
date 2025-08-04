#!/usr/bin/env python3
"""
Web API Project Restore Script
Restores a project from a backup zip file
"""

import os
import zipfile
import shutil
from pathlib import Path
import argparse

def list_backups():
    """List available backup files"""
    backups_dir = Path(__file__).parent.parent.parent / "backups"
    
    if not backups_dir.exists():
        print("❌ No backups directory found")
        return []
    
    backup_files = list(backups_dir.glob("webapi_docrag_backup_*.zip"))
    
    if not backup_files:
        print("❌ No backup files found")
        return []
    
    print("📋 Available Backups:")
    print("=" * 50)
    
    for i, backup in enumerate(sorted(backup_files), 1):
        size = backup.stat().st_size / (1024 * 1024)  # MB
        print(f"{i}. {backup.name} ({size:.2f} MB)")
    
    return sorted(backup_files)

def restore_backup(backup_file, target_dir=None):
    """Restore a backup to a target directory"""
    
    if target_dir is None:
        target_dir = Path(__file__).parent.parent
    else:
        target_dir = Path(target_dir)
    
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        print(f"❌ Backup file not found: {backup_path}")
        return False
    
    print(f"🔄 Restoring backup: {backup_path.name}")
    print(f"📁 Target directory: {target_dir}")
    print("=" * 50)
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            # Extract all files
            zipf.extractall(target_dir)
            
            # List extracted files
            extracted_files = zipf.namelist()
            print(f"✅ Extracted {len(extracted_files)} files")
            
            # Show some key files
            key_files = ['main.py', 'config.py', 'README.md']
            for key_file in key_files:
                if key_file in extracted_files:
                    print(f"✅ {key_file}")
        
        print("=" * 50)
        print(f"✅ Backup restored successfully!")
        print(f"📁 Project location: {target_dir}")
        print(f"🚀 To run: cd {target_dir} && python main.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Restore Web API project from backup")
    parser.add_argument("--list", action="store_true", help="List available backups")
    parser.add_argument("--backup", type=str, help="Backup file to restore")
    parser.add_argument("--target", type=str, help="Target directory for restore")
    
    args = parser.parse_args()
    
    if args.list:
        list_backups()
        return
    
    if args.backup:
        restore_backup(args.backup, args.target)
        return
    
    # Interactive mode
    backups = list_backups()
    if not backups:
        return
    
    try:
        choice = int(input("\nSelect backup number to restore: ")) - 1
        if 0 <= choice < len(backups):
            backup_file = backups[choice]
            target = input(f"Target directory (Enter for current): ").strip()
            restore_backup(backup_file, target if target else None)
        else:
            print("❌ Invalid selection")
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Operation cancelled")

if __name__ == "__main__":
    main()
