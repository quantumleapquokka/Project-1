
# Usage Guide — LConnect Camera Tool

This guide walks you through using the LConnect Camera Tool to configure cameras, capture snapshots, and perform fire detection via an API.

---

## Launching the Application

Ensure Python and PowerShell are installed. Then run:

```bash
python doneGUI.py
```

> Alternatively, run `doneGUI_debug.py` for extra debug output.

---

## Input Fields

### Folder Path
- The local directory where logs, image captures, and API responses will be saved.
- Must **already exist** and be writable.
- Example: `C:\Users\YourName\Documents\CameraRun`

### Detection Frequency
- How often the backend will run image capture + detection per camera.
- Options: `30s`, `60s`, or `120s`.

### Camera Endpoint URL
- The direct image snapshot URL from your camera.
- Must return a **JPEG image** on request.
- Example:
  ```
  http://demo.customer.roboticscats.com:55758/axis-cgi/jpg/image.cgi?resolution=1920x1080
  ```

---

##  Adding a Camera

1. Fill out all fields.
2. Click **"Add Camera"** — this will:
   - Add it to the session list.
   - Call the PowerShell script (`capture_and_detect.ps1`) with the provided values.
   - Capture and analyze an image.

---

##  Viewing Camera List

Click **"Check the Camera List"** to:
- See added cameras
- Edit or remove a selected camera
- Return to the add form

---

##  Stopping the Script

There is no built-in stop/pause functionality yet. You can manually kill the PowerShell process if needed.

---

## Output Files

Each run generates the following in the selected folder:
- `capture.jpg` — latest snapshot from the camera
- `last-response.json` — API response
- `results.txt` — detailed iteration log
