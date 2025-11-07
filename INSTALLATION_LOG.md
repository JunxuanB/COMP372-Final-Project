# Installation Log

## System Requirements

- Python 3.9 or higher
- pip (package manager)

## Installation Steps

### 1. Upgrade pip (optional but recommended)
```bash
python3 -m pip install --upgrade pip
```

### 2. Install Dependencies
```bash
python3 -m pip install matplotlib networkx Pillow numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python3 -c "import matplotlib, networkx, PIL, numpy; print('All dependencies installed!')"
```

### 4. Check Tkinter (built-in GUI library)
```bash
python3 -c "import tkinter; print('Tkinter available')"
```

## Installed Packages

Core dependencies:
- matplotlib 3.9.4
- networkx 3.2.1
- Pillow 11.3.0
- numpy 2.0.2

Tkinter: 8.5 (built-in)

## Notes

Installation may default to user directory on macOS. This is normal and does not affect functionality.
