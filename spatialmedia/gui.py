#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Nuitka compile commands
# nuitka-project: --standalone
# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --output-filename=Spatial Media Metadata Injector
# nuitka-project: --include-data-files=*.ico=Spatial Media Metadata Injector.ico
# nuitka-project: --include-data-files=*.png=Spatial Media Metadata Injector.png

# Windows-specific compile commands
# nuitka-project-if: {OS} == "Windows":
#     nuitka-project: --windows-console-mode=disable
#     nuitka-project: --windows-icon-from-ico=Spatial Media Metadata Injector.ico


"""Spatial Media Metadata Injector GUI

GUI application for examining/injecting spatial media metadata in MP4/MOV files.
"""

import ntpath
import os
import sys
import platform
import ctypes
import traceback

try:
    # python 3
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    import configparser
except ImportError:
    # python 2
    import Tkinter as tk
    from tkFont import Font, nametofont
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    import ttk
except ImportError:
    print("Tkinter library is not available.")
    exit(0)


path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, "..")
sys.path.insert(0, path)
from spatialmedia import metadata_utils

SPATIAL_AUDIO_LABEL = "My video has spatial audio (ambiX ACN/SN3D format)"
HEAD_LOCKED_STEREO_LABEL = "with head-locked stereo"


def make_dpi_aware():
    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
        except AttributeError:
            print("Could not set DPI awareness.")
make_dpi_aware()


class Console():
    def __init__(self):
        self.log = []

    def append(self, text):
        print(text.encode("utf-8"))
        self.log.append(text)


class Application(tk.Frame):
    def action_open(self):
        """Triggers open file dialog, reading new files' metadata."""
        tmp_in_files = filedialog.askopenfilenames(**self.open_options)
        if not tmp_in_files:
            return
        
        # Process first file to show in the UI
        self.in_file = tmp_in_files[0]
        self.all_files = tmp_in_files  # Store all selected files
        
        self.set_message(f"Selected {len(tmp_in_files)} files. Current file: {ntpath.basename(self.in_file)}")
        
        console = Console()
        parsed_metadata = metadata_utils.parse_metadata(self.in_file, console.append)

        metadata = None
        audio_metadata = None
        if parsed_metadata:
            metadata = parsed_metadata.video
            audio_metadata = parsed_metadata.audio

        for line in console.log:
            if "Error" in line:
                self.set_error("Failed to load file %s" % ntpath.basename(self.in_file))
                self.var_spherical.set(0)
                self.var_spatial_audio.set(0)
                self.disable_state()
                self.button_open.configure(state="normal")
                return

        self.enable_state()
        self.checkbox_spherical.configure(state="normal")

        infile = os.path.abspath(self.in_file)
        file_extension = os.path.splitext(infile)[1].lower()

        self.var_spherical.set(1)
        self.spatial_audio_description = metadata_utils.get_spatial_audio_description(
            parsed_metadata.num_audio_channels
        )

        if not metadata:
            self.var_3d.set(0)

        if not audio_metadata:
            self.var_spatial_audio.set(0)

        if metadata:
            metadata = next(iter(metadata.values()))

            if metadata.get("Spherical", "") == "true":
                self.var_spherical.set(1)
            else:
                self.var_spherical.set(0)

            if metadata.get("StereoMode", "") == "top-bottom":
                self.var_3d.set(1)
            else:
                self.var_3d.set(0)

        if audio_metadata:
            self.var_spatial_audio.set(1)
            print(audio_metadata.get_metadata_string())

        self.update_state()

    def action_inject_delay(self):
        """Process all selected files for injection."""
        stereo = None
        if self.var_3d.get():
            stereo = "top-bottom"

        metadata = metadata_utils.Metadata()
        metadata.video = metadata_utils.generate_spherical_xml(stereo=stereo)

        if self.var_spatial_audio.get():
            metadata.audio = metadata_utils.get_spatial_audio_metadata(
                self.spatial_audio_description.order,
                self.spatial_audio_description.has_head_locked_stereo,
            )

        console = Console()
        success_count = 0
        
        for input_file in self.all_files:
            split_filename = os.path.splitext(ntpath.basename(input_file))
            base_filename = split_filename[0]
            extension = split_filename[1]
            
            # Create output filename for each file
            # Fix: Use self.save_file directly as it's already the correct directory path
            output_file = os.path.join(
                #os.path.dirname(self.save_file), # Remove os.path.dirname() call to fix directory path issue
                self.save_file,  # Remove os.path.dirname() call
                f"{base_filename}_injected{extension}"
            )
            
            try:
                metadata_utils.inject_metadata(
                    input_file, output_file, metadata, console.append
                )
                success_count += 1
            except Exception as e:
                console.append(f"Error processing {ntpath.basename(input_file)}: {str(e)}")
        
        self.set_message(
            f"Successfully processed {success_count} out of {len(self.all_files)} files"
        )
        self.button_open.configure(state="normal")
        self.update_state()

    def action_inject(self):
        """Inject metadata into new save files."""
        # Ask for output directory instead of single file
        self.save_file = filedialog.askdirectory(title="Select Output Directory")
        if not self.save_file:
            return

        self.set_message(f"Processing {len(self.all_files)} files...")

        # Launch injection on a separate thread after disabling buttons
        self.disable_state()
        self.master.after(100, self.action_inject_delay)

    def action_set_spherical(self):
        self.update_state()

    def action_set_spatial_audio(self):
        self.update_state()

    def action_set_3d(self):
        self.update_state()

    def enable_state(self):
        self.button_open.configure(state="normal")

    def disable_state(self):
        self.checkbox_spherical.configure(state="disabled")
        self.checkbox_spatial_audio.configure(state="disabled")
        self.checkbox_3D.configure(state="disabled")
        self.button_inject.configure(state="disabled")
        self.button_open.configure(state="disabled")

    def update_state(self):
        self.checkbox_spherical.configure(state="normal")
        if self.var_spherical.get():
            self.checkbox_3D.configure(state="normal")
            self.button_inject.configure(state="normal")
            if self.spatial_audio_description.is_supported:
                self.checkbox_spatial_audio.configure(state="normal")
        else:
            self.checkbox_3D.configure(state="disabled")
            self.button_inject.configure(state="disabled")
            self.checkbox_spatial_audio.configure(state="disabled")
        if self.spatial_audio_description.has_head_locked_stereo:
            self.label_spatial_audio.configure(
                text="{}\n{}".format(SPATIAL_AUDIO_LABEL, HEAD_LOCKED_STEREO_LABEL)
            )
        else:
            self.label_spatial_audio.configure(text=SPATIAL_AUDIO_LABEL)

    def set_error(self, text):
        self.label_message["text"] = text
        self.label_message.config(fg="red")

    def set_message(self, text):
        self.label_message["text"] = text
        self.label_message.config(fg="blue")

    def create_widgets(self):
        """Sets up GUI contents."""

        row = 0
        column = 0

        PAD_X = 10

        row = row + 1
        column = 0
        self.label_message = tk.Label(self)
        self.label_message["text"] = "Click Open to open your 360 video."
        self.label_message.grid(
            row=row,
            column=column,
            rowspan=1,
            columnspan=2,
            padx=PAD_X,
            pady=10,
            sticky="w",
        )

        row = row + 1
        separator = tk.Frame(self, relief=tk.GROOVE, bd=1, height=2, bg="white")
        separator.grid(columnspan=row, padx=PAD_X, pady=4, sticky="n" + "e" + "s" + "w")

        # Spherical Checkbox
        row += 1
        self.label_spherical = tk.Label(self, anchor="w")
        self.label_spherical["text"] = "My video is spherical (360)"
        self.label_spherical.grid(
            row=row, column=column, padx=PAD_X, pady=7, sticky="w"
        )
        column += 1

        self.var_spherical = tk.IntVar()
        self.checkbox_spherical = tk.Checkbutton(self, variable=self.var_spherical)
        self.checkbox_spherical["command"] = self.action_set_spherical
        self.checkbox_spherical.grid(row=row, column=column, padx=PAD_X, pady=2)

        # 3D
        row = row + 1
        column = 0
        self.label_3D = tk.Label(self, anchor="w")
        self.label_3D["text"] = "My video is stereoscopic 3D (top/bottom layout)"
        self.label_3D.grid(row=row, column=column, padx=PAD_X, pady=7, sticky="w")
        column += 1

        self.var_3d = tk.IntVar()
        self.checkbox_3D = tk.Checkbutton(self, variable=self.var_3d)
        self.checkbox_3D["command"] = self.action_set_3d
        self.checkbox_3D.grid(row=row, column=column, padx=PAD_X, pady=2)

        # Spatial Audio Checkbox
        row += 1
        column = 0
        self.label_spatial_audio = tk.Label(self, anchor="w", justify=tk.LEFT)
        self.label_spatial_audio["text"] = SPATIAL_AUDIO_LABEL
        self.label_spatial_audio.grid(
            row=row, column=column, padx=PAD_X, pady=7, sticky="w"
        )

        column += 1
        self.var_spatial_audio = tk.IntVar()
        self.checkbox_spatial_audio = tk.Checkbutton(
            self, variable=self.var_spatial_audio
        )
        self.checkbox_spatial_audio["command"] = self.action_set_spatial_audio
        self.checkbox_spatial_audio.grid(row=row, column=column, padx=0, pady=0)

        row = row + 1
        separator = tk.Frame(self, relief=tk.GROOVE, bd=1, height=2, bg="white")
        separator.grid(
            columnspan=row, padx=PAD_X, pady=10, sticky="n" + "e" + "s" + "w"
        )

        # Button Frame
        column = 0
        row = row + 1
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=row, column=0, columnspan=3, padx=PAD_X, pady=10)

        style = ttk.Style()
        style.configure("TButton", foreground="black")

        self.button_open = ttk.Button(buttons_frame)
        self.button_open["text"] = "Open"
        self.button_open["command"] = self.action_open
        self.button_open.grid(row=0, column=0, padx=14, pady=2)

        self.button_inject = ttk.Button(buttons_frame)
        self.button_inject["text"] = "Inject metadata"
        self.button_inject["command"] = self.action_inject
        self.button_inject.grid(row=0, column=1, padx=14, pady=2)

    def __init__(self, master=None):
        master.wm_title("Spatial Media Metadata Injector")
        master.config(menu=tk.Menu(master))
        self.title = "Spatial Media Metadata Injector"
        self.open_options = {}
        self.open_options["filetypes"] = [("Videos", ("*.mov", "*.mp4"))]
        self.open_options["multiple"] = True  # Enable multiple file selection

        self.save_options = {}

        tk.Frame.__init__(self, master)
        self.create_widgets()
        self.pack()

        self.in_file = None
        self.all_files = []  # Store all selected files
        self.disable_state()
        self.enable_state()
        master.attributes("-topmost", True)
        master.focus_force()
        self.after(50, lambda: master.attributes("-topmost", False))
        self.spatial_audio_description = None


def report_callback_exception(self, *args):
    exception = traceback.format_exception(*args)
    messagebox.showerror("Error", exception)


def main():
    root = tk.Tk()
    root.tk.call('tk', 'scaling', 2.0)
    root.withdraw()
    app_window = tk.Toplevel(root, class_="Spatial Media Metadata Injector")
    app_window.resizable(False, False)

    if platform.system() == "Windows":
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        app_window.iconbitmap("Spatial Media Metadata Injector.ico")
    else:
        app_window.iconphoto(False, tk.PhotoImage(file="Spatial Media Metadata Injector.png"))

    app_window.protocol("WM_DELETE_WINDOW", root.destroy)
    tk.report_callback_exception = report_callback_exception
    Application(master=app_window)
    root.mainloop()


if __name__ == "__main__":
    main()