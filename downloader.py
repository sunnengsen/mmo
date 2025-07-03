import subprocess

def download_video(url, output_folder):
    command = [
        'yt-dlp',
        '-f', 'bestvideo+bestaudio/best',
        '-P', output_folder,
        url
    ]
    subprocess.run(command)
