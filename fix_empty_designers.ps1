$root = "D:\history of id course"

# EAMES
$eamesFolder = "$root\images\eames"
$eamesPortrait = "$eamesFolder\Charles and Ray Eames.jpg"
if (-not (Test-Path $eamesPortrait)) {
    $fallback = Get-ChildItem $eamesFolder -Filter "*.jpg" | Select-Object -First 1
    if ($fallback) {
        Write-Host "Fixing Eames with fallback: $($fallback.Name)"
        Copy-Item $fallback.FullName -Destination $eamesPortrait
    } else {
        Write-Host "Eames folder is empty!"
    }
}

# PININFARINA
$pinFolder = "$root\images\pininfarina"
$pinPortrait = "$pinFolder\pininfarina_portrait.jpg"
if (-not (Test-Path $pinFolder)) { New-Item -ItemType Directory -Path $pinFolder -Force }

if (-not (Test-Path $pinPortrait)) {
   # Check if any files exist
   $fallback = Get-ChildItem $pinFolder -Filter "*.jpg" | Select-Object -First 1
   if ($fallback) {
       Write-Host "Fixing Pininfarina with fallback: $($fallback.Name)"
       Copy-Item $fallback.FullName -Destination $pinPortrait
   } else {
       Write-Host "Pininfarina folder is empty! Cannot fix."
   }
}
