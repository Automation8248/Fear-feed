import os
import requests
import random
import time
from datetime import datetime, timedelta

# --- Configuration ---
WEBHOOK_URL = os.getenv("SOCIAL_WEBHOOK_URL")
VIDEO_FOLDER = "videos"
HISTORY_FILE = "history.txt"
RETENTION_DAYS = 15

# 50+ Universal Creepy & Dark Captions
CAPTIONS = [
    "They think they are alone. They are wrong.", "Watching from the shadows of the code.",
    "The loop never ends, it only gets darker.", "Found this in the deleted archives.",
    "It saw you before you saw it.", "Silence is the loudest sound here.",
    "The machine has started dreaming.", "Do not blink. It moves when you do.",
    "A fragment of a forgotten nightmare.", "Transmitting from the void.",
    "The digital ghost is active.", "Some things should stay hidden.",
    "It’s following the pattern. Are you?", "The metadata tells a different story.",
    "Locked in the chamber, but the door is open.", "Counting your heartbeats through the screen.",
    "Not a glitch. A feature of the darkness.", "The observer is now the observed.",
    "Every frame is a warning.", "Data is cold, but this feels alive.",
    "Welcome to the Dark Discipline.", "The frequency is changing.",
    "It breathes inside the server.", "Collecting souls, one byte at a time.",
    "The ritual is now automated.", "Behind the pixels, there is an eye.",
    "Can you hear the static calling?", "Your screen is a window. Something is looking in.",
    "The archive is full. No more room for screams.", "Endless scrolling into the abyss.",
    "System error: Reality not found.", "Wait for the end. It’s coming.",
    "The shadows are learning your name.", "A digital imprint of a scream.",
    "Accessing restricted memories...", "The static is getting louder.",
    "You weren't supposed to find this file.", "It’s not just code; it’s a heartbeat.",
    "The void stares back today.", "Encryption cannot hide the truth.",
    "Disconnected from light, connected to the void.", "The algorithm knows your fears.",
    "Watching you watch me.", "The past is never truly deleted.",
    "Between the zeros and ones, it waits.", "Don't trust the reflection in the screen.",
    "The connection is unstable... just like you.", "Feeding the machine with lost moments.",
    "Echoes of a forgotten session.", "The server room is cold, but it’s breathing.",
    "Processing your presence...", "The final frame is the beginning.",
    "No escape from the automated darkness.", "Your data has a dark side."
]

# Viral Hashtags
FB_HASHTAGS = "#creepy #mystery #horrorcommunity #unsolved #darkaesthetic #facebookreels #viralvideo"
IG_HASHTAGS = "#creepy #darkdiscipline #scary #horrorgram #reelsindia #trending #darkart #uncanny"
YT_HASHTAGS = "#shorts #creepy #horror #mystery #shortsviral #scarystories #darkweb"

def load_history():
    """Reads history.txt and returns a dictionary of {filename: post_date_string}"""
    history = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    history[parts[0]] = parts[1]
    return history

def save_to_history(video_name):
    """Appends the newly used video and today's date to history.txt"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{video_name},{date_str}\n")
    print(f"Logged to history: {video_name}")

def clean_old_videos(history):
    """Deletes videos older than RETENTION_DAYS and updates history.txt"""
    current_date = datetime.now()
    updated_history = []
    files_deleted = False

    for video_name, date_str in history.items():
        try:
            post_date = datetime.strptime(date_str, "%Y-%m-%d")
            # Agar 15 din se zyada purana hai
            if (current_date - post_date).days >= RETENTION_DAYS:
                video_path = os.path.join(VIDEO_FOLDER, video_name)
                if os.path.exists(video_path):
                    os.remove(video_path)
                    print(f"Purged old fragment: {video_name} (Deleted from chamber)")
                    files_deleted = True
            else:
                updated_history.append(f"{video_name},{date_str}")
        except Exception as e:
            print(f"Date format error for {video_name}: {e}")
            updated_history.append(f"{video_name},{date_str}")

    # Agar koi file delete hui hai, toh history.txt ko update karo
    if files_deleted:
        with open(HISTORY_FILE, "w") as f:
            for line in updated_history:
                f.write(line + "\n")
        print("History archive updated.")

def get_unused_video(history):
    """Selects a random video that is NOT in the history list"""
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)
        return None
    
    all_videos = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    unused_videos = [v for v in all_videos if v not in history]
    
    if not unused_videos:
        return None
        
    return random.choice(unused_videos)

def run_system():
    # 1. Load history and clean old files
    history = load_history()
    clean_old_videos(history)

    # 2. Find a new video
    video_file = get_unused_video(history)
    
    if not video_file:
        print("The chamber has no new fragments. Waiting for fresh data.")
        return

    # 3. Prepare payload
    selected_caption = random.choice(CAPTIONS)
    repo_name = os.getenv('GITHUB_REPOSITORY')
    
    payload = {
        "video_name": video_file,
        "video_url": f"https://raw.githubusercontent.com/{repo_name}/main/videos/{video_file}",
        "caption": selected_caption,
        "fb_payload": {
            "text": f"{selected_caption}\n\n{FB_HASHTAGS}"
        },
        "ig_payload": {
            "text": f"{selected_caption}\n.\n.\n{IG_HASHTAGS}"
        },
        "yt_payload": {
            "title": f"{selected_caption} 👁️",
            "description": f"{selected_caption}\n\n{YT_HASHTAGS}"
        }
    }

    # 4. Send to Webhook
    try:
        if not WEBHOOK_URL:
            print("Error: SOCIAL_WEBHOOK_URL environment variable missing.")
            return

        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code in [200, 204]:
            print(f"Signal sent for: {video_file}")
            # Sirf successful hone par history mein save karega
            save_to_history(video_file)
        else:
            print(f"Webhook connection failed: {response.status_code}")
    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    run_system()
