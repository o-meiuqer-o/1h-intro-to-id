$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$destDir = "D:\history of id course\images"
$csvPath = "D:\history of id course\mass_asset_list.csv"
$logPath = "D:\history of id course\mass_download.log"

$userAgent = "ID_Course_Student_Project/1.0 (contact@example.com)"

function Sanitize-Filename ($str) {
    if (-not $str) { return "unknown" }
    return $str.ToLower().Replace(" ", "_").Replace("-", "_").Replace("'", "").Replace("/", "_").Replace("(", "").Replace(")", "")
}

function Log-Message ($msg) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    try { Add-Content -Path $logPath -Value "[$timestamp] $msg" } catch {}
    Write-Host "[$timestamp] $msg"
}

Log-Message "Starting Mass Asset Download..."

if (-not (Test-Path $csvPath)) {
    Log-Message "CSV not found at $csvPath"
    exit
}

$assets = Import-Csv -Path $csvPath

foreach ($asset in $assets) {
    $query = $asset.SearchQuery
    if (-not $query) { continue }

    $designer = Sanitize-Filename $asset.Designer
    $work = Sanitize-Filename $asset.Work
    
    $baseName = "${designer}_${work}"
    
    # Check existing files
    if ((Test-Path "$destDir\$baseName.jpg") -or (Test-Path "$destDir\$baseName.png") -or (Test-Path "$destDir\$baseName.jpeg")) {
        Log-Message "Skipping $baseName (Already exists)"
        continue
    }

    Log-Message "Searching for: $query"

    try {
        # 1. Search API
        $searchUrl = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=File:$([Uri]::EscapeDataString($query))&gsrlimit=1&prop=imageinfo&iiprop=url|size&format=json"
        
        $json = Invoke-RestMethod -Uri $searchUrl -UserAgent $userAgent
        
        if (-not $json.query -or -not $json.query.pages) {
            Log-Message " [NOT FOUND] No results for '$query'"
            continue
        }

        # Get first page safely
        $pages = $json.query.pages
        $firstPage = $pages.PSObject.Properties | Select-Object -First 1
        
        if (-not $firstPage) {
            Log-Message " [ERROR] Could not extract page from response"
            continue
        }
        
        $pageData = $firstPage.Value
        
        if (-not $pageData.imageinfo) {
             Log-Message " [ERROR] No imageinfo for '$query'"
             continue
        }
        
        $imageUrl = $pageData.imageinfo[0].url
        $size = $pageData.imageinfo[0].size
        
        if (-not $imageUrl) {
            Log-Message " [ERROR] No URL in imageinfo"
            continue
        }

        Log-Message " [FOUND] Size: $([math]::Round($size/1KB, 0)) KB - URL: $imageUrl"

        # 2. Download
        $ext = [IO.Path]::GetExtension($imageUrl)
        # Handle query params in older wikimedia urls if any
        if ($ext -match "\?") { $ext = $ext.Split("?")[0] }
        
        $targetPath = Join-Path $destDir "$baseName$ext"

        invoke-WebRequest -Uri $imageUrl -OutFile $targetPath -UserAgent $userAgent -TimeoutSec 60
        
        Log-Message " [SAVED] $targetPath"
        
        # Rate Limit
        Start-Sleep -Seconds 2

    } catch {
        Log-Message " [ERROR] Failed to process '$query': $($_.Exception.Message)"
        Start-Sleep -Seconds 2
    }
}

Log-Message "Mass Download Complete."
