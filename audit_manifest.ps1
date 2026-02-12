$manifestPath = "D:\history of id course\gallery_manifest.json"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

$missing = @()

foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    
    # Assuming the portrait is one of the images, typically the one with 'portrait' in name
    # OR we look at all images in the list.
    
    foreach ($imgRelPath in $designer.images) {
        $fullPath = Join-Path "D:\history of id course" $imgRelPath
        if (-not (Test-Path $fullPath)) {
            $missing += [PSCustomObject]@{
                Designer = $key
                MissingFile = $imgRelPath
            }
        }
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Found $($missing.Count) missing images from manifest:"
    $missing | Format-Table -AutoSize
} else {
    Write-Host "All manifest images exist."
}
