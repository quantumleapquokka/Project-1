
# PowerShell Script — `capture_and_detect.ps1`

This script handles image capture from a camera feed and posts it to a fire detection API. It is invoked by the Python GUI and runs headlessly.

---

##  Script Parameters

```powershell
param (
    [int]$Iteration = 3,
    [int]$WaitTime = 30,
    [switch]$ListResults,
    [string]$Frequency,
    [string]$CameraURL,
    [string]$FolderPath
)
```

- `Iteration`: Number of detection attempts (default: 3)
- `WaitTime`: Delay between each attempt (default: 30s)
- `ListResults`: Optional flag to print details to console
- `CameraURL`: Direct URL to fetch camera snapshot
- `FolderPath`: Where to store image/output files
- `Frequency`: Passed by GUI for logging purposes only

---

##  Configuration

```powershell
$username = "root"
$password = "Cashflow108!"  # Replace for production use
$outputFile = Join-Path $FolderPath "capture.jpg"
$responsePath = Join-Path $FolderPath "last-response.json"
$resultsFile = Join-Path $FolderPath "results.txt"
```

---

## Main Workflow

For each iteration:
1. Downloads a snapshot from the camera URL
2. Sends it to the fire detection API via `Invoke-RestMethod`
3. Saves API response to `.json`
4. Logs output and status to `results.txt`

---

## Output Example

- `capture.jpg`: Current frame
- `results.txt`: Summary and logs for each attempt
- `last-response.json`: Raw API response

---

## Troubleshooting

- ❌ **Image capture failed**: Check camera URL or credentials
- ❌ **401 Unauthorized**: Credentials incorrect or camera needs login
- ❌ **Folder not found**: FolderPath must exist beforehand

> PowerShell 5.1 does not support `-AllowUnencryptedAuthentication`, so this parameter has been removed.

---

## Note

Credentials are hardcoded for now. Future improvements should securely prompt for them or use environment variables.
