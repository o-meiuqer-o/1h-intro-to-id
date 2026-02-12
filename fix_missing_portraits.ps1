$manifestPath = "D:\history of id course\gallery_manifest.json"
$root = "D:\history of id course"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    
    # Identify the "portrait" file in the list.
    # Usually it is 'designer_portrait.jpg' or contains 'portrait'.
    # Or we just count the missing ones.
    
    foreach ($imgRelPath in $designer.images) {
        $fullPath = Join-Path $root $imgRelPath
        
        if (-not (Test-Path $fullPath)) {
            $folder = Split-Path $fullPath -Parent
            $fileName = Split-Path $fullPath -Leaf
            
            # Use heuristics to find a replacement in $folder
            if (Test-Path $folder) {
                $candidates = Get-ChildItem $folder -File
                $replacement = $null
                
                # Strategy 1: Look for files with designer name but not 'portrait' (since portrait is missing)
                # Strategy 2: Look for 'portrait' variations like 'Portrait' or 'photo'
                
                # Priority 1: Contains "portrait" or "photo" or "headshot"
                $p1 = $candidates | Where-Object { $_.Name -match "(portrait|photo|headshot)" } | Select-Object -First 1
                if ($p1) { $replacement = $p1 }
                
                # Priority 2: Contains full name (fuzzy) or last name
                if (-not $replacement) {
                    $nameParts = $designer.name -split " "
                    $lastName = $nameParts[-1]
                    $p2 = $candidates | Where-Object { $_.Name -match $lastName -and $_.Name -notmatch "chair|lamp|sofa|table|house" } | Select-Object -First 1
                    if ($p2) { $replacement = $p2 }
                }
                
                # Priority 3: Just take the largest file that isn't known to be a work?
                # Risky. Let's stick to P1 and P2.
                
                if ($replacement) {
                    Write-Host "Restoring $fileName using $($replacement.Name)"
                    Rename-Item $replacement.FullName -NewName $fileName
                } else {
                    Write-Host "Could not find replacement for $fileName in $folder"
                }
            }
        }
    }
}
