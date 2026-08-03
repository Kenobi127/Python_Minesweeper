# 💣 Minesweeper (Tkinter & CLI)

A desktop implementation of the classic Minesweeper game built in Python using Tkinter, featuring custom graphics, first-click safety, recursive board clearance, and an alternative terminal-based CLI mode.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

* **Interactive GUI:** Built with Tkinter, featuring custom flag and mine graphics, dynamic counters, and real-time game tracking.
* **First-Click Protection:** Guarantees that the player''s initial click is never a mine.
* **Recursive Clearance:** Automatically expands empty regions when clicking zero-mine cells.
* **Cross-Platform Compatibility:** Uses modern `pathlib` for relative asset loading across Windows, macOS, and Linux.
* **Dual Interface:** Includes both the primary GUI application and a standalone terminal/CLI version.

---

## 📁 Project Structure

minesweeper-tkinter/
├── assets/                  # Icons and button images
│   ├── flag.ico
│   ├── flag.png
│   └── mine.png
├── cli/                     # Command-line version
│   └── terminal_version.py
├── src/                     # Main GUI source code
│   ├── __init__.py
│   └── app.py               # Main application entry point
├── .gitignore               # Environment and cache exclusion settings
└── README.md                # Documentation

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher.
* Tkinter (included with standard Python installations on Windows and macOS).

### Running the GUI Application

From the root project directory, run:

python src/app.py

### Running the Terminal Version

If you want to play the command-line version:

python cli/terminal_version.py

---

## 👨‍💻 Author

**Mateo Lopez Moncaleano**