"""
FERDataCollector implementation
"""

import os
import threading
import time
import tkinter as tk
from tkinter import Button, Entry, Frame, Label, Spinbox, filedialog, ttk

import cv2
from PIL import Image, ImageTk


class FERDataCollector:
    """
    A GUI application for collecting facial expression recognition (FER) data using OpenCV.
    Allows users to capture video frames and save them to a specified directory.
    """

    def __init__(self, root):
        """
        Initialize the FER Data Collector application.
        """
        self.root = root
        self.root.title("FER Data Collector")

        self._add_video_region()
        self._add_output_directory_region()
        self._add_video_length_region()
        self._add_data_type_region()
        self._add_start_data_collection_button()
        self._add_recording_task_region()
        self._add_recording_control_region()
        self._add_status_label()

        self.cap = cv2.VideoCapture(0)
        self.data_collection_started = False
        self.stop_video_updating = False
        self.out = None
        self.idx = 0
        self.frames = []

        self.emotion_labels = [
            "Neutral",
            "Calm",
            "Happy",
            "Sad",
            "Angry",
            "Fear",
            "Disgust",
            "Surprise",
        ]
        self.engagement_labels = ["Distracted", "Engaged"]

        self.update_video()

    def _add_video_region(self):
        """
        Create a region with video widget
        """
        self.video_label = Label(self.root)
        self.video_label.pack()

    def _add_output_directory_region(self):
        """
        Create a region with output directory selecting
        """
        dir_frame = Frame(self.root)
        dir_frame.pack(pady=5)

        self.dir_label = Label(dir_frame, text="Output Directory:")
        self.dir_label.pack(side=tk.LEFT, padx=5)

        self.dir_entry = Entry(dir_frame, width=40)
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        self.dir_entry.insert(0, os.getcwd())  # Default to current directory

        self.browse_button = Button(dir_frame, text="Browse", command=self.select_directory)
        self.browse_button.pack(side=tk.LEFT, padx=5)

    def _add_video_length_region(self):
        """
        Create a region with video length selecting
        """
        length_frame = Frame(self.root)
        length_frame.pack(pady=5)

        self.length_label = Label(length_frame, text="Video length (seconds):")
        self.length_label.pack(side=tk.LEFT, padx=5)

        self.length_spinbox = Spinbox(
            length_frame, from_=3, to=10, width=5, textvariable=tk.StringVar(value="5")
        )
        self.length_spinbox.pack(side=tk.LEFT, padx=5)

    def _add_data_type_region(self):
        """
        Create a region with selecting data type for collecting
        """
        data_type_frame = Frame(self.root)
        data_type_frame.pack(pady=5)

        self.data_type_label = Label(data_type_frame, text="Select data type for collecting:")
        self.data_type_label.pack(side=tk.LEFT, padx=5)

        self.data_type_combo = ttk.Combobox(
            data_type_frame, values=["Emotions", "Engagement"], state="readonly"
        )
        self.data_type_combo.pack(side=tk.LEFT, padx=5)
        self.data_type_combo.current(0)

    def _add_start_data_collection_button(self):
        """
        Create a start data collection button
        """
        self.start_data_collection_text = "Start data collection"
        self.stop_data_collection_text = "Stop data collection"
        self.start_button = Button(
            self.root, text=self.start_data_collection_text, command=self.start_stop_data_collection
        )
        self.start_button.pack()

    def _add_recording_task_region(self):
        """
        Create a region with displaying recording task
        """
        recording_task_frame = Frame(self.root)
        recording_task_frame.pack(pady=5)

        self.recording_task_label = Label(recording_task_frame, text="Record video with class:")
        self.recording_task_label.pack(side=tk.LEFT, padx=5)

        self.recording_task = Label(recording_task_frame, text="")
        self.recording_task.pack(side=tk.LEFT, padx=5)

    def _add_recording_control_region(self):
        """
        Create a region with recording control buttons
        """
        recording_control_frame = Frame(self.root)
        recording_control_frame.pack(pady=5)
        self.record_button = Button(
            recording_control_frame, text="Record Video", command=self.start_recording
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        self.play_button = Button(
            recording_control_frame, text="Play Video", command=self.play_video
        )
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.save_button = Button(
            recording_control_frame, text="Save recorded video", command=self.save_video
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.record_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)

    def _add_status_label(self):
        """
        Create a status label
        """
        self.status_label = Label(self.root, text="", fg="black")
        self.status_label.pack(pady=5)

    def select_directory(self):
        """
        Create a dialog for selecting output directory
        """
        directory = filedialog.askdirectory(initialdir=self.dir_entry.get())
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def update_video_frame(self, frame, text=""):
        """
        Function which is used to display frame in a video widget
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if text != "":
            position = (10, 30)  # Coordinates (x, y) for top-left corner
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (255, 0, 0)
            thickness = 2

            # Write the text on the image
            cv2.putText(frame, text, position, font, font_scale, color, thickness)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def update_video(self):
        """
        Function which updates frames in video widget
        """
        if not self.stop_video_updating:
            ret, frame = self.cap.read()
            if ret:
                self.update_video_frame(frame)

        self.root.after(10, self.update_video)

    def get_current_class(self):
        """
        Function returns current class which should be recorded
        """
        if self.data_type_combo.get() == "Emotions":
            if self.idx >= len(self.emotion_labels):
                self.idx = 0
            return self.emotion_labels[self.idx]
        if self.idx >= len(self.engagement_labels):
            self.idx = 0
        return self.engagement_labels[self.idx]

    def start_stop_data_collection(self):
        """
        A handler of start data collection button
        """
        self.idx = 0
        if self.data_collection_started:
            self.dir_entry.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)
            self.length_spinbox.config(state=tk.NORMAL)
            self.data_type_combo.config(state=tk.NORMAL)
            self.record_button.config(state=tk.DISABLED)
            self.play_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.start_button.config(text=self.start_data_collection_text)
            self.recording_task.config(text="")
            self.data_collection_started = False
        else:
            self.dir_entry.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.DISABLED)
            self.length_spinbox.config(state=tk.DISABLED)
            self.data_type_combo.config(state=tk.DISABLED)
            self.record_button.config(state=tk.NORMAL)
            self.play_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.start_button.config(text=self.stop_data_collection_text)
            self.recording_task.config(text=self.get_current_class())
            self.data_collection_started = True

    def start_recording(self):
        """
        Function to start video recording
        """
        self.record_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.frames = []

        def _countdown(n):
            if n > 0:
                self.status_label.config(
                    text="Recording will begin in " + str(n) + " s", fg="black"
                )  # Update the label text
                self.root.after(1000, _countdown, n - 1)
            else:
                self.stop_video_updating = True
                duration = int(self.length_spinbox.get())
                threading.Thread(target=self.record, args=(duration,), daemon=True).start()

        _countdown(3)

    def record(self, duration):
        """
        Function which records video and save it to frames list
        """

        def _countdown(n):
            if n > 0:
                self.status_label.config(
                    text="Recording will stop in " + str(n) + " s", fg="black"
                )  # Update the label text
                self.root.after(1000, _countdown, n - 1)

        _countdown(duration)
        start_time = time.time()
        while (time.time() - start_time) < duration:
            ret, frame = self.cap.read()
            if ret:
                self.update_video_frame(frame, "Recording...")
                self.frames.append(frame)
        self.stop_recording()

    def stop_recording(self):
        """
        Function to stop video recording
        """
        self.stop_video_updating = False
        self.record_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.status_label.config(text="", fg="black")

    def play_video(self):
        """
        Function to play recorded video
        """
        self.stop_video_updating = True
        if len(self.frames) > 0:
            threading.Thread(target=self._play_video_thread, daemon=True).start()
        else:
            self.status_label.config(text="Error! Nothing to playback!", fg="red")

    def _play_video_thread(self):
        """
        Separate thread for a video playback
        """
        for frame in self.frames:
            self.update_video_frame(
                frame, "Playback... Recorded class: " + self.get_current_class()
            )
        self.stop_video_updating = False

    def save_video(self):
        """
        Save sequence of frames to a file
        """
        output_dir = self.dir_entry.get()
        file_name = self.get_current_class() + str(int(time.time())) + ".mp4"
        file_name = os.path.join(output_dir, file_name)
        if len(self.frames) > 0:
            self.status_label.config(text="Saving video...", fg="black")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            height, width, _ = self.frames[0].shape
            self.out = cv2.VideoWriter(file_name, fourcc, 10.0, (width, height))
            threading.Thread(target=self._save_video_thread, daemon=True).start()
        else:
            self.status_label.config(text="Error! Nothing to save!", fg="red")
            self.stop_video_updating = False

    def _save_video_thread(self):
        """
        Separate thread for saving video
        """
        for frame in self.frames:
            self.out.write(frame)
        self.status_label.config(text="", fg="black")
        self.out.release()
        self.frames = []
        self.idx += 1
        self.recording_task.config(text=self.get_current_class())
        self.stop_video_updating = False

    def __del__(self):
        """
        Dtor
        """
        self.cap.release()
        if self.out:
            self.out.release()


if __name__ == "__main__":
    tk_app = tk.Tk()
    app = FERDataCollector(tk_app)
    tk_app.mainloop()
