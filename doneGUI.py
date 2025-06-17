import tkinter as tk
import os
import re
from tkinter import ttk, messagebox
import subprocess
camera_list = []
frame1_list = []

"""
This is the GUI part for LookOut System Connection
It allows users to input camera settings and manage the camera list

It consists of two frames --
Frame1: For adding cameras, entering camera settings and validating inputs to the widgets
Frame2: For displaying the list of added cameras and allowing users to remove or to edit them
Frame1 and Frame2 are used to switch between the two frames
"""
class Frame1(tk.Frame):
    """Frame1: for adding camera settings and managing the camera list."""
    def __init__(self, parent, switch_to_frame2, switch_to_frame3):
        super().__init__(parent)   # Initialize Frame1
        self.switch_to_frame2 = switch_to_frame2   # Switch to Frame2
        self.switch_to_frame3 = switch_to_frame3   # Switch to Frame3
        self.create_widgets()  # Create widgets for Frame1

    def create_widgets(self):
        """Create and layout widgets for Frame1."""
        # Camera path
        path_label = tk.Label(self, text="Folder Path:")
        path_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_path = tk.Entry(self, width=50)
        self.entry_path.grid(row=1, column=1, padx=10, pady=10)

        # Frequency
        freq_label = tk.Label(self, text="Detection Frequency:")
        freq_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_freq = ttk.Combobox(self, values=["30s", "60s", "120s"], state="readonly", width=47)
        self.entry_freq.current(0)
        self.entry_freq.grid(row=2, column=1, padx=10, pady=10)

        # URL
        url_label = tk.Label(self, text="Camera Endpoint URL:")
        url_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_url = tk.Entry(self, width=50)
        self.entry_url.grid(row=3, column=1, padx=10, pady=10)

        # Buttons (Add + Check)
        add_button = tk.Button(self, text="Add Camera", width=20, command=self.add_camera)
        add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        list_button = tk.Button(self, text="Check the Camera List", width=20, command=self.switch_to_frame2)
        list_button.grid(row=4, column=1, padx=10, pady=10)

    def add_camera(self):
        """Add a camera to the camera list."""
        folder_path = self.entry_path.get()
        detection_freq = self.entry_freq.get()
        camera_url = self.entry_url.get()
        def is_valid_url(url):
            return re.match(r'^https?://[^\s]+$', url) != None

        if not folder_path or not detection_freq or not camera_url:
            messagebox.showerror("Input Error", "Please complete all fields.")
            return

        if not is_valid_url(camera_url):
            messagebox.showerror("Validation Error", "Please enter a valid Camera URL (starting with http:// or https://)")
            return
       
        camera = {
            'path': folder_path,
            'frequency': detection_freq,
            'url': camera_url
        }
        camera_list.append(camera)  # Add camera to the global list
        frame1_list.append(self)    # Add camera to the frame1 list for later reference
        messagebox.showinfo("Camera Added", "Camera configuration has been successfully added.")
        self.run_powershell(folder_path, detection_freq, camera_url)   # Run PowerShell script with the provided parameters
        self.switch_to_frame2()

    def run_powershell(self, folder_path, detection_freq, camera_url):
        try:
            subprocess.run([
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", "capture_and_detect.ps1",
                "-FolderPath", folder_path,
                "-Frequency", detection_freq,
                "-CameraURL", camera_url
            ], check=True)
            print("PowerShell script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error running PowerShell script:", e)


class Frame2(tk.Frame):
    """Frame2: for displaying the list of cameras and allowing users to edit or remove them."""
    def __init__(self, parent, switch_to_frame1, add_new_frame1):
        super().__init__(parent)
        self.switch_to_frame1 = switch_to_frame1
        self.add_new_frame1 = add_new_frame1 
        self.create_widgets()
        
    def create_widgets(self):
        self.table = ttk.Treeview(self, columns=("Path", "Freq", "URL"), show="headings", selectmode='browse')
        for col in ("Path", "Freq", "URL"):
            self.table.heading(col, text=col)
            self.table.column(col, width=180)
        self.table.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        tk.Button(self, text="Edit Selected", command=self.edit_camera).grid(row=1, column=0, pady=10)
        tk.Button(self, text="Remove Selected", command=self.remove_camera).grid(row=1, column=1, pady=10)
        tk.Button(self, text="Back to Add", command=self.switch_to_frame1).grid(row=1, column=2, pady=10)
        tk.Button(self, text="Add a New Camera", command=self.add_new_frame1).grid(row=1, column=3, pady=10)

        self.update_camera_list()
        
    def update_camera_list(self):
        self.table.delete(*self.table.get_children())
        for cam in camera_list:
            self.table.insert("", "end", values=(cam['path'], cam['frequency'], cam['url']))

    def edit_camera(self):
        selected = self.table.selection()
        index = self.table.index(selected[0])
        camera_list.pop(index)
        frame1_list.pop(index)
        self.update_camera_list()
        self.switch_to_frame1()

    def confirm_camera(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select Camera", "Please select a camera to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this camera?")
        if confirm:
            self.remove_camera()

    def remove_camera(self):
        selected = self.table.selection()
        index = self.table.index(selected[0])
        camera_list.pop(index)
        frame1_list.pop(index)
        self.update_camera_list()

class Frame3(tk.Frame):
    """Frame3: ReadMe Page -- what's LConnect?"""
    """This frame provides additional information about the LConnect application."""
    def __init__(self, parent, switch_to_frame1, switch_to_frame2):
        super().__init__(parent)
        self.switch_to_frame1 = switch_to_frame1
        self.switch_to_frame2 = switch_to_frame2
        self.create_widgets()

    def create_widgets(self):
        welcome_label = tk.Label(self, text="Welcome to LConnect! This system helps monitor wildfire risks using the camera settings you provide.\n\n"
                                        "Please enter your camera information below.", justify="left", font=("Times", 20, "bold"), wraplength=700)
        welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 10))

        tk.Button(self, text="Start to Camera Settings", width=20, command=self.switch_to_frame1).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        tk.Button(self, text="Check the Camera List", width=20, command=self.switch_to_frame2).grid(row=1, column=1,padx=10, pady=10, sticky='w')

        self.readme_visible = False
        self.readme_button = tk.Button(self, text="What is LConnect? ▼", width=20, command=self.toggle_readme)
        self.readme_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.readme_detail = tk.Label(self, text=(
            "LConnect automates retrieval of images from multiple FTP folders,\n"
            "submits them to a wildfire-detection API, records API responses, and saves positively flagged images.\n"
            "It provides a simple graphical interface for mapping FTP folders to API endpoints."
        ), justify="left", wraplength=700, bg="lightgrey", font=("Arial", 18, "italic"))
        self.readme_detail.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.readme_detail.grid_remove()

    def toggle_readme(self):
        if self.readme_visible:
            self.readme_detail.grid_remove()
            self.readme_button.config(text="What is LConnect? ▼")
            self.readme_visible = False
        else:
            self.readme_detail.grid()
            self.readme_button.config(text="Hide Details ▲")
            self.readme_visible = True

        
class LConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LConnect Camera Configurator")
        self.root.geometry("800x600")

        self.frame1 = None
        self.frame2 = None
        self.frame3 = None

        self.frame1 = Frame1(root, self.show_frame2, self.show_frame3)
        self.frame2 = Frame2(root, self.show_frame1, self.add_new_frame1)
        self.frame3 = Frame3(root, self.show_frame1, self.show_frame2)

        for frame in (self.frame1, self.frame2, self.frame3):
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame3()

    def show_frame1(self):
        self.frame2.update_camera_list()
        self.frame1.tkraise()

    def show_frame2(self):
        self.frame2.update_camera_list()
        self.frame2.tkraise()

    def show_frame3(self):
        self.frame2.update_camera_list()
        self.frame3.tkraise()

    def add_new_frame1(self):
        if self.frame1:
            self.frame1.destroy()
        self.frame1 = Frame1(self.root, self.show_frame2)
        self.frame1.grid(row=0, column=0, sticky='nsew')
        self.frame1.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = LConnectApp(root)
    root.mainloop()