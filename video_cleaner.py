import os
import json
import random
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
from typing import List, Optional

CONFIG_FILE = "config.json"
SEEN_FILE = "seen_videos.json"
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpeg', '.mpg', '.webm', '.3gp', '.m4v'}

IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")
IS_WINDOWS = sys.platform.startswith("win")

# ---------------- CONFIG HANDLING ---------------- #

def load_config() -> dict:
    if Path(CONFIG_FILE).exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            print("Config file corrupted. Recreating.")
    return {}

def save_config(config: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_player_path(config: dict) -> Optional[str]:
    use_default = config.get("use_default_player")

    if use_default:
        return None

    player_path = config.get("player_path")
    if player_path and Path(player_path).exists():
        return player_path

    root = tk.Tk()
    root.withdraw()

    use_sys = messagebox.askyesno(
        "Use Default Player?",
        "Would you like to use your system's default video player?"
    )

    if use_sys:
        config["use_default_player"] = True
        save_config(config)
        return None

    player_path = filedialog.askopenfilename(
        title="Select Custom Video Player Executable",
        filetypes=[("All Files", "*.*")]
    )

    if not player_path:
        raise FileNotFoundError("No video player selected.")

    config["player_path"] = player_path
    config["use_default_player"] = False
    save_config(config)
    return player_path

def get_root_folder(config: dict) -> Path:
    root = tk.Tk()
    root.withdraw()

    existing_path = config.get("root_folder")
    if existing_path and Path(existing_path).exists():
        reuse = messagebox.askyesno("Use Previous Folder", f"Use previously selected root folder?\n\n{existing_path}")
        if reuse:
            return Path(existing_path)

    selected_path = filedialog.askdirectory(title="Select Root Folder Containing Videos")
    if not selected_path:
        raise FileNotFoundError("No root folder selected.")
    
    config["root_folder"] = selected_path
    save_config(config)
    return Path(selected_path)

# ---------------- VIDEO MANAGEMENT ---------------- #

def load_seen_videos() -> List[str]:
    if Path(SEEN_FILE).exists():
        try:
            with open(SEEN_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            print("Seen video file corrupted. Resetting.")
    return []

def save_seen_videos(seen_videos: List[str]):
    try:
        with open(SEEN_FILE, 'w') as f:
            json.dump(seen_videos, f, indent=4)
        print(f"✅ Saved seen video count: {len(seen_videos)}")
    except Exception as e:
        print(f"❌ Failed to save seen videos: {e}")

def find_all_videos(root_dir: Path) -> List[Path]:
    return [f for f in root_dir.rglob("*") if f.suffix.lower() in VIDEO_EXTENSIONS and f.is_file()]

def filter_unseen(videos: List[Path], seen: List[str]) -> List[Path]:
    return [v for v in videos if str(v.resolve()) not in seen]

# ---------------- GUI INTERACTIONS ---------------- #

def prompt_action(video_path: Path) -> Optional[str]:
    choice = {"action": None}

    def on_mark_seen():
        choice["action"] = "seen"
        root.quit()

    def on_delete():
        choice["action"] = "delete"
        root.quit()

    def on_skip():
        choice["action"] = "skip"
        root.quit()

    root = tk.Tk()
    root.title("Video Watched")
    root.geometry("400x180")

    label = tk.Label(root, text=f"What do you want to do with:\n{video_path.name}", wraplength=350)
    label.pack(padx=20, pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    seen_btn = tk.Button(btn_frame, text="Mark as Seen", width=15, command=on_mark_seen)
    seen_btn.grid(row=0, column=0, padx=10)

    delete_btn = tk.Button(btn_frame, text="Delete", width=15, command=on_delete)
    delete_btn.grid(row=0, column=1, padx=10)

    skip_btn = tk.Button(root, text="Skip", width=32, command=on_skip)
    skip_btn.pack(pady=10)

    root.mainloop()
    root.destroy()
    return choice["action"]

def show_done_popup():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Done", "🎉 No more unseen videos available.")
    root.destroy()

# ---------------- VIDEO LAUNCH ---------------- #

def launch_video(player_path: Optional[str], video_path: Path):
    try:
        if player_path:  # Use custom player
            if IS_MAC and player_path.endswith(".app"):
                subprocess.run(["open", "-a", player_path, str(video_path)], check=True)
            elif IS_LINUX and player_path.endswith(".sh"):
                subprocess.run(["bash", player_path, str(video_path)], check=True)
            else:
                subprocess.run([player_path, str(video_path)], check=True)
        else:
            # Use system default
            if IS_MAC:
                subprocess.run(["open", str(video_path)], check=True)
            elif IS_LINUX:
                subprocess.run(["xdg-open", str(video_path)], check=True)
            elif IS_WINDOWS:
                subprocess.run(["cmd", "/c", "start", "", str(video_path)], shell=True, check=True)
            else:
                raise OSError("Unsupported OS for default video player.")
    except subprocess.CalledProcessError:
        print(f"⚠️ Error occurred while playing video: {video_path}")
        return False
    except Exception as e:
        print(f"❌ Failed to launch video: {e}")
        return False
    return True

# ---------------- MAIN FUNCTION ---------------- #

def main():
    try:
        config = load_config()
        player_path = get_player_path(config)
        root_dir = get_root_folder(config)

        seen_videos = load_seen_videos()
        if not Path(SEEN_FILE).exists():
            print("📝 Creating new seen_videos.json")
            save_seen_videos(seen_videos)

        while True:
            all_videos = find_all_videos(root_dir)
            unseen_videos = filter_unseen(all_videos, seen_videos)

            if not unseen_videos:
                show_done_popup()
                break

            selected_video = random.choice(unseen_videos)
            print(f"▶️ Playing: {selected_video}")

            if not launch_video(player_path, selected_video):
                continue

            action = prompt_action(selected_video)
            resolved_path = str(selected_video.resolve())

            if action == "seen":
                if resolved_path not in seen_videos:
                    seen_videos.append(resolved_path)
                    save_seen_videos(seen_videos)
                else:
                    print("ℹ️ Video already marked as seen.")
            elif action == "delete":
                try:
                    selected_video.unlink()
                    print(f"🗑️ Deleted: {selected_video}")
                except Exception as e:
                    print(f"❌ Failed to delete video: {e}")
            elif action == "skip":
                print("⏭️ Skipped.")
                continue
            else:
                print("⚠️ No valid action selected, skipping.")

    except Exception as e:
        print(f"🚨 Unhandled error: {e}")

# ---------------- ENTRY POINT ---------------- #

if __name__ == "__main__":
    main()
