param(
    [string]$DesignerFolder,
    [string[]]$Works,
    [string]$PlaceHolderPath = "D:\history of id course\place holder.png",
    [string]$CsvPath = "D:\history of id course\missing_images.csv"
)

# Ensure CSV exists with headers
if (-not (Test-Path $CsvPath)) {
    Set-Content -Path $CsvPath -Value "Designer,Work,Status,Date" -Encoding UTF8
}

$imagesDir = "D:\history of id course\images\$DesignerFolder"
if (-not (Test-Path $imagesDir)) {
    New-Item -ItemType Directory -Path $imagesDir | Out-Null
}

foreach ($work in $Works) {
    # Sanitize filename
    $cleanWork = $work -replace " ", "_" -replace "[^a-zA-Z0-9_]", ""
    $outputFile = "$imagesDir\$($DesignerFolder)_$($cleanWork.ToLower()).jpg"
    
    if (Test-Path $outputFile) {
        Write-Host "Skipping existing: $work" -ForegroundColor Gray
        continue
    }

    Write-Host "Generating placeholder for: $work" -ForegroundColor Cyan
    
    if (Test-Path $PlaceHolderPath) {
        Copy-Item $PlaceHolderPath -Destination $outputFile
        
        $currentDate = Get-Date -Format "yyyy-MM-dd HH:mm"
        $logLine = "$DesignerFolder,$work,Placeholder_Used,$currentDate"
        Add-Content -Path $CsvPath -Value $logLine -Encoding UTF8
    } else {
        Write-Host "Placeholder file not found!" -ForegroundColor Red
    }
}
