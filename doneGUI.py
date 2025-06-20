import tkinter as tk
import os
import re
import webbrowser
from tkinter import ttk, messagebox
import subprocess
from datetime import datetime
camera_list = []
frame1_list = []
ps_processes = []

"""
This is the GUI part for LookOut System Connection
It allows users to input camera settings and manage the camera list

It consists of two frames --
Frame1: For adding cameras, entering camera settings and validating inputs to the widgets
Frame2: For displaying the list of added cameras and allowing users to remove or to edit them
Frame3: For introducing the LookOut System, home page
Frame4: For displaying the progress of the camera monitoring
"""
class Frame1(tk.Frame):
    """Frame1: for adding camera settings and managing the camera list."""
    def __init__(self, parent, switch_to_frame2, switch_to_frame3, camera_to_edit=None, edit_index=None):
        super().__init__(parent)   
        self.switch_to_frame2 = switch_to_frame2   
        self.switch_to_frame3 = switch_to_frame3  
        self.camera_to_edit = camera_to_edit
        self.edit_index = edit_index
        self.ps_process = None
        self.create_widgets()  

    def create_widgets(self):
        """Create and layout widgets for Frame1."""
        #Camera Name
        name_label = tk.Label(self, text="Camera Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_name = tk.Entry(self, width=50)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        if self.camera_to_edit:
            self.entry_name.insert(0, self.camera_to_edit['name'])
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

        # Buttons (Add + Check + Stop)
        add_button = tk.Button(self, text="Add Camera", width=20, command=self.add_camera)
        add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        list_button = tk.Button(self, text="Check the Camera List", width=20, command=self.switch_to_frame2)
        list_button.grid(row=4, column=1, padx=10, pady=10)
        home_button = tk.Button(self, text="↩ Back Home", width=20, command=self.switch_to_frame3)
        home_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='w')

    def add_camera(self):
        """Add a camera to the camera list."""
        camera_name = self.entry_name.get()
        folder_path = self.entry_path.get()
        detection_freq = self.entry_freq.get()
        camera_url = self.entry_url.get()
        def is_valid_url(url):
            return re.match(r'^https?://[^\s]+$', url) != None

        if not camera_name or not folder_path or not detection_freq or not camera_url:
            messagebox.showerror("Input Error", "Please complete all fields.")
            return

        if not is_valid_url(camera_url):
            messagebox.showerror("Validation Error", "Please enter a valid Camera URL (starting with http:// or https://)")
            return
       
        camera = {
            'name': camera_name,
            'path': folder_path,
            'frequency': detection_freq,
            'url': camera_url
        }
        if self.edit_index is not None:
            camera_list[self.edit_index] = camera  # Update existing camera
            frame1_list[self.edit_index] = self
        else:
            camera_list.append(camera)  # Add new camera
            frame1_list.append(self)    # Add camera to the frame1 list for later reference
        messagebox.showinfo("Camera Added", "Camera configuration has been successfully added.")
        self.switch_to_frame2()
        self.run_powershell(folder_path, detection_freq, camera_url)   # Run PowerShell script with the provided parameters
        

    def run_powershell(self, folder_path, detection_freq, camera_url):
        try:
            self.ps_process = subprocess.Popen([
                "pwsh.exe",  # or "powershell.exe" if using legacy version
                "-ExecutionPolicy", "Bypass",
                "-File", "capture_and_detect.ps1",
                "-FolderPath", folder_path,
                "-Frequency", detection_freq,
                "-ApiURL", camera_url
            ])
            ps_processes.append(self.ps_process)
            print("PowerShell script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error running PowerShell script:", e)

class Frame2(tk.Frame):
    """Frame2: for displaying the list of cameras and allowing users to edit or remove them."""
    def __init__(self, parent, switch_to_frame1, switch_to_frame3, switch_to_frame4, add_new_frame1):
        super().__init__(parent)
        self.switch_to_frame1 = switch_to_frame1
        self.switch_to_frame3 = switch_to_frame3
        self.add_new_frame1 = add_new_frame1
        self.switch_to_frame4 = switch_to_frame4
        self.ps_process = None
        self.create_widgets()

    def create_widgets(self):
        """create the table"""
        # set the table
        self.table = ttk.Treeview(self, columns=("Name", "Path", "Freq", "URL"), show="headings", selectmode='browse')
        for col in ("Name", "Path", "Freq", "URL"):
            self.table.heading(col, text=col)
            self.table.column(col, width=180)
        self.table.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # set the buttons
        tk.Button(self, text="Edit Selected", command=self.edit_camera).grid(row=1, column=0, pady=10)
        tk.Button(self, text="Remove Selected", command=self.remove_camera).grid(row=1, column=1, pady=10)
        tk.Button(self, text="Back to Add", command=self.switch_to_frame1).grid(row=1, column=2, pady=10)
        tk.Button(self, text="Add a New Camera", command=self.add_new_frame1).grid(row=1, column=3, pady=10)
        tk.Button(self, text="↩ Back Home", command=self.switch_to_frame3).grid(row=2, column=0, pady=10)
        tk.Button(self, text="View Progress", command=self.switch_to_frame4).grid(row=2, column=1, pady=10)
        tk.Button(self, text="Stop Monitoring 🛑", width=20, command=self.stop_powershell).grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky='w')

        self.update_camera_list()

    def stop_powershell(self):
        """Stop all PowerShell monitoring processes."""
        global ps_processes
        any_stopped = False
        for p in ps_processes:
            if p.poll() is None:
                p.terminate()
                any_stopped = True
                print("PowerShell script terminated.")
        if not any_stopped:
            messagebox.showinfo("No Active Script", "No active monitoring process to stop.")

    def update_camera_list(self):
        """Update the camera list in the table."""
        self.table.delete(*self.table.get_children())
        for cam in camera_list:
            self.table.insert("", "end", values=(cam['name'], cam['path'], cam['frequency'], cam['url']))

    def edit_camera(self):
       """Edit the selected camera."""
       selected = self.table.selection()
       if not selected:
        messagebox.showwarning("No Selection", "Please select a camera to edit.")
        return
       index = self.table.index(selected[0])
       camera = camera_list[index]
       self.add_new_frame1(camera, index)

    def remove_camera(self):
        """Remove the selected camera."""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select Camera", "Please select a camera to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this camera?")
        if not confirm:
            return
        index = self.table.index(selected[0])
        camera_list.pop(index)
        frame1_list.pop(index)
        self.update_camera_list()

class Frame3(tk.Frame):
    """Frame3: ReadMe Page -- what's LConnect?"""
    """This frame provides additional information about the LConnect application."""
    def __init__(self, parent, switch_to_frame1, switch_to_frame2, switch_to_frame4):
        super().__init__(parent)
        self.switch_to_frame1 = switch_to_frame1 
        self.switch_to_frame2 = switch_to_frame2
        self.switch_to_frame4 = switch_to_frame4
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets for Frame3."""
        # Welcome label
        welcome_label = tk.Label(self, text="Welcome to LConnect! This system helps monitor wildfire risks using the camera settings you provide.\n\n"
                                        "Please enter your camera information below.", justify="left", font=("Arial", 20, "bold"), wraplength=700)
        welcome_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Buttons to switch frames
        tk.Button(self, text="Start to Camera Settings ➕", command=self.switch_to_frame1).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self, text="Check the Camera List 📋", command=self.switch_to_frame2).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="View Progress 👁", command=self.switch_to_frame4).grid(row=1, column=2, padx=10, pady=10)

        # ReadMe to show what is LConnect
        self.readme_visible = False
        self.readme_button = tk.Button(self, text="What is LConnect? ▼", command=self.toggle_readme)
        self.readme_button.grid(row=2, column=1, padx=10, pady=10)
        
        self.readme_detail = tk.Label(self, text=(
            "LConnect automates retrieval of images from multiple FTP folders,\n"
            "submits them to a wildfire-detection API, records API responses, and saves positively flagged images.\n"
            "It provides a simple graphical interface for mapping FTP folders to API endpoints.\n"
            "For more information, please visit our website."
        ), justify="left", wraplength=700, font=("Arial", 14, "italic"), fg="grey")
        self.readme_detail.grid(row=3, column=0, columnspan=3, padx=50, pady=10)
        self.readme_link = tk.Label(self, text="check the website for more information", bg="lightgrey", font=("Arial", 16))
        self.readme_link.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.readme_link.bind("<Button-1>", lambda e: webbrowser.open("https://roboticscats.com/lookout/"))
        self.readme_link.config(fg="blue", cursor="hand2")
        self.readme_link.config(fg="blue", cursor="hand2")

        self.readme_detail.grid_remove()  #remove the readme at the begining
        self.readme_link.grid_remove()

    def toggle_readme(self):
        """Toggle the visibility of the ReadMe section."""
        if self.readme_visible:
            self.readme_detail.grid_remove()
            self.readme_link.grid_remove()
            self.readme_button.config(text="What is LConnect? ▼")
            self.readme_visible = False
        else:
            self.readme_detail.grid()
            self.readme_link.grid()
            self.readme_button.config(text="Hide Details ▲")
            self.readme_visible = True

class Frame4(tk.Frame):
    """Frame4: Progress monitor checking cameras information and images sent in 2 minutes"""
    def __init__(self, parent, switch_to_frame3):
        super().__init__(parent)
        self.switch_to_frame3 = switch_to_frame3
        self.update_interval_seconds = 120
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout widgets for Frame4."""
        # Title and description
        title = tk.Label(self, text="LConnect Progress Monitor", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        description = tk.Label(self, text="This section shows the progress of the LConnect system.\n"
                                        "It displays the cameras you have configured, the last time they were detected,\n"
                                        "when they were created, and how many images have been sent to the LookOut system.\n"
                                        "You can monitor the status of each camera and ensure that they are functioning correctly.",
                                        justify="left", font=("Arial", 14), wraplength=700)
        description.pack(pady=20)

        # Treeview to display camera progress   
        # Camera name, endTime, startTime, imagesSent
        self.tree = ttk.Treeview(self, columns=("Camera", "Last Detected", "Created on", "Images Sent"), show="headings")
        self.tree.heading("Camera", text="Camera")
        self.tree.heading("Last Detected", text="Last Detected")
        self.tree.heading("Created on", text="Created on")
        self.tree.heading("Images Sent", text="Images Sent")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)
        self.update_camera_list()
        # Back to home button
        back_button = tk.Button(self, text="↩ Back Home", command=self.switch_to_frame3)
        back_button.pack(pady=10)

    def update_camera_list(self):
        self.tree.delete(*self.tree.get_children())
        for cam in camera_list:
            results_path = os.path.join(cam["path"], "results.txt")
            last_detected = "-"
            created_on = "-"
            images_sent = 0

            if os.path.exists(results_path):
                try:
                    with open(results_path, "r") as f:
                        lines = f.readlines()
                        created_on = lines[0].strip() if lines else "-"
                        for line in lines:
                            match = re.match(r"\[(.*?)\]", line)
                            if match:
                                last_detected = match.group(1)
                            if "Fire Detection FOUND!" in line or "No detection." in line:
                                images_sent += 1
                except Exception as e:
                    print(f"Failed to read {results_path}: {e}")

            cam["last_detected"] = last_detected
            cam["created_on"] = created_on
            cam["images_sent"] = images_sent

            self.tree.insert("", "end", values=(cam["name"], last_detected, created_on, images_sent))
        self.after(5000, self.update_camera_list)  # Update every 5 seconds


class LConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LConnect Camera Configurator")
        self.root.geometry("800x600")

        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.frame4 = None

        self.frame1 = Frame1(root, self.show_frame2, self.show_frame3)
        self.frame2 = Frame2(root, self.show_frame1, self.show_frame3, self.show_frame4, self.add_new_frame1)
        self.frame3 = Frame3(root, self.show_frame1, self.show_frame2, self.show_frame4)
        self.frame4 = Frame4(root, self.show_frame3)

        for frame in (self.frame1, self.frame2, self.frame3, self.frame4):
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame3()

        self.root.protocol("WM_DELETE_WINDOW", self.cleanup) # terminate on window close

    def show_frame1(self):
        if self.frame2 is not None:
            self.frame2.update_camera_list()
        if self.frame1 is not None:
            self.frame1.tkraise()

    def show_frame2(self):
        if self.frame2 is not None:
            self.frame2.update_camera_list()
            self.frame2.tkraise()

    def show_frame3(self):
        if self.frame2 is not None:
            self.frame2.update_camera_list()
        if self.frame3 is not None:
            self.frame3.tkraise()
    
    def show_frame4(self):
        if self.frame2 is not None:
            self.frame2.update_camera_list()
        if self.frame4 is not None:
            self.frame4.tkraise()
    
    def add_new_frame1(self, camera=None, index=None):
        if self.frame1:
            self.frame1.destroy()
        self.frame1 = Frame1(self.root, self.show_frame2, self.show_frame3, camera, index)
        self.frame1.grid(row=0, column=0, sticky='nsew')
        self.frame1.tkraise()

    def cleanup(self):
        global ps_processes
        for p in ps_processes:
            if p and p.poll() is None:
                try:
                    p.terminate()
                    print("PowerShell script terminated on close.")
                except Exception as e:
                    print("Error terminating PowerShell process:", e)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LConnectApp(root)
    root.mainloop()