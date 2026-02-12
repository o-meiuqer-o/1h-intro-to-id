$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$destDir = "D:\history of id course\images"
$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# List of assets with DIRECT URLs where known, or Page URLs
$assets = @(
    @{ Key="dreyfuss_we500"; Url="https://upload.wikimedia.org/wikipedia/commons/2/23/WE500dialphone.jpg"; Type="Direct" },
    @{ Key="dreyfuss_t86"; Url="https://upload.wikimedia.org/wikipedia/commons/2/2f/T-86_Round_Thermostat%2C_1953.jpg"; Type="Direct" },
    @{ Key="dreyfuss_tractor"; Url="https://upload.wikimedia.org/wikipedia/commons/0/05/John_Deere_B_tractor_VA2.jpg"; Type="Direct" },
    @{ Key="bill_clock"; Url="https://upload.wikimedia.org/wikipedia/commons/e/ea/Junghans_K%C3%BCchenuhr.jpg"; Type="Direct" },
    @{ Key="gropius_adler"; Url="https://upload.wikimedia.org/wikipedia/commons/e/e0/Adler_Standard_6.jpg"; Type="Direct" },
    @{ Key="loewy_lucky"; Url="https://upload.wikimedia.org/wikipedia/commons/3/36/Lucky_strike.jpg"; Type="Direct" },
    @{ Key="loewy_avanti"; Url="https://commons.wikimedia.org/wiki/File:Studebaker_Avanti.jpg"; Type="Page" },
    @{ Key="behrens_kettle"; Url="https://commons.wikimedia.org/wiki/File:Electric_water_kettle,_designed_by_Peter_Behrens,_AEG,_Berlin,_c._1909,_brass_-_Museum_Künstlerkolonie_Darmstadt_-_Mathildenhöhe_-_Darmstadt,_Germany_-_DSC06390.jpg"; Type="Page" },
    @{ Key="dresser_claret"; Url="https://commons.wikimedia.org/wiki/File:Christopher_Dresser_-_Claret_jug_-_Google_Art_Project.jpg"; Type="Page" },
    @{ Key="ulm_campus"; Url="https://commons.wikimedia.org/wiki/File:Hochschule_f%C3%BCr_Gestaltung,_Ulm.jpg"; Type="Page" }
)

foreach ($asset in $assets) {
    Write-Host "Processing $($asset.Key)..." -NoNewline
    $targetPath = Join-Path $destDir "$($asset.Key).jpg"
    
    try {
        $downloadUrl = $asset.Url
        
        if ($asset.Type -eq "Page") {
            # Scrape
            $pageReq = Invoke-WebRequest -Uri $asset.Url -UserAgent $userAgent -UseBasicParsing -TimeoutSec 30
             if ($pageReq.Content -match 'href="([^"]*upload\.wikimedia\.org[^"]*)"[^>]*>Original file</a>') {
                $downloadUrl = $matches[1]
            } elseif ($pageReq.Content -match 'href="([^"]*upload\.wikimedia\.org[^"]*)" class="internal"') {
                $downloadUrl = $matches[1]
            } else {
                Write-Host " [FAILED: URL not found]" -ForegroundColor Red
                continue
            }
            if ($downloadUrl.StartsWith("//")) { $downloadUrl = "https:" + $downloadUrl }
        }
        
        # Download
        Invoke-WebRequest -Uri $downloadUrl -OutFile $targetPath -UserAgent $userAgent -UseBasicParsing -TimeoutSec 60
        
        $item = Get-Item $targetPath
        if ($item.Length -gt 15000) {
            Write-Host " [OK] ($([math]::Round($item.Length/1KB, 0)) KB)" -ForegroundColor Green
        } else {
            Write-Host " [WARNING: Small File]" -ForegroundColor Yellow
        }
        
        Start-Sleep -Seconds 5
        
    } catch {
        Write-Host " [ERROR: $($_.Exception.Message)]" -ForegroundColor Red
        Start-Sleep -Seconds 5
    }
}
