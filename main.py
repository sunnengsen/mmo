import tkinter as tk
from tkinter import filedialog, messagebox
from downloader import download_video
from processor import flip_video, split_video
import os

class VideoToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader & Processor")

        self.url_var = tk.StringVar()
        self.output_dir = tk.StringVar()

        tk.Label(root, text="Video URL:").pack()
        tk.Entry(root, textvariable=self.url_var, width=50).pack()

        tk.Button(root, text="Select Output Folder", command=self.choose_folder).pack()
        tk.Label(root, textvariable=self.output_dir).pack()

        tk.Button(root, text="Download Video", command=self.download).pack(pady=5)
        tk.Button(root, text="Flip Video", command=self.flip).pack(pady=5)
        tk.Button(root, text="Split Video", command=self.split).pack(pady=5)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def download(self):
        url = self.url_var.get()
        folder = self.output_dir.get()
        if not url or not folder:
            messagebox.showerror("Error", "URL and Output Folder are required.")
            return
        download_video(url, folder)
        messagebox.showinfo("Done", "Download finished.")

    def flip(self):
        input_path = filedialog.askopenfilename(title="Select Video to Flip")
        if not input_path:
            return
        output_path = os.path.splitext(input_path)[0] + "_flipped.mp4"
        flip_video(input_path, output_path)
        messagebox.showinfo("Done", f"Flipped video saved to:\n{output_path}")

    def split(self):
        input_path = filedialog.askopenfilename(title="Select Video to Split")
        if not input_path:
            return
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        split_video(input_path, output_folder)
        messagebox.showinfo("Done", f"Video split saved in:\n{output_folder}")

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoToolApp(root)
    root.mainloop()
