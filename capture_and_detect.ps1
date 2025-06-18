# Define Script Parameters
param (
    [ValidateRange(1, 1440)][int]$Iteration = 3,
    [ValidateRange(15, 300)][int]$WaitTime = 30,
    [switch]$ListResults,
    [string]$Frequency,
    [string]$ApiURL,
    [string]$FolderPath
)

Write-Host "Running detection on $ApiURL every $Frequency seconds..."
Write-Host "Saving output to $FolderPath"

# --- Configuration ---
$username = "root"
$password = "Cashflow108!"
$cameraUrl = "http://demo.customer.roboticscats.com:55758/axis-cgi/jpg/image.cgi?resolution=1920x1080"
$outputFile = Join-Path $FolderPath "capture.jpg"
$responsePath = Join-Path $FolderPath "last-response.json"
$resultsFile = Join-Path $FolderPath "results.txt"
$apiUrl = $ApiURL # "https://lax.pop.roboticscats.com/api/detects?apiKey=6b4b4551f987d18b70ca53c1975c4fd3"

# --- Initialize ---
$startTime = Get-Date
Set-Content -Path $resultsFile -Value "LookOut Connect Results"
Add-Content -Path $resultsFile -Value "-----------------------"
$captureTimes = @()
$successTime = 0

# --- Main Loop ---
$i = 1
while ($true) {
    $captureSnapshot = $true
    $getStartTime = Get-Date

    try {
        Invoke-WebRequest -Uri $cameraUrl `
            -Credential (New-Object System.Management.Automation.PSCredential($username, (ConvertTo-SecureString $password -AsPlainText -Force))) `
            -OutFile $outputFile `
            -AllowUnencryptedAuthentication # IF USING EARLIER VERSION OF POWERSHELL (i.e. 5.1) IT WILL NOT WORK
    }
    catch {
        $captureSnapshot = $false
        Write-Error "Image capture failed on iteration $i"
        Write-Host "Exception Type: $($_.Exception.GetType().FullName)"
        Write-Host "Message: $($_.Exception.Message)"
        Write-Host "Stack Trace: $($_.Exception.StackTrace)"
        continue
    }

    $getEndTime = Get-Date
    $postStartTime = Get-Date

    if ($captureSnapshot) {
        try {
            $response = Invoke-RestMethod -Uri $apiUrl -Method Post -InFile $outputFile -ContentType "image/jpeg"
            # Save API response to file for inspection
            $response | ConvertTo-Json -Depth 10 | Set-Content -Path $responsePath

            # Also optionally print to console
            Write-Host "Raw API Response:"
            $response | ConvertTo-Json -Depth 10
            $postSuccess = $true
            $successTime++
        }
        catch {
            $postSuccess = $false
            Add-Content -Path $resultsFile -Value "[$(Get-Date)] Iteration ${i}: API call failed. Exception: $($_.Exception.Message)"
        }
    } else {
        $postSuccess = $false
    }

    # check for bounding box in response
    if ($postSuccess -and ($response | Out-String | Select-String -Pattern 'score' -Quiet)) {
        Add-Content -Path $resultsFile -Value "[$(Get-Date)] Iteration ${i}: Fire Detection FOUND!"

        # Create 'positives' subfolder if it doesn't exist
        $positivesFolder = Join-Path $FolderPath "positives"
        if (!(Test-Path $positivesFolder)) {
            New-Item -ItemType Directory -Path $positivesFolder | Out-Null
        }

        # Copy image to 'positives' folder with a timestamped name
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $positiveImage = Join-Path $positivesFolder "positive_$timestamp.jpg"
        Copy-Item -Path $outputFile -Destination $positiveImage

    } elseif ($postSuccess) {
        Add-Content -Path $resultsFile -Value "[$(Get-Date)] Iteration ${i}: No detection."
    }

    $postEndTime = Get-Date
    $getElapsedTime = ($getEndTime - $getStartTime).TotalMilliseconds
    $postElapsedTime = ($postEndTime - $postStartTime).TotalMilliseconds
    $captureTimes += $postElapsedTime

    $postElapsedTimeSecond = [math]::Round($postElapsedTime / 1000, 2)
    $sleepTime = [math]::Round(($WaitTime - $getElapsedTime / 1000 - $postElapsedTime / 1000), 2)
    if ($sleepTime -lt 0) { $sleepTime = 0 }

    if ($ListResults) {
        $msg = "$(Get-Date) Iteration $i : Success=$postSuccess, Elapsed=${postElapsedTimeSecond}s, Sleeping ${sleepTime}s"
        Write-Host $msg
        Add-Content -Path $resultsFile -Value $msg
    }

    Start-Sleep -Seconds $sleepTime
    $i++
}

# --- Final Stats ---
$averageTime = [math]::Round((($captureTimes | Measure-Object -Average).Average / 1000), 2)
$maxTime = [math]::Round((($captureTimes | Measure-Object -Maximum).Maximum / 1000), 2)
$minTime = [math]::Round((($captureTimes | Measure-Object -Minimum).Minimum / 1000), 2)
$endTime = Get-Date

$summary = @"
Summary:
---------
Start: $startTime
End: $endTime
Iterations: $i
Successes: $successTime
Interval (s): $WaitTime

Processing Times (s):
- Avg: $averageTime
- Max: $maxTime
- Min: $minTime
"@
Add-Content -Path $resultsFile -Value $summary
Write-Host $summary
