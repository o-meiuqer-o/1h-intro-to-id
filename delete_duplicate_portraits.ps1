$manifestPath = "D:\history of id course\gallery_manifest.json"
$root = "D:\history of id course"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

$allProtected = @()

# 1. Collect all Protected Files (Official Manifest Images)
foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    foreach ($img in $designer.images) {
        $fullPath = Join-Path $root $img
        $allProtected += $fullPath
    }
}

# 2. Iterate Designers and Cleanup
foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    
    $folderPath = Join-Path $root "images\$key"
    if (-not (Test-Path $folderPath)) { continue }
    
    # Generate Name Patterns
    $nameParts = $designer.name -split " "
    $firstName = $nameParts[0]
    $lastName = $nameParts[-1]
    
    $pats = @(
        "*portrait*",
        "*photograph*",
        "*headshot*",
        "$($firstName)_$($lastName)*",      # Dieter_Rams*
        "$($lastName)_$($firstName)*",      # Rams_Dieter*
        "$($firstName)$($lastName)*",       # DieterRams*
        "$($firstName) $($lastName)*"       # Dieter Rams*
    )
    
    $files = Get-ChildItem $folderPath -File
    
    foreach ($file in $files) {
        # Check if Protected
        if ($allProtected -contains $file.FullName) {
            continue
        }
        
        # Check if matches Pattern
        $matchesPattern = $false
        foreach ($pat in $pats) {
            if ($file.Name -like $pat) {
                $matchesPattern = $true
                break
            }
        }
        
        if ($matchesPattern) {
            Write-Host "Deleting duplicate portrait: $($file.Name)"
            Remove-Item $file.FullName -Force
        }
    }
}
