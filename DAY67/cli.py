import argparse
import json
import time
import os
import sys
from datetime import datetime

# Ensure the system_monitor module is available
try:
    from system_monitor import (
        get_system_info, get_cpu_info, get_memory_info, 
        get_disk_info, get_network_info, format_bytes, main as curses_main
    )
    print("Successfully imported system_monitor module")
except ImportError as e:
    print(f"Error importing system_monitor.py: {e}")
    print("Make sure system_monitor.py is in the same directory as cli.py")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error when importing system_monitor.py: {e}")
    sys.exit(1)

def print_header(title):
    """Print a formatted header"""
    term_width = os.get_terminal_size().columns
    print("\n" + "=" * term_width)
    print(title.center(term_width))
    print("=" * term_width + "\n")

def print_section(title, content):
    """Print a formatted section with title and content"""
    term_width = os.get_terminal_size().columns
    print("\n" + "-" * term_width)
    print(f" {title} ".center(term_width, "-"))
    print("-" * term_width)
    
    # Print the content with proper indentation
    for line in content.split('\n'):
        print(line)

def print_table(headers, rows):
    """Print a formatted table"""
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print headers
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        print(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))

def print_system_info():
    """Print basic system information"""
    system_info = get_system_info()
    
    content = (
        f"System: {system_info['system']} {system_info['release']}\n"
        f"Version: {system_info['version']}\n"
        f"Hostname: {system_info['node']}\n"
        f"Machine: {system_info['machine']}\n"
        f"Processor: {system_info['processor']}\n"
        f"Python Version: {system_info['python_version']}\n"
        f"Boot Time: {system_info['boot_time']}"
    )
    
    print_section("System Information", content)

def print_cpu_info():
    """Print CPU information"""
    cpu_info = get_cpu_info()
    
    content = (
        f"CPU Usage: {cpu_info['percent']}%\n"
        f"CPU Cores: {cpu_info['count']}\n"
        f"CPU Frequency: {cpu_info['freq_current']} MHz"
    )
    
    if cpu_info['freq_max'] != "N/A":
        content += f" (Max: {cpu_info['freq_max']} MHz)"
    
    print_section("CPU Information", content)
    
    # Print ASCII graph for CPU history
    if cpu_info['history']:
        print("\n  CPU Usage History:")
        print_ascii_graph(cpu_info['history'], 60, 10)

def print_memory_info():
    """Print memory information"""
    memory_info = get_memory_info()
    
    content = (
        f"Total Memory: {format_bytes(memory_info['total'])}\n"
        f"Available Memory: {format_bytes(memory_info['available'])}\n"
        f"Used Memory: {format_bytes(memory_info['used'])} ({memory_info['percent']}%)\n"
        f"Swap Total: {format_bytes(memory_info['swap_total'])}\n"
        f"Swap Used: {format_bytes(memory_info['swap_used'])} ({memory_info['swap_percent']}%)"
    )
    
    print_section("Memory Information", content)
    
    # Print ASCII graph for memory history
    if memory_info['history']:
        print("\n  Memory Usage History:")
        print_ascii_graph(memory_info['history'], 60, 10)

def print_disk_info():
    """Print disk information"""
    disk_info = get_disk_info()
    
    print_section("Disk Information", "")
    
    for disk in disk_info:
        content = (
            f"Device: {disk['device']}\n"
            f"Mount Point: {disk['mountpoint']}\n"
            f"File System: {disk['fstype']}\n"
            f"Total Size: {format_bytes(disk['total'])}\n"
            f"Used Space: {format_bytes(disk['used'])} ({disk['percent']}%)\n"
            f"Free Space: {format_bytes(disk['free'])}"
        )
        
        print(f"\n  {disk['mountpoint']} ({disk['device']}):")
        print("  " + "-" * (os.get_terminal_size().columns - 4))
        
        for line in content.split('\n'):
            print(f"    {line}")
        
        # Print ASCII progress bar
        bar_width = 40
        filled = int(bar_width * disk['percent'] / 100)
        bar = "  Usage: ["
        bar += "#" * filled + " " * (bar_width - filled)
        bar += f"] {disk['percent']}%"
        print(f"\n{bar}")

def print_network_info():
    """Print network information"""
    network_info = get_network_info()
    
    content = (
        f"Total Received: {format_bytes(network_info['bytes_recv'])}\n"
        f"Total Sent: {format_bytes(network_info['bytes_sent'])}\n"
        f"Download Rate: {format_bytes(network_info['recv_rate'])}/s\n"
        f"Upload Rate: {format_bytes(network_info['sent_rate'])}/s\n"
        f"Packets Received: {network_info['packets_recv']}\n"
        f"Packets Sent: {network_info['packets_sent']}"
    )
    
    print_section("Network Information", content)
    
    # Print ASCII graphs for network history
    if network_info['recv_history']:
        print("\n  Download Rate History:")
        max_value = max(max(network_info['recv_history']), 1)
        print_ascii_graph(
            [value / max_value * 100 for value in network_info['recv_history']], 
            60, 10
        )
    
    if network_info['sent_history']:
        print("\n  Upload Rate History:")
        max_value = max(max(network_info['sent_history']), 1)
        print_ascii_graph(
            [value / max_value * 100 for value in network_info['sent_history']], 
            60, 10
        )

def print_ascii_graph(values, width=60, height=10):
    """Print an ASCII graph of values"""
    if not values:
        return
    
    # Normalize values to fit in the height
    max_value = 100  # Values are expected to be percentages
    normalized = []
    for value in values[-width:]:  # Only take the most recent values that fit in the width
        normalized.append(min(int(value * height / max_value), height))
    
    # Print the graph from top to bottom
    for h in range(height, 0, -1):
        line = "    "
        for val in normalized:
            if val >= h:
                line += "█"
            else:
                line += " "
        print(line)
    
    # Print the x-axis
    print("    " + "▔" * len(normalized))
    
    # Print current value
    current = values[0] if values else 0
    print(f"    Current: {current:.1f}%")

def monitor_continuously(interval, output_format):
    """Monitor system resources continuously"""
    try:
        print(f"Starting continuous monitoring (Press Ctrl+C to exit)...")
        time.sleep(1)  # Give user a chance to see the message
        
        while True:
            # Clear screen - use cls on Windows, clear on Unix
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Print current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"System Monitor - {current_time} (Press Ctrl+C to exit)")
            
            if output_format == "text":
                print_system_info()
                print_cpu_info()
                print_memory_info()
                print_disk_info()
                print_network_info()
            
            elif output_format == "json":
                data = {
                    "timestamp": current_time,
                    "system": get_system_info(),
                    "cpu": get_cpu_info(),
                    "memory": get_memory_info(),
                    "disk": get_disk_info(),
                    "network": get_network_info()
                }
                print(json.dumps(data, indent=2))
            
            elif output_format == "compact":
                cpu_info = get_cpu_info()
                memory_info = get_memory_info()
                network_info = get_network_info()
                
                print(f"\nCPU: {cpu_info['percent']}% | Memory: {memory_info['percent']}% | "
                      f"Download: {format_bytes(network_info['recv_rate'])}/s | "
                      f"Upload: {format_bytes(network_info['sent_rate'])}/s")
                
                # Print compact ASCII graphs
                print("\nCPU Usage:    ", end="")
                print_compact_bar(cpu_info['percent'])
                
                print("Memory Usage: ", end="")
                print_compact_bar(memory_info['percent'])
            
            # Wait for the next update
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    except Exception as e:
        print(f"Error during monitoring: {e}")

def print_compact_bar(percent, width=50):
    """Print a compact progress bar"""
    filled = int(width * percent / 100)
    bar = "["
    bar += "#" * filled + " " * (width - filled)
    bar += f"] {percent:.1f}%"
    print(bar)

def export_to_file(filename, format_type):
    """Export system information to a file"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info()
    }
    
    with open(filename, 'w') as f:
        if format_type == 'json':
            json.dump(data, f, indent=2)
        else:  # text format
            f.write(f"System Monitor Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # System Info
            f.write("SYSTEM INFORMATION\n")
            f.write("------------------\n")
            for key, value in data['system'].items():
                f.write(f"{key.capitalize()}: {value}\n")
            
            # CPU Info
            f.write("\nCPU INFORMATION\n")
            f.write("--------------\n")
            f.write(f"Usage: {data['cpu']['percent']}%\n")
            f.write(f"Cores: {data['cpu']['count']}\n")
            f.write(f"Frequency: {data['cpu']['freq_current']} MHz\n")
            
            # Memory Info
            f.write("\nMEMORY INFORMATION\n")
            f.write("------------------\n")
            f.write(f"Total: {format_bytes(data['memory']['total'])}\n")
            f.write(f"Available: {format_bytes(data['memory']['available'])}\n")
            f.write(f"Used: {format_bytes(data['memory']['used'])} ({data['memory']['percent']}%)\n")
            f.write(f"Swap Total: {format_bytes(data['memory']['swap_total'])}\n")
            f.write(f"Swap Used: {format_bytes(data['memory']['swap_used'])} ({data['memory']['swap_percent']}%)\n")
            
            # Disk Info
            f.write("\nDISK INFORMATION\n")
            f.write("----------------\n")
            for disk in data['disk']:
                f.write(f"\n{disk['mountpoint']} ({disk['device']})\n")
                f.write(f"  File System: {disk['fstype']}\n")
                f.write(f"  Total: {format_bytes(disk['total'])}\n")
                f.write(f"  Used: {format_bytes(disk['used'])} ({disk['percent']}%)\n")
                f.write(f"  Free: {format_bytes(disk['free'])}\n")
            
            # Network Info
            f.write("\nNETWORK INFORMATION\n")
            f.write("-------------------\n")
            f.write(f"Total Received: {format_bytes(data['network']['bytes_recv'])}\n")
            f.write(f"Total Sent: {format_bytes(data['network']['bytes_sent'])}\n")
            f.write(f"Download Rate: {format_bytes(data['network']['recv_rate'])}/s\n")
            f.write(f"Upload Rate: {format_bytes(data['network']['sent_rate'])}/s\n")
    
    print(f"System information exported to {filename}")

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="System Resource Monitor CLI")
    
    # Command group
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument("--interactive", action="store_true", help="Run in interactive curses mode (default)")
    command_group.add_argument("--monitor", action="store_true", help="Monitor system resources continuously")
    command_group.add_argument("--snapshot", action="store_true", help="Take a snapshot of current system resources")
    command_group.add_argument("--export", metavar="FILENAME", help="Export system information to a file")
    
    # Options
    parser.add_argument("--interval", type=float, default=1.0, help="Update interval in seconds (default: 1.0)")
    parser.add_argument("--format", choices=["text", "json", "compact"], default="text", help="Output format (default: text)")
    parser.add_argument("--export-format", choices=["text", "json"], default="text", help="Export format (default: text)")
    
    args = parser.parse_args()
    
    # Handle export command
    if args.export:
        export_to_file(args.export, args.export_format)
        return
    
    # Handle snapshot command
    if args.snapshot:
        print_system_info()
        print_cpu_info()
        print_memory_info()
        print_disk_info()
        print_network_info()
        return
    
    # Handle monitor command
    if args.monitor:
        monitor_continuously(args.interval, args.format)
        return
    
    # Default to interactive mode
    try:
        # Import and run the curses-based UI
        print("Starting interactive mode...")
        from system_monitor import main as curses_main
        import curses
        curses.wrapper(curses_main)
    except ImportError:
        print("Error: Could not import curses module")
    except Exception as e:
        print(f"Error starting interactive mode: {e}")

if __name__ == "__main__":
    main()