"""
Disk Explorer - Command Line Interface
Day 68 of 365 Days of Python

This module provides a command-line interface for the file system analyzer.
"""

import os
import sys
import argparse
from file_analyzer import scan_directory, format_size, get_directory_summary


def create_bar_chart(data, max_width=50):
    """Create a simple ASCII bar chart."""
    if not data:
        return "No data to display"
    
    # Find the maximum value for scaling
    max_value = max(data.values())
    
    # Sort items by value in descending order
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
    # Determine the longest label for alignment
    longest_label = max(len(label) for label, _ in sorted_items)
    
    chart = []
    for label, value in sorted_items:
        # Calculate bar width
        bar_width = int((value / max_value) * max_width) if max_value > 0 else 0
        
        # Format the value
        formatted_value = format_size(value)
        
        # Create the bar
        bar = f"{label.ljust(longest_label)} | {'█' * bar_width} {formatted_value}"
        chart.append(bar)
    
    return "\n".join(chart)


def find_large_files(directory, min_size_mb=100, count=20):
    """Find large files in a directory."""
    min_size_bytes = min_size_mb * 1024 * 1024
    scan_result = scan_directory(directory, min_size=min_size_bytes)
    
    if "error" in scan_result:
        return scan_result["error"]
    
    # Sort all files by size
    sorted_files = sorted(scan_result["files"], key=lambda x: x["size"], reverse=True)
    
    result = []
    result.append(f"Top {min(count, len(sorted_files))} largest files in {directory}:")
    result.append(f"(Minimum size: {min_size_mb} MB)")
    result.append("")
    
    for i, file_info in enumerate(sorted_files[:count], 1):
        result.append(f"{i}. {file_info['path']}")
        result.append(f"   Size: {format_size(file_info['size'])}")
        result.append(f"   Type: {file_info['type'].capitalize()}")
        result.append(f"   Modified: {file_info['modified']}")
        result.append("")
    
    return "\n".join(result)


def analyze_dir_types(directory):
    """Analyze file types in a directory and display as chart."""
    scan_result = scan_directory(directory)
    
    if "error" in scan_result:
        return scan_result["error"]
    
    result = []
    result.append(f"File type analysis for {directory}")
    result.append(f"Total size: {format_size(scan_result['total_size'])}")
    result.append("")
    result.append("File Type Distribution:")
    result.append(create_bar_chart(scan_result["type_stats"]))
    
    return "\n".join(result)


def interactive_mode():
    """Run in interactive mode."""
    print("Disk Explorer - Interactive Mode")
    print("--------------------------------")
    
    while True:
        print("\nChoose an option:")
        print("1. Scan directory")
        print("2. Find large files")
        print("3. Analyze file types")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            directory = input("Enter directory path (or press Enter for current directory): ")
            if not directory:
                directory = os.getcwd()
            
            if not os.path.exists(directory):
                print(f"Error: Directory '{directory}' does not exist.")
                continue
                
            print(f"\nScanning {directory}...")
            result = scan_directory(directory)
            print("\n" + get_directory_summary(result))
            
        elif choice == "2":
            directory = input("Enter directory path (or press Enter for current directory): ")
            if not directory:
                directory = os.getcwd()
                
            if not os.path.exists(directory):
                print(f"Error: Directory '{directory}' does not exist.")
                continue
                
            try:
                min_size = int(input("Minimum file size in MB (default: 100): ") or "100")
                count = int(input("Number of files to show (default: 20): ") or "20")
            except ValueError:
                print("Error: Please enter valid numbers.")
                continue
                
            print(f"\nSearching for large files in {directory}...")
            print("\n" + find_large_files(directory, min_size, count))
            
        elif choice == "3":
            directory = input("Enter directory path (or press Enter for current directory): ")
            if not directory:
                directory = os.getcwd()
                
            if not os.path.exists(directory):
                print(f"Error: Directory '{directory}' does not exist.")
                continue
                
            print(f"\nAnalyzing file types in {directory}...")
            print("\n" + analyze_dir_types(directory))
            
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main entry point for the program."""
    parser = argparse.ArgumentParser(description="Disk Explorer - Analyze file system usage")
    
    # Create a group for main commands
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument("--scan", "-s", metavar="DIR", help="Scan a directory and show summary")
    command_group.add_argument("--large", "-l", metavar="DIR", help="Find large files in a directory")
    command_group.add_argument("--types", "-t", metavar="DIR", help="Analyze file types in a directory")
    command_group.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    
    # Additional options
    parser.add_argument("--min-size", type=int, default=100, help="Minimum file size in MB (for --large)")
    parser.add_argument("--count", type=int, default=20, help="Number of files to show (for --large)")
    
    args = parser.parse_args()
    
    # Run in interactive mode if no arguments or --interactive is specified
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    # Handle scan command
    if args.scan:
        target_dir = args.scan if os.path.exists(args.scan) else os.getcwd()
        result = scan_directory(target_dir)
        print(get_directory_summary(result))
        
    # Handle large files command
    elif args.large:
        target_dir = args.large if os.path.exists(args.large) else os.getcwd()
        print(find_large_files(target_dir, args.min_size, args.count))
        
    # Handle file types command
    elif args.types:
        target_dir = args.types if os.path.exists(args.types) else os.getcwd()
        print(analyze_dir_types(target_dir))


if __name__ == "__main__":
    main()