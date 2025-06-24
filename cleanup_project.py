#!/usr/bin/env python3
"""
Project Cleanup Script for Weather Dominator
Removes unnecessary files and directories while preserving core functionality
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_project():
    """Clean up the Weather Dominator project directory"""
    
    project_root = Path(__file__).parent
    print(f"🧹 Cleaning up project: {project_root}")
    
    # Files and directories to remove
    cleanup_targets = []
    
    # 1. Remove all __pycache__ directories and .pyc files
    pycache_dirs = list(project_root.rglob("__pycache__"))
    cleanup_targets.extend(pycache_dirs)
    
    pyc_files = list(project_root.rglob("*.pyc"))
    cleanup_targets.extend(pyc_files)
    
    # 2. Remove empty models directory
    models_dir = project_root / "models"
    if models_dir.exists() and not any(models_dir.iterdir()):
        cleanup_targets.append(models_dir)
    
    # 3. Remove empty user_preferences directory
    user_prefs_dir = project_root / "data" / "user_preferences"
    if user_prefs_dir.exists() and not any(user_prefs_dir.iterdir()):
        cleanup_targets.append(user_prefs_dir)
    
    # 4. Remove old backup files (keep only the most recent)
    backups_dir = project_root / "data" / "backups"
    if backups_dir.exists():
        backup_files = list(backups_dir.glob("*_backup_*.json"))
        if len(backup_files) > 3:  # Keep only 3 most recent backups
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            old_backups = backup_files[:-3]
            cleanup_targets.extend(old_backups)
    
    # 5. Remove old export files (keep only the most recent)
    exports_dir = project_root / "data" / "exports"
    if exports_dir.exists():
        export_files = list(exports_dir.glob("weather_journal_*.txt"))
        if len(export_files) > 2:  # Keep only 2 most recent exports
            export_files.sort(key=lambda x: x.stat().st_mtime)
            old_exports = export_files[:-2]
            cleanup_targets.extend(old_exports)
    
    # 6. Remove temporary files
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*.log",
        ".DS_Store",
        "Thumbs.db",
        "*.swp",
        "*.swo",
        "*~"
    ]
    
    for pattern in temp_patterns:
        temp_files = list(project_root.rglob(pattern))
        cleanup_targets.extend(temp_files)
    
    # Perform cleanup
    removed_count = 0
    for target in cleanup_targets:
        try:
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                    print(f"🗂️  Removed directory: {target.relative_to(project_root)}")
                else:
                    target.unlink()
                    print(f"🗑️  Removed file: {target.relative_to(project_root)}")
                removed_count += 1
        except Exception as e:
            print(f"⚠️  Failed to remove {target}: {e}")
    
    print(f"\n✅ Cleanup complete! Removed {removed_count} items.")
    
    # Show remaining project structure
    print("\n📁 Final project structure:")
    show_project_structure(project_root)

def show_project_structure(root_path, max_depth=3, current_depth=0, prefix=""):
    """Display the project structure"""
    if current_depth > max_depth:
        return
    
    items = []
    try:
        items = sorted(root_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        # Skip certain files/directories for cleaner output
        skip_items = {".git", ".venv", "__pycache__", ".gitignore", "weather_dominator.db"}
        if item.name in skip_items:
            continue
        
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and current_depth < max_depth:
            next_prefix = prefix + ("    " if is_last else "│   ")
            show_project_structure(item, max_depth, current_depth + 1, next_prefix)

if __name__ == "__main__":
    cleanup_project()
