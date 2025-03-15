# System Resource Monitor

Welcome to the System Resource Monitor! This command-line interface (CLI) tool allows you to monitor and manage your system's resources effectively. Whether you need continuous monitoring, a one-time snapshot, or to export your system information, this tool has you covered.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Monitor Mode](#monitor-mode)
  - [Snapshot Mode](#snapshot-mode)
  - [Export Mode](#export-mode)
  - [Interactive Mode](#interactive-mode)
- [Options](#options)
- [Contributing](#contributing)
- [License](#license)

## Usage

You can run the application using the following command:

```bash
python cli.py
```

### Monitor Mode

For continuous monitoring of your system's resources, use the following command:

```bash
python cli.py --monitor --format compact
```

#### Options:
- **Change update interval**: Adjust the update frequency with `--interval`. For example, to update every 2 seconds:
  ```bash
  python cli.py --monitor --interval 2.0
  ```
- **Change output format**: Use `--format` to specify the display format. For a minimal display:
  ```bash
  python cli.py --monitor --format compact
  ```

You can combine options as needed:
```bash
python cli.py --monitor --interval 2.0 --format compact
```

### Snapshot Mode

If you need a one-time snapshot of your current system resources, use:

```bash
python cli.py --snapshot
```

### Export Mode

To export system information to a file, you can use the following commands:

- Export to a text file:
  ```bash
  python cli.py --export system_report.txt
  ```

- Export as JSON:
  ```bash
  python cli.py --export system_report.json --export-format json
  ```

### Interactive Mode

For a more engaging experience, you can run the application in interactive mode:

```bash
python cli.py --interactive
```

In this mode:
- Press `q` to quit.
- Watch real-time graphs update based on your system's resource usage.

### Exiting the Application

- In **monitor mode**, press `Ctrl+C` to exit.

## Options

Here’s a summary of the available options:

- `--monitor`: Enable continuous monitoring.
- `--snapshot`: Take a one-time snapshot of system resources.
- `--export <filename>`: Export system information to a specified file.
- `--export-format <format>`: Specify the format for exported data (e.g., `json`).
- `--interval <seconds>`: Set the update interval for monitor mode.
- `--format <type>`: Choose the output format (e.g., `compact`).

## Contributing

We welcome contributions! If you have suggestions or improvements, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the System Resource Monitor! We hope it helps you keep track of your system's performance effectively. Happy monitoring!