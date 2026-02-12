$manifestPath = "D:\history of id course\gallery_manifest.json"
$root = "D:\history of id course"
$json = Get-Content $manifestPath -Raw | ConvertFrom-Json

$allProtected = @()

# Helper to normalize path
function Standardize-Path($p) {
    return [System.IO.Path]::GetFullPath($p)
    # create-react-app style paths or whatever
}

Write-Host "Building Protected List..."
foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    foreach ($img in $designer.images) {
        $fullPath = Join-Path $root $img
        # Normalize slashes
        $norm = $fullPath.Replace('/', '\')
        $allProtected += $norm
    }
}

Write-Host "Protecting $($allProtected.Count) images."

foreach ($key in $json.PSObject.Properties.Name) {
    if ($key -eq "_archive") { continue }
    $designer = $json.$key
    
    $folderPath = Join-Path $root "images\$key"
    if (-not (Test-Path $folderPath)) { continue }
    
    $nameParts = $designer.name -split " "
    $firstName = $nameParts[0].Trim()
    $lastName = $nameParts[-1].Trim()
    
    # Heuristics for duplicate portraits
    $pats = @(
        "*portrait*",
        "*photograph*",
        "*headshot*"
    )
    
    $files = Get-ChildItem $folderPath -File
    
    foreach ($file in $files) {
        $fileNorm = $file.FullName.Replace('/', '\')
        
        # Check if Protected
        if ($allProtected -contains $fileNorm) {
            continue
        }
        
        # Check Patterns
        $matchesPattern = $false
        foreach ($pat in $pats) {
            if ($file.Name -like $pat) {
                $matchesPattern = $true
                break
            }
        }
        
        # Strict Name Matching
        if (-not $matchesPattern) {
            $bn = $file.BaseName.ToLower().Trim()
            $fn = $firstName.ToLower()
            $ln = $lastName.ToLower()
            
            if ($bn -eq "${fn}_${ln}" -or 
                $bn -eq "${ln}_${fn}" -or 
                $bn -eq "${fn}${ln}" -or 
                $bn -eq "${fn} ${ln}") {
                $matchesPattern = $true
            }
        }
        
        if ($matchesPattern) {
            Write-Host "Deleting duplicate portrait [$key]: $($file.Name)"
            Remove-Item $file.FullName -Force
        }
    }
}
