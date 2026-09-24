# File Integrity Checker

A simple Python-based tool to monitor and verify the integrity of files within a directory using SHA-256 hashing. It detects if files have been added, removed, or tampered with by comparing current file hashes against a saved baseline.

## Overview

This project provides a command-line interface to:
- Initialize a baseline of file hashes for a specified directory.
- Compare current file states against the baseline.
- Detect modified (tampered), missing, or newly added files.
- Manually reinitialize the baseline when needed.

## Requirements

- **Python**: 3.12 or higher recommended.
- **Dependencies**: Uses only Python standard libraries (`json`, `pathlib`, `hashlib`).

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OmarAhmedTHE25th/File-Integrity-Checker.git
   cd "File Integrity Checker"
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

## Usage

Run the main script using Python:

```bash
python Checker.py
```

### Interactive Steps:
1. **Enter Path**: Provide the absolute or relative path to the directory you want to monitor.
2. **Manual Reinitialization**: 
   - Enter `y` to delete the existing `hashes.json` and create a new baseline.
   - Enter `n` to check the current directory state against the existing `hashes.json`.

## Scripts

- `Checker.py`: The main entry point for the application. It handles user input, hash calculation, and integrity reporting.

## Environment Variables

- None required.

## Tests

Automated tests are provided to verify the integrity checking logic.

Run the tests using Python's built-in `unittest` framework:
```bash
python test_checker.py
```

Manual verification can be performed by modifying or deleting files in the target directory and running `Checker.py`.

## Project Structure

```text
File Integrity Checker/
├── Checker.py       # Main logic for hashing and comparison
├── test_checker.py  # Automated tests
├── hashes.json      # Storage for file hashes (generated after first run)
├── README.md        # Project documentation
├── LICENSE          # MIT License file
└── .venv/           # Python virtual environment (if created)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
*Based on: [roadmap.sh/projects/file-integrity-checker](https://roadmap.sh/projects/file-integrity-checker)*
