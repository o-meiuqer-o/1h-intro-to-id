$csvPath = "D:\history of id course\expanded_designers.csv"
$baseDir = "D:\history of id course\images"

$designers = Import-Csv -Path $csvPath

foreach ($d in $designers) {
    if (-not $d.Folder) { continue }
    $targetPath = Join-Path $baseDir $d.Folder
    if (-not (Test-Path $targetPath)) {
        New-Item -ItemType Directory -Force -Path $targetPath | Out-Null
        Write-Host "Created: $targetPath"
    } else {
        Write-Host "Exists: $targetPath"
    }
}
Write-Host "Folder structure setup complete."
