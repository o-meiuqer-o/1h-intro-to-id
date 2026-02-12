$manifestPath = "D:\history of id course\gallery_manifest.json"
$root = "D:\history of id course"
$extras = "D:\history of id course\images\_extras"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    
    # Target portrait file (usually the one with 'portrait' in it, or the 6th-ish item, but let's assume valid naming)
    # We will try to find the manifest entry that looks like a portrait.
    $portraitEntry = $designer.images | Where-Object { $_ -match "portrait" } | Select-Object -First 1
    
    if (-not $portraitEntry) {
         # If no explicit portrait file in manifest, roughly guess it's the one with the designer's name
         $portraitEntry = $designer.images | Where-Object { $_ -match $designer.name -or $_ -match $key } | Select-Object -First 1
    }
    
    if ($portraitEntry) {
        $fullPath = Join-Path $root $portraitEntry
        $fileName = Split-Path $fullPath -Leaf
        $folder = Split-Path $fullPath -Parent
        
        if (-not (Test-Path $fullPath)) {
            Write-Host "Missing: $fileName. Checking Extras..."
            
            # Check _extras/designerName
            $extrasFolder = Join-Path $extras $key
            
            if (Test-Path $extrasFolder) {
                # Find any image in extras
                $recovery = Get-ChildItem $extrasFolder -File | Select-Object -First 1
                
                if ($recovery) {
                    if (-not (Test-Path $folder)) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }
                    
                    Write-Host "Recovering from extras: $($recovery.Name) -> $fileName"
                    Copy-Item $recovery.FullName -Destination $fullPath
                } else {
                    Write-Host "No files in extras for $key"
                }
            } else {
                Write-Host "No extras folder for $key"
            }
        }
    }
}
