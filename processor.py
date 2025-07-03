import subprocess
import os

def flip_video(input_path, output_path, direction='horizontal'):
    filter_opt = 'hflip' if direction == 'horizontal' else 'vflip'
    command = ['ffmpeg', '-i', input_path, '-vf', filter_opt, '-c:a', 'copy', output_path]
    subprocess.run(command)

def split_video(input_path, output_folder, segment_time=600):
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_pattern = os.path.join(output_folder, f"{base_name}_part_%03d.mp4")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    command = ['ffmpeg', '-i', input_path, '-c', 'copy', '-map', '0', '-f', 'segment', '-segment_time', str(segment_time), output_pattern]
    subprocess.run(command)
