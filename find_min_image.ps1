Add-Type -AssemblyName System.Drawing

$files = Get-ChildItem "D:\history of id course\images" -Recurse | Where-Object { $_.Extension -match "\.(jpg|png|webp)$" }

if ($files.Count -eq 0) {
    Write-Host "No images found."
    exit
}

$minHeight = 99999
$minImage = ""

foreach ($file in $files) {
    try {
        $stream = [System.IO.File]::OpenRead($file.FullName)
        $image = [System.Drawing.Image]::FromStream($stream, $false, $false)
        
        if ($image.Height -lt $minHeight) {
            $minHeight = $image.Height
            $minImage = $file.FullName
        }
        
        $image.Dispose()
        $stream.Close()
    }
    catch {
        Write-Host "Error reading $($file.Name): $_"
    }
}

Write-Host "Smallest Image: $minImage"
Write-Host "Height: $minHeight"
