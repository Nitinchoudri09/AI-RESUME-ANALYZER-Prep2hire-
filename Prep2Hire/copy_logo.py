import os, shutil, glob

brain_dir = r"C:\Users\HP\.gemini\antigravity\brain\54d381c8-aa52-4913-bb76-bd1944aa2a81"
static_dir = r"c:\Users\HP\Downloads\Prep2Hire (9)\Prep2Hire\static"

# create static dir if not exists
os.makedirs(static_dir, exist_ok=True)

media_files = glob.glob(os.path.join(brain_dir, "media_*.png"))
if not media_files:
    print("No media files found!")
else:
    latest_file = max(media_files, key=os.path.getmtime)
    print("Latest media file is:", latest_file)
    target_path = os.path.join(static_dir, "logo.png")
    shutil.copy2(latest_file, target_path)
    print("Copied to:", target_path)
