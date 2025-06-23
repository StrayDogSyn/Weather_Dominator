#!/usr/bin/env python3
"""
cleanup.py - Project Cleanup Script

This script cleans up unnecessary files from the Weather Dominator project:
- Removes __pycache__ directories and .pyc files
- Removes backup files and temporary files
- Cleans up demo and test files (optional)
- Preserves important project files and structure

Usage:
    python cleanup.py [--demo] [--all]
    
Options:
    --demo    Also remove demo files (demo_*.py, *_demo.py)
    --all     Remove all temporary and demo files
    
Author: Weather Dominator Team
Date: June 2025
"""

import os
import sys
import shutil
import argparse
import glob
from pathlib import Path


def remove_pycache_dirs(project_root):
    """Remove all __pycache__ directories recursively"""
    removed_count = 0
    
    for root, dirs, files in os.walk(project_root):
        # Skip .venv directory to avoid touching installed packages
        if '.venv' in root:
            continue
            
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"✅ Removed: {pycache_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {pycache_path}: {e}")
    
    return removed_count


def remove_pyc_files(project_root):
    """Remove all .pyc and .pyo files"""
    removed_count = 0
    
    for root, dirs, files in os.walk(project_root):
        # Skip .venv directory
        if '.venv' in root:
            continue
            
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"✅ Removed: {file_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Error removing {file_path}: {e}")
    
    return removed_count


def remove_backup_files(project_root):
    """Remove backup and temporary files"""
    patterns = ['*.bak', '*.backup', '*~', '*.tmp', '*.temp']
    removed_count = 0
    
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(project_root, '**', pattern), recursive=True):
            # Skip .venv directory
            if '.venv' in file_path:
                continue
                
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    return removed_count


def remove_demo_files(project_root):
    """Remove demo and test files"""
    patterns = ['demo_*.py', '*_demo.py', 'test_*.py', '*_test.py']
    removed_count = 0
    
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(project_root, '**', pattern), recursive=True):
            # Skip .venv directory
            if '.venv' in file_path:
                continue
                
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    return removed_count


def clean_empty_directories(project_root):
    """Remove empty directories (except .venv and important project dirs)"""
    important_dirs = {'.git', '.venv', 'data', 'db', 'ml', 'ui', 'utils'}
    removed_count = 0
    
    for root, dirs, files in os.walk(project_root, topdown=False):
        # Skip .venv and other important directories
        if any(important in root for important in important_dirs):
            continue
            
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                # Only remove if truly empty (no files or subdirs)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"✅ Removed empty directory: {dir_path}")
                    removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {dir_path}: {e}")
    
    return removed_count


def main():
    parser = argparse.ArgumentParser(description="Clean up Weather Dominator project files")
    parser.add_argument('--demo', action='store_true', 
                       help='Also remove demo files (demo_*.py, *_demo.py)')
    parser.add_argument('--all', action='store_true',
                       help='Remove all temporary and demo files')
    
    args = parser.parse_args()
    
    # Get project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("🧹 WEATHER DOMINATOR PROJECT CLEANUP")
    print("=" * 40)
    print(f"Project root: {project_root}")
    print()
    
    total_removed = 0
    
    # Always clean cache and temporary files
    print("1. Removing __pycache__ directories...")
    total_removed += remove_pycache_dirs(project_root)
    
    print("\n2. Removing .pyc/.pyo files...")
    total_removed += remove_pyc_files(project_root)
    
    print("\n3. Removing backup/temporary files...")
    total_removed += remove_backup_files(project_root)
    
    # Conditionally remove demo files
    if args.demo or args.all:
        print("\n4. Removing demo/test files...")
        total_removed += remove_demo_files(project_root)
    
    # Clean empty directories
    print("\n5. Removing empty directories...")
    total_removed += clean_empty_directories(project_root)
    
    print("\n" + "=" * 40)
    print(f"🎉 Cleanup complete! Removed {total_removed} items.")
    
    if not (args.demo or args.all):
        print("\n💡 Tip: Use --demo to also remove demo files")
        print("💡 Tip: Use --all for complete cleanup")
    
    print("\n📁 Project structure preserved:")
    important_files = [
        "main.py", "config.json", "requirements.txt", 
        "data/", "db/", "ml/", "ui/", "utils/"
    ]
    for item in important_files:
        item_path = os.path.join(project_root, item)
        if os.path.exists(item_path):
            print(f"  ✅ {item}")


if __name__ == "__main__":
    main()
