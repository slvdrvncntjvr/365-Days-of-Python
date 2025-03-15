import os
import time
import curses
import psutil
import platform
from datetime import datetime
from collections import deque
import signal
import sys

# Configuration
UPDATE_INTERVAL = 1.0  # seconds
HISTORY_LENGTH = 60    # data points to keep (for graphs)
GRAPH_WIDTH = 50       # width of graphs in characters

# Initialize data stores
cpu_history = deque([0] * HISTORY_LENGTH, maxlen=HISTORY_LENGTH)
memory_history = deque([0] * HISTORY_LENGTH, maxlen=HISTORY_LENGTH)
net_recv_history = deque([0] * HISTORY_LENGTH, maxlen=HISTORY_LENGTH)
net_sent_history = deque([0] * HISTORY_LENGTH, maxlen=HISTORY_LENGTH)

# Network stats for delta calculation
last_net_io = psutil.net_io_counters()
last_net_time = time.time()

def get_system_info():
    """Get basic system information"""
    uname = platform.uname()
    return {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor if uname.processor else "Unknown",
        "python_version": platform.python_version(),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

def get_cpu_info():
    """Get CPU information"""
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    
    cpu_history.append(cpu_percent)
    
    return {
        "percent": cpu_percent,
        "count": cpu_count,
        "freq_current": cpu_freq.current if cpu_freq else "N/A",
        "freq_max": cpu_freq.max if cpu_freq and cpu_freq.max else "N/A",
        "history": list(cpu_history)
    }

def get_memory_info():
    """Get memory information"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    memory_percent = mem.percent
    memory_history.append(memory_percent)
    
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": memory_percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent,
        "history": list(memory_history)
    }

def get_disk_info():
    """Get disk information"""
    partitions = []
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt' and ('cdrom' in part.opts or part.fstype == ''):
            # Skip CD-ROM on Windows
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError:
            # Skip if we don't have permission
            continue
    
    return partitions

def get_network_info():
    """Get network information"""
    global last_net_io, last_net_time
    
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    
    # Calculate rates
    time_delta = current_time - last_net_time
    recv_rate = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_delta
    sent_rate = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_delta
    
    # Update histories
    net_recv_history.append(recv_rate)
    net_sent_history.append(sent_rate)
    
    # Update last values
    last_net_io = current_net_io
    last_net_time = current_time
    
    return {
        "bytes_sent": current_net_io.bytes_sent,
        "bytes_recv": current_net_io.bytes_recv,
        "packets_sent": current_net_io.packets_sent,
        "packets_recv": current_net_io.packets_recv,
        "sent_rate": sent_rate,
        "recv_rate": recv_rate,
        "sent_history": list(net_sent_history),
        "recv_history": list(net_recv_history)
    }

def format_bytes(bytes_value):
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def draw_horizontal_graph(win, y, x, width, values, max_value=100, title="", color_pair=1):
    """Draw a horizontal graph using Unicode block characters"""
    if max_value <= 0:
        max_value = max(values) if values else 1
    
    # Draw title
    if title:
        win.addstr(y, x, title, curses.A_BOLD)
        y += 1
    
    # Calculate scaling factor
    scale = width / max_value
    
    # Draw the graph
    for i, value in enumerate(values):
        if i >= width:
            break
        
        bar_height = int(value * scale)
        if bar_height > 0:
            win.addstr(y, x + width - i - 1, "█", curses.color_pair(color_pair))
    
    # Draw current value percentage
    current_value = values[0] if values else 0
    win.addstr(y, x + width + 1, f"{current_value:.1f}", curses.color_pair(color_pair))
    
    return y + 1

def draw_progress_bar(win, y, x, width, percent, title="", color_pair=1):
    """Draw a progress bar with percentage"""
    # Draw title
    if title:
        win.addstr(y, x, title, curses.A_BOLD)
        y += 1
    
    # Calculate the number of filled blocks
    filled_width = int(width * percent / 100)
    
    # Draw the progress bar
    win.addstr(y, x, "[")
    for i in range(width):
        if i < filled_width:
            win.addstr("█", curses.color_pair(color_pair))
        else:
            win.addstr(" ")
    win.addstr("]")
    
    # Draw percentage
    win.addstr(y, x + width + 3, f"{percent:.1f}%", curses.color_pair(color_pair))
    
    return y + 1

def main(stdscr):
    """Main function to run the system monitor"""
    # Set up curses
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.use_default_colors()
    
    # Define color pairs
    curses.init_pair(1, curses.COLOR_GREEN, -1)    # Normal/Good
    curses.init_pair(2, curses.COLOR_YELLOW, -1)   # Warning
    curses.init_pair(3, curses.COLOR_RED, -1)      # Critical
    curses.init_pair(4, curses.COLOR_CYAN, -1)     # Info
    curses.init_pair(5, curses.COLOR_BLUE, -1)     # Network
    
    # Get initial system info (static data)
    system_info = get_system_info()
    
    # Main loop
    try:
        while True:
            # Clear screen
            stdscr.clear()
            
            # Get terminal dimensions - FIXED FOR WINDOWS
            max_y, max_x = stdscr.getmaxyx()
            
            # Get real-time data
            cpu_info = get_cpu_info()
            memory_info = get_memory_info()
            disk_info = get_disk_info()
            network_info = get_network_info()
            
            # Display system info
            stdscr.addstr(1, 2, f"System Monitor - {system_info['system']} {system_info['release']}", curses.A_BOLD)
            stdscr.addstr(2, 2, f"Host: {system_info['node']} | Uptime: {calculate_uptime(system_info['boot_time'])}")
            stdscr.addstr(3, 2, f"Python: {system_info['python_version']} | Press 'q' to quit")
            
            # Draw horizontal line
            stdscr.addstr(4, 2, "─" * (max_x - 4))
            
            # Display CPU info
            row = 5
            stdscr.addstr(row, 2, "CPU", curses.A_BOLD)
            row += 1
            stdscr.addstr(row, 4, f"Cores: {cpu_info['count']} | Frequency: {cpu_info['freq_current']:.1f} MHz")
            row += 1
            
            # Determine color based on CPU usage
            cpu_color = 1  # Green by default
            if cpu_info['percent'] > 80:
                cpu_color = 3  # Red for high usage
            elif cpu_info['percent'] > 50:
                cpu_color = 2  # Yellow for medium usage
            
            # Draw CPU usage progress bar
            row = draw_progress_bar(stdscr, row, 4, 50, cpu_info['percent'], "Usage:", cpu_color)
            
            # Draw CPU history graph
            row = draw_horizontal_graph(stdscr, row, 4, GRAPH_WIDTH, cpu_info['history'], 100, "History:", cpu_color)
            row += 1
            
            # Display Memory info
            stdscr.addstr(row, 2, "Memory", curses.A_BOLD)
            row += 1
            stdscr.addstr(row, 4, f"Total: {format_bytes(memory_info['total'])} | Available: {format_bytes(memory_info['available'])}")
            row += 1
            
            # Determine color based on memory usage
            mem_color = 1  # Green by default
            if memory_info['percent'] > 80:
                mem_color = 3  # Red for high usage
            elif memory_info['percent'] > 50:
                mem_color = 2  # Yellow for medium usage
            
            # Draw memory usage progress bar
            row = draw_progress_bar(stdscr, row, 4, 50, memory_info['percent'], "Usage:", mem_color)
            
            # Draw memory history graph
            row = draw_horizontal_graph(stdscr, row, 4, GRAPH_WIDTH, memory_info['history'], 100, "History:", mem_color)
            row += 1
            
            # Display Swap info
            stdscr.addstr(row, 4, f"Swap: {format_bytes(memory_info['swap_total'])} | Used: {format_bytes(memory_info['swap_used'])} ({memory_info['swap_percent']}%)")
            row += 2
            
            # Display Disk info
            stdscr.addstr(row, 2, "Disk", curses.A_BOLD)
            row += 1
            
            for disk in disk_info:
                # Determine color based on disk usage
                disk_color = 1  # Green by default
                if disk['percent'] > 90:
                    disk_color = 3  # Red for high usage
                elif disk['percent'] > 70:
                    disk_color = 2  # Yellow for medium usage
                
                # Show disk info
                stdscr.addstr(row, 4, f"{disk['mountpoint']} ({disk['device']})")
                row += 1
                stdscr.addstr(row, 6, f"Total: {format_bytes(disk['total'])} | Used: {format_bytes(disk['used'])} | Free: {format_bytes(disk['free'])}")
                row += 1
                
                # Draw disk usage progress bar
                row = draw_progress_bar(stdscr, row, 6, 50, disk['percent'], "Usage:", disk_color)
                row += 1
            
            # Display Network info
            stdscr.addstr(row, 2, "Network", curses.A_BOLD)
            row += 1
            stdscr.addstr(row, 4, f"Total Received: {format_bytes(network_info['bytes_recv'])} | Total Sent: {format_bytes(network_info['bytes_sent'])}")
            row += 1
            stdscr.addstr(row, 4, f"Download: {format_bytes(network_info['recv_rate'])}/s | Upload: {format_bytes(network_info['sent_rate'])}/s")
            row += 1
            
            # Draw network download history graph
            row = draw_horizontal_graph(stdscr, row, 4, GRAPH_WIDTH, network_info['recv_history'], 
                                       max(max(network_info['recv_history']), 1), 
                                       "Download History:", 5)
            
            # Draw network upload history graph
            row = draw_horizontal_graph(stdscr, row, 4, GRAPH_WIDTH, network_info['sent_history'], 
                                       max(max(network_info['sent_history']), 1), 
                                       "Upload History:", 5)
            
            # Show current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if max_y > 5 and max_x > len(current_time) + 2:  # Ensure we don't write out of bounds
                stdscr.addstr(max_y - 1, max_x - len(current_time) - 2, current_time)
            
            # Refresh the screen
            stdscr.refresh()
            
            # Check for keypress
            stdscr.timeout(int(UPDATE_INTERVAL * 1000))
            key = stdscr.getch()
            
            # Handle keypresses
            if key == ord('q'):
                break
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Exit curses mode before printing the exception
        curses.endwin()
        print(f"An error occurred: {e}")
        raise

def calculate_uptime(boot_time_str):
    """Calculate system uptime from boot time string"""
    boot_time = datetime.strptime(boot_time_str, "%Y-%m-%d %H:%M:%S")
    uptime_seconds = (datetime.now() - boot_time).total_seconds()
    
    days = int(uptime_seconds // (24 * 3600))
    uptime_seconds %= (24 * 3600)
    hours = int(uptime_seconds // 3600)
    uptime_seconds %= 3600
    minutes = int(uptime_seconds // 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def signal_handler(sig, frame):
    """Handle signals to ensure clean exit"""
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check for required package
    try:
        import psutil
    except ImportError:
        print("This program requires the 'psutil' package.")
        print("Please install it with 'pip install psutil'")
        sys.exit(1)
    
    # Run the curses application
    curses.wrapper(main)