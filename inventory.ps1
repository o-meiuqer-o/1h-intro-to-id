$files = Get-ChildItem -Path "D:\history of id course\images" -File -Recurse
Write-Host "=== TOTAL ==="
Write-Host "Files: $($files.Count)"
Write-Host "Size: $([math]::Round(($files | Measure-Object -Property Length -Sum).Sum / 1MB, 1)) MB"
Write-Host ""
Write-Host "=== BY EXTENSION ==="
$files | Group-Object Extension | Sort-Object Count -Descending | ForEach-Object {
    Write-Host "  $($_.Name): $($_.Count)"
}
Write-Host ""
Write-Host "=== LARGE FILES (>2MB) ==="
$files | Where-Object { $_.Length -gt 2MB } | Sort-Object Length -Descending | ForEach-Object {
    $rel = $_.FullName.Replace("D:\history of id course\images\", "")
    Write-Host "  $([math]::Round($_.Length/1MB,2)) MB - $rel"
}
Write-Host ""
Write-Host "=== PER DESIGNER ==="
Get-ChildItem -Path "D:\history of id course\images" -Directory | Where-Object { $_.Name -notlike '_*' } | Sort-Object Name | ForEach-Object {
    $count = (Get-ChildItem $_.FullName -File -Recurse).Count
    Write-Host "  $($_.Name): $count"
}
