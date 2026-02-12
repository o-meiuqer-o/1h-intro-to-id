$imagesDir = "D:\history of id course\images"
$outputFile = "D:\history of id course\gallery_manifest.json"
$csvPath = "D:\history of id course\expanded_designers.csv"
$baseUrl = "images"

$galleryData = @{}

# Load Designer Metadata
$designers = Import-Csv -Path $csvPath
$designerMeta = @{}
foreach ($d in $designers) {
    $designerMeta[$d.Folder] = @{
        Name = $d.Name
        Birth = $d.Birth
        Death = if ($d.Death) { $d.Death } else { $null }
        PeakYear = $d.PeakYear
    }
}

# Get all designer folders
$folders = Get-ChildItem -Path $imagesDir -Directory

foreach ($folder in $folders) {
    $designerId = $folder.Name
    $files = Get-ChildItem -Path $folder.FullName -File
    
    $images = @()
    foreach ($file in $files) {
        if ($file.Extension -match "\.(jpg|jpeg|png|gif|webp)$") {
            $images += "$baseUrl/$designerId/$($file.Name)"
        }
    }
    
    if ($images.Count -gt 0) {
        $meta = $designerMeta[$designerId]
        if (-not $meta) { 
            $meta = @{ 
                Name = $designerId
                Birth = 1900
                Death = $null
                PeakYear = 1950
            } 
        }
        
        $galleryData[$designerId] = @{
            name = $meta.Name
            birth = $meta.Birth
            death = $meta.Death
            peakYear = $meta.PeakYear
            images = $images
        }
    }
}

$json = $galleryData | ConvertTo-Json -Depth 4
$json | Set-Content -Path $outputFile -Encoding UTF8

Write-Host "Generated enhanced gallery_manifest.json with birth/death data for $($galleryData.Count) designers."
