# Installation Log - COMP372 Final Project

**Date**: 2025-11-07
**Project**: Shortest Paths and Minimum Spanning Trees Implementation

---

## System Environment

### Hardware
- **Machine**: Apple MacBook Pro
- **Processor**: Apple M4 Pro
- **RAM**: 24 GB
- **Operating System**: macOS (Darwin 24.4.0)

### Software
- **Python Version**: 3.9.6
- **pip Version (Initial)**: 21.2.4
- **Development Directory**: `/Users/junxuanb/Documents/COMP372-Final-Project`
- **Git Branch**: main

---

## Pre-Installation Check

### Initial Python Environment
**Command executed**:
```bash
python3 --version
```
**Output**: Python 3.9.6

**Command executed**:
```bash
python3 -m pip list
```
**Initial packages**:
```
Package    Version
---------- -------
altgraph   0.17.2
future     0.18.2
macholib   1.15.2
pip        21.2.4
setuptools 58.0.4
six        1.15.0
wheel      0.37.0
```

**Status**: ⚠️ Missing required dependencies (matplotlib, networkx, Pillow)

---

## Installation Steps

### Step 1: Upgrade pip (Optional but Recommended)
**Command**:
```bash
python3 -m pip install --upgrade pip
```
**Purpose**: Upgrade pip from version 21.2.4 to latest version (25.3)
**Status**: ✅ Completed
**Result**: Successfully upgraded pip to version 25.3

---

### Step 2: Install Project Dependencies
**Command**:
```bash
python3 -m pip install matplotlib networkx Pillow numpy
```
**Purpose**: Install all required packages listed in requirements.txt
**Dependencies installed**:
- matplotlib 3.9.4: For graph visualization and plotting
- networkx 3.2.1: For graph data structures and layout algorithms
- Pillow 11.3.0: For GIF animation generation
- numpy 2.0.2: For numerical operations

**Additional dependencies automatically installed**:
- contourpy 1.3.0
- cycler 0.12.1
- fonttools 4.60.1
- kiwisolver 1.4.7
- packaging 25.0
- pyparsing 3.2.5
- python-dateutil 2.9.0.post0
- importlib-resources 6.5.2
- zipp 3.23.0

**Status**: ✅ Completed
**Installation Time**: ~30 seconds

---

### Step 3: Verify Installation
**Command**:
```bash
python3 -c "import matplotlib; import networkx; import PIL; import numpy; print('All dependencies installed successfully')"
```
**Purpose**: Verify all packages are importable
**Status**: ✅ Completed
**Output**: All dependencies installed successfully!

---

### Step 4: Check Tkinter Availability
**Command**:
```bash
python3 -c "import tkinter; print('Tkinter version:', tkinter.TkVersion)"
```
**Purpose**: Verify Tkinter (built-in GUI library) is available
**Note**: Tkinter is typically included with Python installation on macOS
**Status**: ✅ Completed
**Output**: Tkinter version: 8.5
**Result**: Tkinter is available and ready to use for GUI development

---

## Post-Installation Summary

### Installed Packages
**Complete list of Python packages after installation**:
```
Package             Version
------------------- -----------
altgraph            0.17.2
contourpy           1.3.0
cycler              0.12.1
fonttools           4.60.1
future              0.18.2
importlib_resources 6.5.2
kiwisolver          1.4.7
macholib            1.15.2
matplotlib          3.9.4       ← Core dependency
networkx            3.2.1       ← Core dependency
numpy               2.0.2       ← Core dependency
packaging           25.0
pillow              11.3.0      ← Core dependency (PIL)
pip                 25.3        ← Upgraded
pyparsing           3.2.5
python-dateutil     2.9.0.post0
setuptools          58.0.4
six                 1.15.0
wheel               0.37.0
zipp                3.23.0
```

### Installation Issues Encountered
**Status**: ✅ No issues encountered

**Notes**:
- Installation defaulted to user directory (`/Users/junxuanb/Library/Python/3.9/`) because system site-packages is not writeable
- This is normal behavior on macOS and does not affect functionality
- Warning about PATH for scripts (pip, numpy-config, etc.) can be safely ignored for this project

### Verification Results
✅ **All verifications passed successfully**:
1. All required packages (matplotlib, networkx, Pillow, numpy) are importable
2. Tkinter GUI library is available (version 8.5)
3. No import errors or compatibility issues detected
4. Environment is ready for project development

### Total Installation Time
**Approximately 5 minutes** (including pip upgrade and all dependencies)

---

## Notes for Documentation

This installation log will be used to complete the following sections in the project report:

1. **Software Environment Section**:
   - Python version: 3.9.6
   - Operating system: macOS
   - Required libraries and versions
   - Installation method

2. **Hardware Environment Section**:
   - Machine specifications (to be added)
   - Processor details (to be added)

3. **User Manual - Installation Section**:
   - Step-by-step installation instructions
   - Prerequisites
   - Troubleshooting common issues

---

*This log will be updated as installation progresses*
