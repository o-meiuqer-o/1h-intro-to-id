$path = "D:\history of id course\index.html"
$content = Get-Content $path -Raw

# 1. Level 1 Injection
# Insert Start Tag before v-pillars-grid
# Insert End Tag before the closing of v-level-1 (marked by <!-- LEVEL 2)
Write-Host "Injecting Level 1 wrappers..."

# Pattern: (<div class="v-pillars-grid">)
# Replace: <div class="v-scrollable-body">$1
$content = $content -replace '(<div class="v-pillars-grid">)', '<div class="v-scrollable-body">$1'

# Pattern: (</div>)(\s*<!-- LEVEL 2)
# Replace: $1</div>$2
# Note: The $1 captures the closing div of the Level 1 container.
# We want to insert </div> BEFORE it.
# So: </div>$1$2 ? No.
# Existing: ... content ... </div> <!-- LEVEL 2 -->
# We want: ... content ... </div> </div> <!-- LEVEL 2 -->
# The captured </div> IS the closing of v-level-1.
# So we want to insert our closing </div> BEFORE it.
# So: replace '(\s*</div>\s*<!-- LEVEL 2)' with '</div>$1'
# Wait. '</div>' matches the existing one.
# If I do '</div>$1', I get '</div></div>...'.
# Yes.
$content = [regex]::Replace($content, '(\s*</div>\s*<!-- LEVEL 2)', '`n</div>$1')


# 2. Level 2 Injection
# Insert Start Tag before v-analysis-grid
# Insert End Tag after v-principles-full closing
Write-Host "Injecting Level 2 wrappers..."

# Pattern: (<div class="v-analysis-grid">)
# Replace: <div class="v-scrollable-body">$1
$content = $content -replace '(<div class="v-analysis-grid">)', '<div class="v-scrollable-body">$1'

# Closing L2
# Find v-principles-full and its closing div.
# Pattern: (<div class="v-principles-full">.*?</div>)(\s*</div>) <-- The last div is v-level-2 close
# Regex must be greedy for content inside principles?
# '(?s)(<div class="v-principles-full">.*?</div>)(\s*</div>)'
# But principles full might have nested divs? Yes (paragraphs don't nest divs usually, but dangerous).
# Better: Find the closing div of v-level-2.
# It is followed by </div> (modal-scroll) then </div> (modal-wrap).
# Start looking from v-principles-full.
# Pattern: '(?s)(<div class="v-principles-full">.*?)(\s*</div>\s*</div>\s*</div>\s*<div)'
# Insert </div> before captured group 2?
# The group 2 starts with closing of div level 2?
# Let's trust that v-level-2 is followed by </div></div>.
# Pattern: '(\s*</div>)(\s*</div>\s*</div>\s*<div)'
# Capture 1 is v-level-2 closing.
# Replace: </div>$1$2

$content = [regex]::Replace($content, '(?s)(<div class="v-principles-full">.*?)(\s*</div>\s*</div>\s*</div>)', '$1`n</div>$2')

Set-Content $path $content -Encoding UTF8
Write-Host "Done."
