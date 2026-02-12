# Populate Tier 2 placeholders using `populate_placeholders.ps1`

$scriptPath = "D:\history of id course\populate_placeholders.ps1"

# 11. Max Bill
& $scriptPath -DesignerFolder "bill" -Works @(
    "Kitchen Clock", "Pavilion Sculpture", "Typography", "Ulm School", "Triangular Structure", "Endless Ribbon", "Stackable Chair", "Sun Lamp", "Junghans Wall Clock", "Ulm Stool"
)

# 12. Wilhelm Wagenfeld
& $scriptPath -DesignerFolder "wagenfeld" -Works @(
    "Portrait", "Bauhaus Lamp", "Kubus", "WMF Ash Tray", "Salt and Pepper Shakers", "Tea Service", "Egg Coddler", "Max and Moritz", "Wagenfeld Teapot", "Glassware"
)

# 13. Marianne Brandt
& $scriptPath -DesignerFolder "brandt" -Works @(
    "Portrait", "Tea Infuser", "Kandem Lamp", "Ashtray", "Bauhaus Metalwork", "Coffee and Tea Set", "Ceiling Lamp", "Desk Lamp", "Bowl", "Geometric Teapot"
)
