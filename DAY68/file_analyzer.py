import os
import time
from collections import defaultdict
from datetime import datetime


def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except (OSError, FileNotFoundError):
        return 0


def get_file_type(file_path):
    """Determine file type based on extension."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if not ext:
        return "unknown"
    
    # Remove the dot from extension
    ext = ext[1:]
    
    # Group file types
    image_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']
    video_types = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm']
    audio_types = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a']
    document_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv']
    archive_types = ['zip', 'rar', '7z', 'tar', 'gz', 'bz2']
    code_types = ['py', 'js', 'html', 'css', 'java', 'c', 'cpp', 'h', 'php', 'rb']
    
    if ext in image_types:
        return "image"
    elif ext in video_types:
        return "video"
    elif ext in audio_types:
        return "audio"
    elif ext in document_types:
        return "document"
    elif ext in archive_types:
        return "archive"
    elif ext in code_types:
        return "code"
    else:
        return "other"


def scan_directory(directory_path, min_size=0, include_hidden=False):
    """
    Scan a directory and return information about files and subdirectories.
    
    Args:
        directory_path: Path to directory to scan
        min_size: Minimum file size in bytes to include in results
        include_hidden: Whether to include hidden files and directories
        
    Returns:
        dict: Dictionary containing scan results
    """
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return {
            "error": f"Directory does not exist or is not accessible: {directory_path}",
            "files": [],
            "type_stats": {},
            "total_size": 0,
            "largest_files": []
        }
    
    files = []
    largest_files = []
    type_stats = defaultdict(int)
    total_size = 0
    
    # Start time for performance tracking
    start_time = time.time()
    
    for root, dirs, filenames in os.walk(directory_path):
        # Skip hidden directories if not included
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            filenames = [f for f in filenames if not f.startswith('.')]
        
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_size = get_file_size(file_path)
            
            # Skip files smaller than min_size
            if file_size < min_size:
                continue
            
            file_type = get_file_type(file_path)
            modified_time = os.path.getmtime(file_path)
            modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            
            # Calculate relative path from the scanned directory
            rel_path = os.path.relpath(file_path, directory_path)
            
            file_info = {
                "path": rel_path,
                "size": file_size,
                "type": file_type,
                "modified": modified_date
            }
            
            files.append(file_info)
            
            # Update type statistics
            type_stats[file_type] += file_size
            
            # Update total size
            total_size += file_size
            
            # Maintain a list of largest files
            if len(largest_files) < 10:
                largest_files.append(file_info)
                largest_files.sort(key=lambda x: x["size"], reverse=True)
            elif file_size > largest_files[-1]["size"]:
                largest_files[-1] = file_info
                largest_files.sort(key=lambda x: x["size"], reverse=True)
    
    # Calculate scan duration
    duration = time.time() - start_time
    
    return {
        "directory": directory_path,
        "scan_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "duration": f"{duration:.2f} seconds",
        "files": files,
        "file_count": len(files),
        "type_stats": dict(type_stats),
        "total_size": total_size,
        "largest_files": largest_files
    }


def format_size(size_bytes):
    """Format bytes into a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_directory_summary(scan_result):
    """Generate a summary of the directory scan."""
    if "error" in scan_result:
        return scan_result["error"]
    
    summary = []
    summary.append(f"Directory: {scan_result['directory']}")
    summary.append(f"Scan time: {scan_result['scan_time']} (took {scan_result['duration']})")
    summary.append(f"Total files: {scan_result['file_count']}")
    summary.append(f"Total size: {format_size(scan_result['total_size'])}")
    
    # Add file type breakdown
    summary.append("\nFile Type Breakdown:")
    for file_type, size in sorted(scan_result['type_stats'].items(), key=lambda x: x[1], reverse=True):
        percentage = (size / scan_result['total_size']) * 100 if scan_result['total_size'] > 0 else 0
        summary.append(f"  {file_type.capitalize()}: {format_size(size)} ({percentage:.1f}%)")
    
    # Add largest files
    summary.append("\nLargest Files:")
    for i, file_info in enumerate(scan_result['largest_files'], 1):
        summary.append(f"  {i}. {file_info['path']} - {format_size(file_info['size'])}")
    
    return "\n".join(summary)


if __name__ == "__main__":
    # Example usage when run directly
    import sys
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.getcwd()
    
    print(f"Scanning directory: {target_dir}")
    result = scan_directory(target_dir)
    print(get_directory_summary(result))