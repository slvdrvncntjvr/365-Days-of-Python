"""
File sorting implementations for the organizer.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from .utils import get_file_size_category

def organize_by_extension(directory: str, reverse: bool = False) -> Dict[str, List[str]]:
    """
    Organize files by their extension.
    
    Args:
        directory: The directory to organize
        reverse: Whether to sort in reverse alphabetical order
        
    Returns:
        Dictionary mapping each category to a list of moved files
    """
    moved_files = {}
    
    # Get all files in the directory (non-recursive)
    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))]
    
    # Sort files by extension if requested
    if reverse:
        files.sort(key=lambda x: os.path.splitext(x)[1].lower(), reverse=True)
    else:
        files.sort(key=lambda x: os.path.splitext(x)[1].lower())
    
    for file in files:
        file_path = os.path.join(directory, file)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Get the file extension (or "no_extension" if none)
        _, ext = os.path.splitext(file)
        category = ext[1:].lower() if ext else "no_extension"
        
        # Create category directory if it doesn't exist
        category_dir = os.path.join(directory, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        # Move the file
        destination = os.path.join(category_dir, file)
        try:
            shutil.move(file_path, destination)
            
            # Track moved files
            if category not in moved_files:
                moved_files[category] = []
            moved_files[category].append(file)
            
        except Exception as e:
            print(f"Error moving {file}: {e}")
    
    return moved_files

def organize_by_date(directory: str, reverse: bool = False) -> Dict[str, List[str]]:
    """
    Organize files by their creation/modification date (by month).
    
    Args:
        directory: The directory to organize
        reverse: Whether to sort from newest to oldest
        
    Returns:
        Dictionary mapping each category to a list of moved files
    """
    moved_files = {}
    
    # Get all files in the directory (non-recursive)
    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))]
    
    # Create a list of (file, modification_time) tuples
    file_times = []
    for file in files:
        file_path = os.path.join(directory, file)
        mod_time = os.path.getmtime(file_path)
        file_times.append((file, mod_time))
    
    # Sort files by modification time
    file_times.sort(key=lambda x: x[1], reverse=reverse)
    
    for file, mod_time in file_times:
        file_path = os.path.join(directory, file)
        
        # Format the date as YYYY-MM
        date_obj = datetime.fromtimestamp(mod_time)
        category = date_obj.strftime("%Y-%m")
        
        # Create category directory if it doesn't exist
        category_dir = os.path.join(directory, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        # Move the file
        destination = os.path.join(category_dir, file)
        try:
            shutil.move(file_path, destination)
            
            # Track moved files
            if category not in moved_files:
                moved_files[category] = []
            moved_files[category].append(file)
            
        except Exception as e:
            print(f"Error moving {file}: {e}")
    
    return moved_files

def organize_by_size(directory: str, reverse: bool = False) -> Dict[str, List[str]]:
    """
    Organize files by their size.
    
    Args:
        directory: The directory to organize
        reverse: Whether to sort from largest to smallest
        
    Returns:
        Dictionary mapping each category to a list of moved files
    """
    moved_files = {}

    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))]
    
    file_sizes = []
    for file in files:
        file_path = os.path.join(directory, file)
        size = os.path.getsize(file_path)
        file_sizes.append((file, size))
    
    file_sizes.sort(key=lambda x: x[1], reverse=reverse)
    
    for file, size in file_sizes:
        file_path = os.path.join(directory, file)
        

        category = get_file_size_category(size)
        

        category_dir = os.path.join(directory, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        

        destination = os.path.join(category_dir, file)
        try:
            shutil.move(file_path, destination)

            if category not in moved_files:
                moved_files[category] = []
            moved_files[category].append(file)
            
        except Exception as e:
            print(f"Error moving {file}: {e}")
    
    return moved_files