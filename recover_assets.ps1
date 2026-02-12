$ErrorActionPreference = "Stop"
$destDir = "D:\history of id course\images"
$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Explicit list of failed items with corrected Page URLs
$recoveryAssets = @(
    @{ Key="ive_imac"; Target="ive_imac"; Url="https://commons.wikimedia.org/wiki/File:IMac_G3_Bondi_Blue.png" },
    @{ Key="behrens_kettle"; Target="behrens_kettle"; Url="https://commons.wikimedia.org/wiki/File:Electric_water_kettle,_designed_by_Peter_Behrens,_AEG,_Berlin,_c._1909,_brass_-_Museum_Künstlerkolonie_Darmstadt_-_Mathildenhöhe_-_Darmstadt,_Germany_-_DSC06390.jpg" },
    @{ Key="dresser_claret"; Target="dresser_claret"; Url="https://commons.wikimedia.org/wiki/File:Christopher_Dresser_-_Claret_jug_-_Google_Art_Project.jpg" },
    @{ Key="gropius_adler"; Target="gropius_adler"; Url="https://commons.wikimedia.org/wiki/File:Adler_Standard_6.jpg" },
    @{ Key="loewy_avanti"; Target="loewy_avanti"; Url="https://commons.wikimedia.org/wiki/File:Studebaker_Avanti.jpg" },
    @{ Key="loewy_lucky"; Target="loewy_lucky"; Url="https://commons.wikimedia.org/wiki/File:Lucky_strike.jpg" },
    @{ Key="dreyfuss_we500"; Target="dreyfuss_we500"; Url="https://commons.wikimedia.org/wiki/File:WE500dialphone.jpg" },
    @{ Key="dreyfuss_t86"; Target="dreyfuss_t86"; Url="https://commons.wikimedia.org/wiki/File:T-86_Round_Thermostat,_1953.jpg" },
    @{ Key="dreyfuss_tractor"; Target="dreyfuss_tractor"; Url="https://commons.wikimedia.org/wiki/File:John_Deere_B_tractor_VA2.jpg" },
    @{ Key="bill_clock"; Target="bill_clock"; Url="https://commons.wikimedia.org/wiki/File:Junghans_Küchenuhr.jpg" },
    @{ Key="ulm"; Target="ulm_campus"; Url="https://commons.wikimedia.org/wiki/File:Hochschule_für_Gestaltung,_Ulm.jpg" },
    @{ Key="coldspot"; Target="coldspot"; Url="https://commons.wikimedia.org/wiki/File:Coldspot_Refrigerator.png" } 
)

function Get-ExtensionFromUrl ($url) {
    if ($url -match '\.(jpg|jpeg|png|gif|webp)$') { return $matches[0] }
    return ".jpg"
}

foreach ($asset in $recoveryAssets) {
    Write-Host "Recovering $($asset.Key)..." -NoNewline
    
    try {
        # 1. Scrape Page
        $pageReq = Invoke-WebRequest -Uri $asset.Url -UserAgent $userAgent -UseBasicParsing -TimeoutSec 30
        
        $downloadUrl = $null
        if ($pageReq.Content -match 'href="([^"]*upload\.wikimedia\.org[^"]*)"[^>]*>Original file</a>') {
            $downloadUrl = $matches[1]
        } elseif ($pageReq.Content -match 'href="([^"]*upload\.wikimedia\.org[^"]*)" class="internal"') {
            $downloadUrl = $matches[1]
        }
        
        if (-not $downloadUrl) {
            Write-Host " [FAILED: URL Pattern Not Found]" -ForegroundColor Red
            continue
        }

        if ($downloadUrl.StartsWith("//")) { $downloadUrl = "https:" + $downloadUrl }
        
        # 2. Download
        $ext = Get-ExtensionFromUrl $downloadUrl
        $finalPath = Join-Path $destDir "$($asset.Target)$ext"
        
        Invoke-WebRequest -Uri $downloadUrl -OutFile $finalPath -UserAgent $userAgent -UseBasicParsing -TimeoutSec 60
        
        $item = Get-Item $finalPath
        if ($item.Length -gt 15000) {
            Write-Host " [OK] Saved as $($asset.Target)$ext ($([math]::Round($item.Length/1KB, 0)) KB)" -ForegroundColor Green
        } else {
            Write-Host " [WARNING: Small File]" -ForegroundColor Yellow
        }
        
        # Rate Limit Pause
        Start-Sleep -Seconds 5

    } catch {
        Write-Host " [ERROR: $($_.Exception.Message)]" -ForegroundColor Red
        Start-Sleep -Seconds 5
    }
}
