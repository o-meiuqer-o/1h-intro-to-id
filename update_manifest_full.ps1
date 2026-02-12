$manifestPath = "D:\history of id course\gallery_manifest.json"
$root = "D:\history of id course"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    
    $folderPath = Join-Path $root "images\$key"
    if (-not (Test-Path $folderPath)) { continue }
    
    # Get all images
    $files = Get-ChildItem $folderPath -Include *.jpg, *.jpeg, *.png, *.webp -Recurse
    
    $imageList = @()
    $portrait = $null
    
    foreach ($f in $files) {
        # Create relative path
        # images/key/filename
        $relPath = "images/$key/" + $f.Name
        
        # Identify Portrait for sorting
        if ($f.Name -match "portrait" -or $f.Name -match "photo" -or $f.Name -match "headshot") {
            $portrait = $relPath
        } else {
            $imageList += $relPath
        }
    }
    
    # Sort works alphabetically
    $imageList = $imageList | Sort-Object
    
    # Prepend Portrait
    if ($portrait) {
        $finalList = @($portrait) + $imageList
    } else {
        # Fallback: Try to find name match if no explicit 'portrait'
        $designerName = $json.$key.name
        $nameParts = $designerName -split " "
        $lastName = $nameParts[-1]
        
        # Check if any image looks like a portrait based on earlier conventions (e.g. key_portrait.jpg might be missing)
        # We did a cleanup.
        # Just use the first one if no portrait found, OR keep it separate?
        # The UI uses images[0] as the hero/portrait. So we MUST put the best candidate first.
        
        $finalList = $imageList
    }
    
    # Update JSON
    $json.$key.images = $finalList
    Write-Host "Updated ${key}: $($finalList.Count) images."
}

$json | ConvertTo-Json -Depth 10 | Set-Content $manifestPath
Write-Host "Manifest update complete."
