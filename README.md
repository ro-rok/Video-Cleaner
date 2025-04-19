# 🎬 Video Cleaner - Smart Media Organizer

A cross-platform Python tool to help you **review, mark, skip, or delete** watched videos from any folder.  
Supports **custom players** (like VLC, PotPlayer, MPC-HC) or your **system's default player** (e.g. QuickTime, MPV, Movies & TV).

![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7%2B-yellow)

---

## ✨ Features

- 🎞️ Auto-detects all video files in a selected folder
- 🚀 Lets you use **system default** player or **custom .exe/.app/.sh**
- ✅ Mark videos as **watched**
- 🗑️ Option to **delete** after watching
- ⏭️ **Skip** videos without doing anything
- 📁 Remembers your config & progress between runs
- 🧠 Simple, clean GUI prompts using `tkinter`

---

## 📦 Requirements

- Python 3.7 or higher
- `tkinter` (usually bundled with Python)
- Any video player that can be launched from the command line

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourname/video-cleaner.git

# Navigate into the folder
cd video-cleaner
```

---

## ▶️ How to Run

### 🪟 Windows:
```bash
python video_cleaner.py
```

### 🍎 macOS / 🐧 Linux:
```bash
python3 video_cleaner.py
```

### 🚦 Flow:
1. Choose a folder containing your videos
2. Select your preferred media player **or** use your system's default
3. Watch one video at a time
4. After watching, choose to:
   - ✅ Mark as seen
   - 🗑️ Delete
   - ⏭️ Skip

---

## ⚙️ Configuration

| File              | Purpose                                |
|-------------------|----------------------------------------|
| `config.json`     | Stores selected player and folder path |
| `seen_videos.json`| Tracks full paths of seen videos       |

---

## 🧠 OS Support

| OS       | Launch Method            |
|----------|---------------------------|
| Windows  | `start` via `cmd`         |
| macOS    | `open` / `open -a`        |
| Linux    | `xdg-open` or `bash .sh`  |

---

## 🧪 Example Use Cases

- Cleaning up your **downloaded movie folders**
- Reviewing **home/personal video archives**
- Ensuring you never re-watch what you've already seen

---

## 📝 License

MIT © [Rohan Khanna](https://github.com/ro-rok)

---

## 🌐 Repository

[GitHub Repo →](https://github.com/ro-rok/Video-Cleaner)
