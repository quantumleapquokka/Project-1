import tkinter as tk
from tkinter import ttk

camera_list = []
frame1_list = []

class Frame1(tk.Frame):
    def __init__(self, parent, switch_to_frame2):
        super().__init__(parent)
        self.switch_to_frame2 = switch_to_frame2
        self.create_widgets()

    def create_widgets(self):
        path_label = tk.Label(self, text="Folder Path:")
        path_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_path = tk.Entry(self, width=40)
        self.entry_path.grid(row=0, column=1)

        freq_label = tk.Label(self, text="Detection Frequency:")
        freq_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_freq = ttk.Combobox(self, values=["30s", "60s", "120s"], state="readonly")
        self.entry_freq.current(0)
        self.entry_freq.grid(row=1, column=1)

        url_label = tk.Label(self, text="Camera Endpoint URL:")
        url_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_url = tk.Entry(self, width=40)
        self.entry_url.grid(row=2, column=1)

        add_button = tk.Button(self, text="Add Camera", command=self.add_camera)
        add_button.grid(row=3, column=0, pady=20)
        list_botton = tk.Button(self, text="Check the Camera List", command=self.switch_to_frame2)
        list_botton.grid(row=3, column=1, pady=20)

    def add_camera(self):
        """Add a camera to the camera list."""
        folder_path = self.entry_path.get()
        detection_freq = self.entry_freq.get()
        camera_url = self.entry_url.get()
        if folder_path and detection_freq and camera_url:
            camera = {
                'path': folder_path,
                'frequency': detection_freq,
                'url': camera_url
            }
            camera_list.append(camera)
            frame1_list.append(self)
            print("Camera added:", camera)
            self.switch_to_frame2
        else:
            print("Please complete all fields")

    def check_camera(self):
        """Check the camera configuration."""
        folder_path = self.entry_path.get()
        detection_freq = self.entry_freq.get()
        camera_url = self.entry_url.get()
        if folder_path and detection_freq and camera_url:
            print("Camera configuration is valid.")
        else:
            print("Please complete all fields.")

class Frame2(tk.Frame):
    def __init__(self, parent, switch_to_frame1):
        super().__init__(parent)
        self.switch_to_frame1 = switch_to_frame1
        self.switch_to_frame1 = switch_to_frame1
        self.create_widgets()
        
    def create_widgets(self):
        self.table = ttk.Treeview(self, columns=("Path", "Freq", "URL"), show="headings", selectmode='browse')
        for col in ("Path", "Freq", "URL"):
            self.table.heading(col, text=col)
            self.table.column(col, width=180)
        self.table.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self, text="Edit Selected", command=self.edit_camera).grid(row=1, column=0, pady=10)
        tk.Button(self, text="Remove Selected", command=self.remove_camera).grid(row=1, column=1, pady=10)
        tk.Button(self, text="Back to Add", command=self.switch_to_frame1).grid(row=1, column=2, pady=10)

        self.update_camera_list()
        
    def update_camera_list(self):
        self.table.delete(*self.table.get_children())
        for cam in camera_list:
            self.table.insert("", "end", values=(cam['path'], cam['frequency'], cam['url']))

    def edit_camera(self):
        selected = self.table.selection()
        if not selected:
            print("No camera selected.")
            return
        index = self.table.index(selected[0])
        camera_list.pop(index)
        frame1_list.pop(index)
        self.update_camera_list()
        self.switch_to_frame1()

    def remove_camera(self):
        selected = self.table.selection()
        if not selected:
            print("No camera selected.")
            return
        index = self.table.index(selected[0])
        camera_list.pop(index)
        frame1_list.pop(index)
        self.update_camera_list()

class LConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LConnect Camera Configurator")
        self.root.geometry("700x500")

        self.frame1 = Frame1(root, self.show_frame2)
        self.frame2 = Frame2(root, self.show_frame1)

        for frame in (self.frame1, self.frame2):
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame1()

    def show_frame1(self):
        self.frame1.tkraise()
        self.frame2.update_camera_list()

    def show_frame2(self):
        self.frame2.update_camera_list()
        self.frame2.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = LConnectApp(root)
    root.mainloop()
