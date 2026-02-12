$root = "D:\history of id course"
$folder = "D:\history of id course\images\rams"

$firstName = "Dieter"
$lastName = "Rams"

$files = Get-ChildItem $folder -File
foreach ($file in $files) {
    Write-Host "Checking $($file.Name)... BaseName: $($file.BaseName)"
    
    if ($file.BaseName -eq "$firstName_$lastName") {
        Write-Host "MATCH FOUND: $($file.Name) matches ${firstName}_${lastName}"
    } else {
        Write-Host "NO MATCH: '$($file.BaseName)' vs '${firstName}_${lastName}'"
    }
}
