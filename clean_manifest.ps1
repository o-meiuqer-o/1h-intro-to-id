$manifestPath = "D:\history of id course\gallery_manifest.json"
$root = "D:\history of id course"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    
    $nameParts = $designer.name -split " "
    $firstName = $nameParts[0].Trim()
    $lastName = $nameParts[-1].Trim()
    
    # Identify Official Portrait
    # Priority: 'key_portrait.jpg' (e.g. rams_portrait.jpg)
    # Then: 'portrait' in name
    $official = $null
    
    # Check for exact key_portrait match
    $official = $designer.images | Where-Object { $_ -match "$($key)_portrait" } | Select-Object -First 1
    
    if (-not $official) {
        $official = $designer.images | Where-Object { $_ -match "portrait" } | Select-Object -First 1
    }
    
    # If we found an official portrait, filter the list
    if ($official) {
        $newImages = @()
        foreach ($img in $designer.images) {
            # Always keep the official one
            if ($img -eq $official) {
                $newImages += $img
                continue
            }
            
            # Check if this image is a "Duplicate Portrait" candidate
            $isDuplicate = $false
            $fileName = Split-Path $img -Leaf
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
            
            # Regex Patterns
            if ($fileName -match "portrait" -or $fileName -match "photo" -or $fileName -match "headshot") {
                $isDuplicate = $true
            }
            
            # Name Check (FirstName_LastName etc)
            $bn = $baseName.ToLower().Trim()
            $fn = $firstName.ToLower()
            $ln = $lastName.ToLower()
           
            if ($bn -eq "${fn}_${ln}" -or 
                $bn -eq "${ln}_${fn}" -or 
                $bn -eq "${fn}${ln}" -or 
                $bn -eq "${fn} ${ln}") {
                $isDuplicate = $true
            }
            
            if (-not $isDuplicate) {
                $newImages += $img
            } else {
                Write-Host "Removing duplicate from manifest [$key]: $fileName"
            }
        }
        
        $designer.images = $newImages
    }
}

$json | ConvertTo-Json -Depth 10 | Set-Content $manifestPath
Write-Host "Manifest cleaned."
