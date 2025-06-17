
# Troubleshooting Guide — LConnect Camera Tool

This guide covers common problems and how to fix them when using the LConnect Camera Tool.

---

## General Checklist

Before troubleshooting individual issues, confirm:

- You are using Python 3.8 or later.
- PowerShell is installed and accessible on your system.
- You have not renamed or moved `capture_and_detect.ps1` or `doneGUI.py`.
- The output folder you specify in the GUI **exists** and is writable.
- Your internet connection is active (for API calls).

---

## Errors and Solutions

### Problem: PowerShell script fails with "Image capture failed on iteration 1"

**Cause:** The image could not be fetched from the camera URL.

**Fix:**
- Ensure the URL entered is a valid snapshot URL that ends in `.jpg` or returns a JPEG image.
- Confirm the camera is online and accessible from your network.
- Check if login credentials are required and valid.
- Try running the PowerShell command manually using the printed output from the debug GUI.

---

### Problem: "Unauthorized" error in PowerShell output

**Cause:** The camera requires authentication and the provided credentials are incorrect.

**Fix:**
- Update the username and password in the PowerShell script to valid credentials.
- Test the URL in a browser and enter the same credentials when prompted to confirm access.

---

### Problem: PowerShell error: "A parameter cannot be found that matches parameter name 'AllowUnencryptedAuthentication'"

**Cause:** This parameter is not supported in PowerShell 5.1 or earlier.

**Fix:**
- Remove `-AllowUnencryptedAuthentication` from the script.
- This parameter is not necessary unless your camera requires unsecured HTTP authentication (which most don’t).

---

### Problem: Folder not found or permission denied

**Cause:** The folder specified in the GUI does not exist or cannot be written to.

**Fix:**
- Create the folder manually before entering the path.
- Make sure you are not using restricted locations like `C:\Program Files` or root directories without admin rights.

---

### Problem: Script runs manually but not from GUI

**Cause:** Parameters may not be quoted properly in the subprocess call.

**Fix:**
- Ensure the Python script wraps each parameter in double quotes.
- Use the debug version (`doneGUI_debug.py`) to print the full PowerShell command and test it manually.

---

### Problem: No output files appear

**Cause:** The script may have failed silently or written to the wrong folder.

**Fix:**
- Check the terminal for errors.
- Verify the correct folder was used and that no typos were introduced.
- Make sure you are not overwriting previous outputs or writing to an unexpected location.

---

## Contact

If you're still experiencing issues, consult the script logs (`results.txt`) or enable additional debug printouts in the GUI and PowerShell script.
