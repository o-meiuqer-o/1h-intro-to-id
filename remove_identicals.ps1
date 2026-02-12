$targetFile = "D:\history of id course\place holder.png"
$rootFolder = "D:\history of id course\images"

if (-not (Test-Path $targetFile)) {
    Write-Host "Target file not found: $targetFile"
    exit
}

$targetHash = (Get-FileHash -Path $targetFile -Algorithm SHA256).Hash
Write-Host "Monitoring for files identical to: $targetFile"
Write-Host "Target Hash: $targetHash"

$files = Get-ChildItem -Path $rootFolder -Recurse -File

$count = 0
foreach ($file in $files) {
    try {
        $fileHash = (Get-FileHash -Path $file.FullName -Algorithm SHA256).Hash
        if ($fileHash -eq $targetHash) {
            Write-Host "Deleting duplicate: $($file.FullName)"
            Remove-Item -Path $file.FullName -Force
            $count++
        }
    }
    catch {
        Write-Host "Error processing file: $($file.Name)"
    }
}

Write-Host "Total files deleted: $count"
