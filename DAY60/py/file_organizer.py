

import argparse
import os
import sys
from organizer.sorters import organize_by_extension, organize_by_date, organize_by_size
from organizer.utils import count_files_in_dir, print_summary

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Organize files in a directory")
    parser.add_argument("--dir", type=str, default=".",
                        help="Directory to organize (default: current directory)")
    parser.add_argument("--by", type=str, choices=["ext", "date", "size"],
                        default="ext", help="Criteria to organize by (default: ext)")
    parser.add_argument("--reverse", action="store_true",
                        help="Sort in reverse order")
    
    return parser.parse_args()

def main():
    """Main function of the file organizer."""
    args = parse_arguments()

    if not os.path.isdir(args.dir):
        print(f"Error: '{args.dir}' is not a valid directory.")
        sys.exit(1)
    
    initial_count = count_files_in_dir(args.dir)
    print(f"Found {initial_count} files in '{args.dir}'")
    
    if args.by == "ext":
        moved_files = organize_by_extension(args.dir, args.reverse)
    elif args.by == "date":
        moved_files = organize_by_date(args.dir, args.reverse)
    elif args.by == "size":
        moved_files = organize_by_size(args.dir, args.reverse)
    
    print_summary(moved_files)
    
    print(f"\nOrganization complete! Files organized by {args.by}.")

if __name__ == "__main__":
    main()