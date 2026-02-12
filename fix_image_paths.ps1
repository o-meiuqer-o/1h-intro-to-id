$htmlFile = "D:\history of id course\index.html"
$logFile = "D:\history of id course\image_organization_log.txt"
$backupFile = "D:\history of id course\index_backup_before_path_fix.html"

# Create backup
Copy-Item -Path $htmlFile -Destination $backupFile -Force
Write-Host "Created backup: $backupFile" -ForegroundColor Cyan

# Read the HTML content
$html = Get-Content -Path $htmlFile -Raw -Encoding UTF8

# Parse the log file to get all moved files
$logContent = Get-Content -Path $logFile
$replacements = @()

foreach ($line in $logContent) {
    if ($line -match "^MOVED: (.+?) .+ (.+)/$") {
        $oldFileName = $matches[1]
        $newFolder = $matches[2]
        
        # Create the path mapping
        $oldPath = "images/$oldFileName"
        $newPath = "images/$newFolder/$oldFileName"
        
        $replacements += @{
            Old = $oldPath
            New = $newPath
        }
    }
}

Write-Host "`nFound $($replacements.Count) file movements to process" -ForegroundColor Yellow

# Apply replacements
$changeCount = 0
foreach ($replacement in $replacements) {
    $oldPath = $replacement.Old
    $newPath = $replacement.New
    
    # Check if this path exists in the HTML
    if ($html -match [regex]::Escape($oldPath)) {
        $html = $html -replace [regex]::Escape($oldPath), $newPath
        $changeCount++
        Write-Host "Fixed: $oldPath to $newPath" -ForegroundColor Green
    }
}

# Save the updated HTML
$html | Set-Content -Path $htmlFile -Encoding UTF8 -NoNewline

Write-Host "`n=== Path Fix Complete ===" -ForegroundColor Cyan
Write-Host "Total replacements made: $changeCount" -ForegroundColor Green
Write-Host "Backup saved to: $backupFile" -ForegroundColor Gray
