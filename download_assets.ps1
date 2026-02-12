$ErrorActionPreference = "Stop"
$destDir = "D:\history of id course\images"
$csvPath = "D:\history of id course\assets.csv"
New-Item -ItemType Directory -Force -Path $destDir | Out-Null

$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Import CSV
$assets = Import-Csv -Path $csvPath

# Function to get extension from URL
function Get-ExtensionFromUrl ($url) {
    if ($url -match '\.(jpg|jpeg|png|gif|webp)$') {
        return $matches[0]
    }
    return ".jpg" # Default
}

foreach ($asset in $assets) {
    $baseName = $asset.TargetFilename
    # Skip if already verified good size? No, user wants to fix broken ones.
    
    Write-Host "Processing $($asset.Key) ..." -NoNewline
    
    try {
        $downloadUrl = $asset.Url
        
        if ($asset.Type -eq "Page") {
            # Scrape direct link using BasicParsing (Raw HTML, no DOM/Browser)
            $pageReq = Invoke-WebRequest -Uri $asset.Url -UserAgent $userAgent -UseBasicParsing -TimeoutSec 30
            
            # Regex to find the "Original file" link
            # Look for href="...upload.wikimedia.org..." text="Original file"
            # Pattern: <a href="(url)" ...>Original file</a>
            if ($pageReq.Content -match 'href="([^"]*upload\.wikimedia\.org[^"]*)"[^>]*>Original file</a>') {
                $downloadUrl = $matches[1]
            } elseif ($pageReq.Content -match 'href="([^"]*upload\.wikimedia\.org[^"]*)" class="internal"') {
                $downloadUrl = $matches[1]
            } else {
                Write-Host " [FAILED: Could not find Original File URL]" -ForegroundColor Red
                continue
            }
            
            # Fix relative protocol
            if ($downloadUrl.StartsWith("//")) {
                $downloadUrl = "https:" + $downloadUrl
            }
        }

        # Clean URL
        if ($downloadUrl -match "\?") { $downloadUrl = $downloadUrl.Split("?")[0] }

        # Get correct extension
        $ext = Get-ExtensionFromUrl $downloadUrl
        
        $finalPath = Join-Path $destDir "$baseName$ext"

        # Download
        Invoke-WebRequest -Uri $downloadUrl -OutFile $finalPath -UserAgent $userAgent -UseBasicParsing -TimeoutSec 60
        
        # Verify
        $item = Get-Item $finalPath
        if ($item.Length -gt 15000) {
            Write-Host " [OK] Saved as $baseName$ext ($([math]::Round($item.Length/1KB, 0)) KB)" -ForegroundColor Green
            # Update CSV in memory (conceptually) or print for log
        } else {
            Write-Host " [WARNING: Small File]" -ForegroundColor Yellow
        }
    } catch {
        Write-Host " [ERROR: $($_.Exception.Message)]" -ForegroundColor Red
    }
}
