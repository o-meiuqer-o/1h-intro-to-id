$imagesDir = "D:\history of id course\images"
$logFile = "D:\history of id course\image_organization_log.txt"

# Mapping of filename patterns to designer folders
$designerMappings = @{
    "christopher_dresser" = "dresser"
    "dresser_" = "dresser"
    "dieter_rams" = "rams"
    "ive_" = "ive"
    "jonathan" = "ive"
    "gropius_" = "gropius"
    "walter_gropius" = "gropius"
    "breuer_" = "breuer"
    "marcel_breuer" = "breuer"
    "marcel breuer" = "breuer"
    "loewy_" = "loewy"
    "raymond_loewy" = "loewy"
    "raymond loewy" = "loewy"
    "dreyfuss" = "dreyfuss"
    "henry_dreyfuss" = "dreyfuss"
    "eames" = "eames"
    "charles and ray eames" = "eames"
    "guimard" = "guimard"
    "hector guimard" = "guimard"
    "lihotzky" = "lihotzky"
    "margarete" = "lihotzky"
    "bill_" = "bill"
    "max_bill" = "bill"
    "ettore_sottsass" = "sottsass"
    "sottsass" = "sottsass"
    "morris" = "morris"
    "william_morris" = "morris"
    "behrens_" = "behrens"
    "peter_behrens" = "behrens"
}

# Additional mappings for specific files
$specificMappings = @{
    "braun_razor.jpg" = "rams"
    "braun_sk4.jpg" = "rams"
    "rams_sk4.jpg" = "rams"
    "rams_t3.jpg" = "rams"
    "vitsoe_606.jpg" = "rams"
    "ulm_stool.jpg" = "bill"
    "bill_stool.jpg" = "bill"
    "max_bill_ulm_stool.webp" = "bill"
    "carlton_bookshelf.jpg" = "sottsass"
    "casablanca_sideboard.jpg" = "sottsass"
    "magno_radio.jpg" = "sottsass"
    "wedgwood vase.jpg" = "dresser"
    "missing.jpg" = "_archive"
}

# Create missing designer folders
$missingFolders = @("guimard", "lihotzky", "morris", "bill", "_archive")
foreach ($folder in $missingFolders) {
    $folderPath = Join-Path $imagesDir $folder
    if (-not (Test-Path $folderPath)) {
        New-Item -Path $folderPath -ItemType Directory -Force | Out-Null
        Write-Host "Created folder: $folder"
    }
}

# Get all image files in root directory
$imageFiles = Get-ChildItem -Path $imagesDir -File | Where-Object { 
    $_.Extension -match "\.(jpg|jpeg|png|webp|gif)$" 
}

$moveLog = @()
$movedCount = 0
$skippedCount = 0

foreach ($file in $imageFiles) {
    $fileName = $file.Name.ToLower()
    $targetFolder = $null
    
    # Check specific mappings first
    if ($specificMappings.ContainsKey($file.Name)) {
        $targetFolder = $specificMappings[$file.Name]
    }
    else {
        # Check pattern mappings
        foreach ($pattern in $designerMappings.Keys) {
            if ($fileName.Contains($pattern.ToLower())) {
                $targetFolder = $designerMappings[$pattern]
                break
            }
        }
    }
    
    if ($targetFolder) {
        $targetPath = Join-Path $imagesDir $targetFolder
        $destinationFile = Join-Path $targetPath $file.Name
        
        # Check if file already exists in destination
        if (Test-Path $destinationFile) {
            $logEntry = "SKIPPED: $($file.Name) (already exists in $targetFolder)"
            $moveLog += $logEntry
            $skippedCount++
        }
        else {
            try {
                Move-Item -Path $file.FullName -Destination $destinationFile -Force
                $logEntry = "MOVED: $($file.Name) → $targetFolder/"
                $moveLog += $logEntry
                $movedCount++
                Write-Host $logEntry -ForegroundColor Green
            }
            catch {
                $logEntry = "ERROR: $($file.Name) - $($_.Exception.Message)"
                $moveLog += $logEntry
                Write-Host $logEntry -ForegroundColor Red
            }
        }
    }
    else {
        $logEntry = "UNMATCHED: $($file.Name) (no designer folder identified)"
        $moveLog += $logEntry
        Write-Host $logEntry -ForegroundColor Yellow
    }
}

# Write log file
$moveLog | Set-Content -Path $logFile -Encoding UTF8

Write-Host "`n=== Organization Complete ===" -ForegroundColor Cyan
Write-Host "Moved: $movedCount files" -ForegroundColor Green
Write-Host "Skipped: $skippedCount files" -ForegroundColor Yellow
Write-Host "Log saved to: $logFile"
