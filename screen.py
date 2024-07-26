import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import cv2
import numpy as np
from datetime import datetime
import threading

class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture and Recorder")
        self.root.geometry("400x250")  
        self.root.configure(bg="#660000")  

        self.recording = False
        self.filename = ''
        self.record_thread = None

        self.heading_canvas = tk.Canvas(root, width=400, height=40, bg="#660000", bd=0, highlightthickness=0)
        self.heading_canvas.pack(pady=10)
        self.heading_label = tk.Label(
            root,
            text="Screenshot and Screen Record",
            font=("Times New Roman", 14, 'bold'),
            bg="#660000",
            fg="white"
        )
        self.heading_label.place(x=10, y=10)

        self.heading_canvas.create_line(10, 30, 390, 30, fill="black", width=2)

        self.screenshot_button = tk.Button(
            root,
            text="Take Screenshot",
            command=self.take_screenshot,
            font=("Times New Roman", 12, 'bold'),
            bg="white",
            fg="black"
        )
        self.screenshot_button.pack(pady=10)

        self.record_button = tk.Button(
            root,
            text="Start Recording",
            command=self.toggle_recording,
            font=("Times New Roman", 12, 'bold'),
            bg="white",
            fg="black"
        )
        self.record_button.pack(pady=10)

        self.status_label = tk.Label(
            root,
            text="Status: Ready",
            font=("Times New Roman", 12),
            bg="#660000",
            fg="white"
        )
        self.status_label.pack(pady=10)

    def take_screenshot(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            messagebox.showinfo("Success", f"Screenshot saved as {filename}")

    def toggle_recording(self):
        if self.recording:
            self.recording = False
            self.record_button.config(text="Start Recording")
            if self.record_thread:
                self.record_thread.join() 
            self.status_label.config(text="Status: Recording Stopped")
        else:
            self.recording = True
            self.record_button.config(text="Stop Recording")
            self.filename = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
            if self.filename:
                self.record_thread = threading.Thread(target=self.record_screen)
                self.record_thread.start()
                self.status_label.config(text="Status: Recording")

    def record_screen(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.filename, fourcc, 20.0, (screen_size.width, screen_size.height))

        end_time = datetime.now().timestamp() + 10  # Record for 10 seconds

        while self.recording and datetime.now().timestamp() < end_time:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
        
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
