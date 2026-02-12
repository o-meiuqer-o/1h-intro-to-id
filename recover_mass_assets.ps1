$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$destDir = "D:\history of id course\images"
$csvPath = "D:\history of id course\mass_asset_list.csv"
$logPath = "D:\history of id course\mass_recovery.log"

# Use a standard browser User-Agent to avoid 403 blocks
$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

function Sanitize-Filename ($str) {
    if (-not $str) { return "unknown" }
    return $str.ToLower().Replace(" ", "_").Replace("-", "_").Replace("'", "").Replace("/", "_").Replace("(", "").Replace(")", "")
}

function Log-Message ($msg) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    try { Add-Content -Path $logPath -Value "[$timestamp] $msg" } catch {}
    Write-Host "[$timestamp] $msg"
}

Log-Message "Starting Mass Asset Recovery..."

$assets = Import-Csv -Path $csvPath

foreach ($asset in $assets) {
    $query = $asset.SearchQuery
    if (-not $query) { continue }

    $designer = Sanitize-Filename $asset.Designer
    $work = Sanitize-Filename $asset.Work
    $baseName = "${designer}_${work}"
    
    # Check if ANY extension exists
    $exists = $false
    $extensions = @(".jpg", ".jpeg", ".png", ".gif", ".webp")
    foreach ($ext in $extensions) {
        if (Test-Path "$destDir\$baseName$ext") {
            $exists = $true
            break
        }
    }

    if ($exists) {
        # Log-Message "Skipping $baseName (Already exists)"
        continue
    }

    Log-Message "Recovering: $query"

    try {
        # 1. Search API
        $searchUrl = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=File:$([Uri]::EscapeDataString($query))&gsrlimit=1&prop=imageinfo&iiprop=url|size&format=json"
        
        $json = Invoke-RestMethod -Uri $searchUrl -UserAgent $userAgent
        
        if (-not $json.query -or -not $json.query.pages) {
            Log-Message " [NOT FOUND] No results for '$query'"
            continue
        }

        $pages = $json.query.pages
        $firstPage = $pages.PSObject.Properties | Select-Object -First 1
        $pageData = $firstPage.Value
        
        if (-not $pageData.imageinfo) { continue }
        
        $imageUrl = $pageData.imageinfo[0].url
        $size = $pageData.imageinfo[0].size
        
        if (-not $imageUrl) { continue }

        Log-Message " [FOUND] Size: $([math]::Round($size/1KB, 0)) KB - URL: $imageUrl"

        if ($ext -match "\?") { $ext = $ext.Split("?")[0] }
        
        $targetPath = Join-Path $destDir "$baseName$ext"

        Invoke-WebRequest -Uri $imageUrl -OutFile $targetPath -UserAgent $userAgent -TimeoutSec 60
        
        Log-Message " [SAVED] $targetPath"
        
        # Longer delay to be safe
        Start-Sleep -Seconds 3

    } catch {
        Log-Message " [ERROR] Failed to process '$query': $($_.Exception.Message)"
        Start-Sleep -Seconds 2
    }
}

Log-Message "Recovery Complete."
