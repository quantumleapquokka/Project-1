## FAQ

### How do I add a new camera?
Go to the "Start to Camera Settings" page, fill in the required fields (name, path, frequency, and URL), then click **Add Camera**.

### What kind of URL should I use?
Use a direct image endpoint (e.g., a snapshot URL from your IP camera) starting with `http://` or `https://`.

### How often can images be captured?
You can choose from preset intervals: 30s, 60s, or 120s. These determine how frequently the system captures and analyzes images.

### Where are the results stored?
All detection logs, responses, and images are saved in the local folder you specify during setup (under `results.txt` and `capture.jpg`).

### Why am I seeing "file is being used by another process"?
This error occurs if the PowerShell script tries to access the image file while another process (like the GUI or an antivirus scan) is using it. Try increasing the interval or ensuring no external apps are interfering.

### Can I stop a running scan?
Yes. Click **Stop Monitoring** in the Camera Settings screen to terminate the PowerShell process.

### How can I view progress?
Click **View Progress** to see detection logs, timestamps, and how many images have been processed per camera.
