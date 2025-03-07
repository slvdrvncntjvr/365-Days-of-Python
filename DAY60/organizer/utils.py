"""
Utility functions for the file organizer.
"""

import os
from typing import Dict, List

def count_files_in_dir(directory: str) -> int:
    """
    Count the number of files in a directory (non-recursive).
    
    Args:
        directory: The directory to count files in
        
    Returns:
        The number of files in the directory
    """
    return len([f for f in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory, f))])

def get_file_size_category(size_bytes: int) -> str:
    """
    Categorize a file based on its size.
    
    Args:
        size_bytes: The size of the file in bytes
        
    Returns:
        A category string
    """
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    
    if size_bytes < kb:
        return "tiny_less_than_1KB"
    elif size_bytes < 10 * kb:
        return "small_1KB_10KB"
    elif size_bytes < 100 * kb:
        return "medium_10KB_100KB"
    elif size_bytes < mb:
        return "large_100KB_1MB"
    elif size_bytes < 10 * mb:
        return "very_large_1MB_10MB"
    elif size_bytes < 100 * mb:
        return "huge_10MB_100MB"
    elif size_bytes < gb:
        return "enormous_100MB_1GB"
    else:
        return "massive_over_1GB"

def print_summary(moved_files: Dict[str, List[str]]) -> None:
    """
    Print a summary of the moved files.
    
    Args:
        moved_files: Dictionary mapping categories to lists of moved files
    """
    total_moved = sum(len(files) for files in moved_files.values())
    
    if total_moved == 0:
        print("\nNo files were moved.")
        return
    
    print(f"\nMoved {total_moved} files into {len(moved_files)} categories:")
    
    for category, files in sorted(moved_files.items()):
        print(f"\n{category} ({len(files)} files):")
        # Show first 5 files in each category, then "..." if there are more
        for file in files[:5]:
            print(f"  - {file}")
        if len(files) > 5:
            print(f"  - ... and {len(files) - 5} more")