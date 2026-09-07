param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$indexPath = Join-Path $ProjectRoot 'index.html'
$html = [IO.File]::ReadAllText($indexPath)
$match = [regex]::Match(
    $html,
    'const DATA=(\[.*?\]);\s*const LABELS=',
    [Text.RegularExpressions.RegexOptions]::Singleline
)

if (-not $match.Success) {
    throw 'Unable to find the DATA array in index.html.'
}

$rows = $match.Groups[1].Value | ConvertFrom-Json
$imageDirectory = Join-Path $ProjectRoot 'image'

foreach ($row in $rows) {
    $localImage = Get-ChildItem -LiteralPath $imageDirectory -File |
        Where-Object { $_.BaseName -eq $row.id -and $_.Extension -match '^\.(png|jpe?g|webp)$' } |
        Select-Object -First 1

    if ($localImage) {
        $row.image = 'image/' + $localImage.Name
    }

    $localSourceImage = Get-ChildItem -LiteralPath $imageDirectory -File |
        Where-Object { $_.BaseName -eq ($row.id + '-source') -and $_.Extension -match '^\.(png|jpe?g|webp)$' } |
        Select-Object -First 1

    if ($localSourceImage -and $row.PSObject.Properties.Name -contains 'sourceImage') {
        $row.sourceImage = 'image/' + $localSourceImage.Name
    }
}

$json = $rows | ConvertTo-Json -Depth 20 -Compress
$replacement = 'const DATA=' + $json + ';' + [Environment]::NewLine + 'const LABELS='
$optimized = $html.Substring(0, $match.Index) + $replacement + $html.Substring($match.Index + $match.Length)

$utf8NoBom = [Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText($indexPath, $optimized, $utf8NoBom)

Write-Host ('Optimized index.html: {0:N2} MB -> {1:N2} MB' -f ($html.Length / 1MB), ($optimized.Length / 1MB))
