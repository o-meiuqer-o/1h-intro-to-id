$extrasRoot = "D:\history of id course\images\_extras"
$targetRoot = "D:\history of id course\images"

$designers = Get-ChildItem $extrasRoot -Directory

foreach ($d in $designers) {
    $targetDir = Join-Path $targetRoot $d.Name
    if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force }
    
    $files = Get-ChildItem $d.FullName -File
    
    foreach ($f in $files) {
        $name = $f.Name
        
        # Cleanup logic
        # 1. Remove "File:" prefix
        $name = $name -replace "^File:", ""
        # 2. Remove generic prefixes (e.g., "Gerhard_Roese__", "D2_")
        $name = $name -replace "^[A-Za-z0-9]+__", "" 
        $name = $name -replace "^[A-Z0-9]+_", ""  # Be careful with this one. D2_ matches.
        
        # 3. Replace spaces, %20, and other chars with underscores
        $name = $name -replace "%20", "_"
        $name = $name -replace " ", "_"
        $name = $name -replace "-", "_"
        
        # 4. Remove multiple underscores
        $name = $name -replace "_+", "_"
        
        # 5. Ensure starts with designer name (Handle case insensitivity)
        if (-not ($name.ToLower().StartsWith($d.Name.ToLower()))) {
            $name = $d.Name + "_" + $name
        }
        
        # 6. Lowercase
        $name = $name.ToLower()
        
        # Move
        $dest = Join-Path $targetDir $name
        
        # Avoid overwrite
        $i = 1
        while (Test-Path $dest) {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($name)
            $ext = [System.IO.Path]::GetExtension($name)
            # Remove any existing _extra suffix to avoid chain
            $base = $base -replace "_extra\d+$", ""
            
            $dest = Join-Path $targetDir "${base}_extra${i}${ext}"
            $i++
        }
        
        Write-Host "Moving $($f.Name) -> $dest"
        Move-Item $f.FullName -Destination $dest
    }
}

Write-Host "Processed all extras."
