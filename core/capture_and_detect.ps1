# Define Script Parameters
param (
    [ValidateRange(1, 1440)][int]$Iteration = 3,
    [ValidateRange(15, 300)][int]$WaitTime = 30,
    [switch]$ListResults,
    [string]$Frequency,
    [string]$CameraURL,
    [string]$FolderPath
)

Write-Host "Running detection on $CameraURL every $Frequency seconds..."
Write-Host "Saving output to $FolderPath"

# --- Configuration ---
$username = "root"
$password = "Cashflow108!"
$cameraUrl = $CameraURL
$outputFile = Join-Path $FolderPath "capture.jpg"
$responsePath = Join-Path $FolderPath "last-response.json"
$resultsFile = Join-Path $FolderPath "results.txt"
$apiUrl = "https://lax.pop.roboticscats.com/api/detects?apiKey=6b4b4551f987d18b70ca53c1975c4fd3"

# --- Initialize ---
$startTime = Get-Date
Set-Content -Path $resultsFile -Value "LookOut Connect Results"
Add-Content -Path $resultsFile -Value "-----------------------"
$captureTimes = @()
$successTime = 0

# --- Main Loop ---
for ($i = 1; $i -le $Iteration; $i++) {
    $captureSnapshot = $true
    $getStartTime = Get-Date

    try {
        Invoke-WebRequest -Uri $cameraUrl `
            -Credential (New-Object System.Management.Automation.PSCredential($username, (ConvertTo-SecureString $password -AsPlainText -Force))) `
            -OutFile $outputFile `
            -AllowUnencryptedAuthentication
    }
    catch {
        $captureSnapshot = $false
        Write-Error "Image capture failed on iteration $i"
        Add-Content -Path $resultsFile -Value "[$(Get-Date)] Iteration ${i}: Image capture failed. Exception: $($_.Exception.Message)"
        continue
    }

    $getEndTime = Get-Date
    $postStartTime = Get-Date

    if ($captureSnapshot) {
        try {
            $response = Invoke-RestMethod -Uri $apiUrl -Method Post -InFile $outputFile -ContentType "image/jpeg"
            # Optional: Save API response to file for inspection
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

    # Optional: check for bounding box in response
    if ($postSuccess -and ($response | Out-String | Select-String -Pattern 'score' -Quiet)) {
        Add-Content -Path $resultsFile -Value "[$(Get-Date)] Iteration ${i}: Fire Detection FOUND!"
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
Iterations: $Iteration
Successes: $successTime
Interval (s): $WaitTime

Processing Times (s):
- Avg: $averageTime
- Max: $maxTime
- Min: $minTime
"@
Add-Content -Path $resultsFile -Value $summary
Write-Host $summary
