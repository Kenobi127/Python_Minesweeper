# 💣 Minesweeper (Tkinter & CLI)

A desktop implementation of the classic Minesweeper game built in Python using Tkinter, featuring custom graphics, and an alternative terminal-based CLI mode.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License: PolyForm NC](https://img.shields.io/badge/License-PolyForm%20NC-blue)

---

## ✨ Features

* **Interactive GUI:** Built with Tkinter, featuring custom flag and mine graphics, dynamic counters, and real-time game tracking.
* **First-Click Protection:** Guarantees that the player's initial click is never a mine.
* **Recursive Clearance:** Automatically expands empty regions when clicking zero-mine cells.
* **Cross-Platform Compatibility:** Uses modern `pathlib` for relative asset loading across Windows, macOS, and Linux.
* **Dual Interface:** Includes both the primary GUI application and a standalone terminal/CLI version.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher.
* Tkinter (included with standard Python installations on Windows and macOS).

### Running the GUI Application

From the root project directory, run:

```bash
python src/tkinter_version.py
```

### Running the Terminal Version

If you want to play the command-line version:

```bash
python cli/terminal_version.py
```

---

## Author

**Mateo Lopez Moncaleano**
