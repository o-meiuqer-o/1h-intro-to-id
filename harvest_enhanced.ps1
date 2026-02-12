$csvPath = "D:\history of id course\expanded_designers.csv"
$imagesDir = "D:\history of id course\images"
$logFile = "D:\history of id course\harvest_log_enhanced.txt"
$progressFile = "D:\history of id course\harvest_progress.json"

# Rate limiting parameters
$baseDelay = 2  # Start with 2 seconds
$maxDelay = 30  # Max 30 seconds
$batchSize = 5  # Process 5 designers at a time
$imagesPerDesigner = 12

# Load progress if exists
$progress = @{}
if (Test-Path $progressFile) {
    $progress = Get-Content $progressFile | ConvertFrom-Json -AsHashtable
    Write-Host "Loaded progress: $($progress.Count) designers already processed" -ForegroundColor Cyan
}

# Load designer metadata
$designers = Import-Csv -Path $csvPath

# Filter designers that need harvesting
$designersToHarvest = $designers | Where-Object {
    $folder = $_.Folder
    $folderPath = Join-Path $imagesDir $folder
    
    # Check if folder exists and has fewer than 3 images
    if (Test-Path $folderPath) {
        $imageCount = (Get-ChildItem -Path $folderPath -File | Where-Object { 
            $_.Extension -match "\.(jpg|jpeg|png|webp|gif)$" 
        }).Count
        return $imageCount -lt 3
    }
    return $true
}

Write-Host "Found $($designersToHarvest.Count) designers needing images" -ForegroundColor Yellow

$currentDelay = $baseDelay
$successCount = 0
$errorCount = 0
$totalDownloaded = 0

foreach ($designer in $designersToHarvest) {
    $name = $designer.Name
    $category = $designer.CategoryName
    $folder = $designer.Folder
    
    # Skip if already processed
    if ($progress.ContainsKey($folder)) {
        Write-Host "SKIP: $name (already processed)" -ForegroundColor Gray
        continue
    }
    
    Write-Host "`n=== Processing: $name ===" -ForegroundColor Cyan
    
    $targetDir = Join-Path $imagesDir $folder
    if (-not (Test-Path $targetDir)) {
        New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
    }
    
    # Build API URL
    $apiUrl = "https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=categorymembers&gcmtitle=Category:$category&gcmtype=file&gcmlimit=$imagesPerDesigner&prop=imageinfo&iiprop=url|size"
    
    try {
        Write-Host "Fetching from Wikimedia API..." -ForegroundColor Gray
        Start-Sleep -Seconds $currentDelay
        
        $response = Invoke-RestMethod -Uri $apiUrl -Method Get -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        if ($response.query -and $response.query.pages) {
            $pages = $response.query.pages
            $downloadedThisDesigner = 0
            
            foreach ($pageId in $pages.PSObject.Properties.Name) {
                $page = $pages.$pageId
                if ($page.imageinfo -and $page.imageinfo.Count -gt 0) {
                    $imageUrl = $page.imageinfo[0].url
                    $imageSize = $page.imageinfo[0].size
                    
                    # Skip small images (< 20KB)
                    if ($imageSize -lt 20480) {
                        Write-Host "  SKIP: $($page.title) (too small: $([math]::Round($imageSize/1024))KB)" -ForegroundColor DarkGray
                        continue
                    }
                    
                    # Extract filename
                    $fileName = [System.IO.Path]::GetFileName($imageUrl.Split('?')[0])
                    $localPath = Join-Path $targetDir $fileName
                    
                    # Download
                    try {
                        Write-Host "  Downloading: $fileName ($([math]::Round($imageSize/1024))KB)..." -ForegroundColor Green
                        Start-Sleep -Milliseconds 500
                        Invoke-WebRequest -Uri $imageUrl -OutFile $localPath -UserAgent "Mozilla/5.0"
                        $downloadedThisDesigner++
                        $totalDownloaded++
                    }
                    catch {
                        Write-Host "  ERROR downloading: $fileName - $($_.Exception.Message)" -ForegroundColor Red
                        $errorCount++
                    }
                }
            }
            
            Write-Host "Downloaded $downloadedThisDesigner images for $name" -ForegroundColor Green
            $successCount++
            
            # Reset delay on success
            $currentDelay = $baseDelay
            
            # Mark as processed
            $progress[$folder] = $true
            $progress | ConvertTo-Json | Set-Content -Path $progressFile
        }
        else {
            Write-Host "No images found for $name" -ForegroundColor Yellow
        }
    }
    catch {
        $errorMsg = $_.Exception.Message
        Write-Host "ERROR: $name - $errorMsg" -ForegroundColor Red
        $errorCount++
        
        # Check for rate limiting
        if ($errorMsg -match "429" -or $errorMsg -match "Too Many Requests") {
            $currentDelay = [Math]::Min($currentDelay * 2, $maxDelay)
            Write-Host "Rate limited! Increasing delay to $currentDelay seconds" -ForegroundColor Yellow
            Start-Sleep -Seconds $currentDelay
        }
    }
    
    # Batch pause every 5 designers
    if (($successCount + $errorCount) % $batchSize -eq 0) {
        Write-Host "`n--- Batch pause (30 seconds) ---" -ForegroundColor Magenta
        Start-Sleep -Seconds 30
    }
}

Write-Host "`n=== Harvesting Complete ===" -ForegroundColor Cyan
Write-Host "Designers processed: $successCount" -ForegroundColor Green
Write-Host "Total images downloaded: $totalDownloaded" -ForegroundColor Green
Write-Host "Errors: $errorCount" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })
Write-Host "Log saved to: $logFile"
