# LConnect 
A GUI-based Python applicatoon that allowes users to configure and manage cameras for Lookout by RoboticsCats

## Features
- Add and manaage camera configurations
- Capture snapshots from network camera feeds
- Automatically send snapshots to Lookout fire detetcion api
- Log resultys and API responses to a user-specified folder
- Tkinter based gui for easy use and real-time feedback.

## Requirements
- Python 3.8+
- Windows Powershell 5.1 or later
- Required Python Modules:
    - `tkinter`
    - `subprocess`
    - `threading`
- Internet connnection
## Getting Started 
### Clone or download this repo
```bash
git clone https://github.com/your-username/lconnect-camera-tool.git
cd lconnect-camera-tool
```
### Run the GUI
```bash
python doneGUI.py
```
### 3. Fill out the fields
- Folder Path: Where results and images should be saved
- Frequency: How often to poll the camera
- Camera Endpoint URL: A direct snapshot URL
## Documemtation
>Visit the [docs](https://link-url-here.org) folder in this repo to read further documentation for the project.