$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$releases = Join-Path (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $project))) 'Releases'
$sub = Join-Path $releases 'SUB RELEASES\5.1-Spring-and-Smoke'
$official = Join-Path $releases 'CrazyAuto-5'
$desktopSource = Join-Path (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $project))) 'AI-Game-Demo\Desktop\CrazyAuto-Demo'
$legacyTwo = Join-Path $releases 'SUB RELEASES\CrazyAuto-2.0'
$legacyThree = Join-Path $releases 'SUB RELEASES\CrazyAuto-3.0'
$legacyFour = Join-Path $releases 'SUB RELEASES\4.5-Weight-Shift'
$sourceVersion = Join-Path $project 'VERSION'
$tempZip = Join-Path $env:TEMP 'CrazyAuto-5.1-final.zip'
foreach ($p in @($sub,$official,$desktopSource,$legacyTwo,$legacyThree,$legacyFour,(Join-Path $sub 'HTML GAME DATA\Rebuildable-Source'),(Join-Path $official 'HTML GAME DATA\Rebuildable-Source'))) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Release path missing: $p" }
}
Set-Content -LiteralPath $sourceVersion -Value '5.1.0' -NoNewline
Set-Content -LiteralPath (Join-Path $sub 'HTML GAME DATA\Rebuildable-Source\VERSION') -Value '5.1.0' -NoNewline
Set-Content -LiteralPath (Join-Path $official 'HTML GAME DATA\Rebuildable-Source\VERSION') -Value '5.1.0' -NoNewline

$historyLines = @('# Preserved release checkpoints', '', 'All earlier packages remain in the neighboring `Releases/SUB RELEASES/` tree. Their full ZIPs are not recopied into each cumulative release, avoiding nested duplicate archives.', '', '| Release folder | Location from `Releases/` |')
Get-ChildItem -LiteralPath (Join-Path $releases 'SUB RELEASES') -Directory | Where-Object { $_.Name -ne '5.1-Spring-and-Smoke' } | Sort-Object Name | ForEach-Object {
  $historyLines += "| $($_.Name) | SUB RELEASES/$($_.Name)/ |"
}
$historyLines += @('', '## Best-preserved major builds included here', '', 'These three selected builds are copied into `Refined-Major-Releases/` so the 2.x, 3.x, and 4.x branches are playable from the current release archive.', '', '| Major | Selected build | Selection |', '|---|---|---|', '| 2 | `CrazyAuto-2.0` | Complete preserved desktop Pygame, browser, installer, and Apps Script package. |', '| 3 | `CrazyAuto-3.0` | Complete preserved Pygame, browser, Apps Script, and 3.0 update notes. |', '| 4 | `4.5-Weight-Shift` | Latest preserved 4.x playable/source/GAS build; retains the earlier face, world, steering, and combined-slip work without nesting duplicate 200 MB archives. |')
Set-Content -LiteralPath (Join-Path $sub 'HTML GAME DATA\Release-History\README.md') -Value ($historyLines -join "`n") -Encoding utf8
Set-Content -LiteralPath (Join-Path $official 'HTML GAME DATA\Release-History\README.md') -Value ($historyLines -join "`n") -Encoding utf8

foreach ($base in @($sub,$official)) {
  $sourceTarget = Join-Path $base 'HTML GAME DATA\Rebuildable-Source'
  $qaTarget = Join-Path $sourceTarget 'qa'
  if (Test-Path -LiteralPath $qaTarget) {
    $sourceRoot = (Resolve-Path -LiteralPath $sourceTarget).Path.TrimEnd('\') + '\'
    $resolvedQa = (Resolve-Path -LiteralPath $qaTarget).Path
    if (-not $resolvedQa.StartsWith($sourceRoot,[System.StringComparison]::OrdinalIgnoreCase)) { throw "QA cache cleanup escaped source package: $resolvedQa" }
    Remove-Item -LiteralPath $resolvedQa -Recurse -Force
  }
  Get-ChildItem -LiteralPath $project -Force | Where-Object { $_.Name -notin @('node_modules','dist','.git','qa') } | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $sourceTarget -Recurse -Force
  }
  Set-Content -LiteralPath (Join-Path $sourceTarget 'VERSION') -Value '5.1.0' -NoNewline
  $desktop = Join-Path $base 'HTML GAME DATA\Desktop-Pygame'
  if (-not (Test-Path -LiteralPath $desktop)) { New-Item -ItemType Directory -Path $desktop | Out-Null }
  Get-ChildItem -LiteralPath $desktopSource -Force | Where-Object { $_.Name -notin @('saves','__pycache__','.git','.venv') } | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $desktop -Recurse -Force
  }
  Copy-Item -LiteralPath (Join-Path $project 'docs\references\PHYSICS-5.1-BRAKING-SUSPENSION.md') -Destination (Join-Path $base 'UPDATE NOTES') -Force
  Copy-Item -LiteralPath (Join-Path $project 'docs\releases\UPDATE-LOG.md') -Destination (Join-Path $base 'UPDATE NOTES') -Force
  Copy-Item -LiteralPath (Join-Path $project 'docs\releases\RELEASE-INDEX.md') -Destination (Join-Path $base 'UPDATE NOTES') -Force
  $skillCopy = Join-Path $base 'UPDATE NOTES\AI-Skill\crazykids-car-engine'
  if (-not (Test-Path -LiteralPath $skillCopy)) { New-Item -ItemType Directory -Path $skillCopy -Force | Out-Null }
  Copy-Item -Path (Join-Path $env:USERPROFILE '.codex\skills\crazykids-car-engine\*') -Destination $skillCopy -Recurse -Force

  $refined = Join-Path $base 'HTML GAME DATA\Release-History\Refined-Major-Releases'
  New-Item -ItemType Directory -Path $refined -Force | Out-Null
  foreach ($selection in @(@{Source=$legacyTwo;Name='CrazyAuto-2.0'},@{Source=$legacyThree;Name='CrazyAuto-3.0'})) {
    $target = Join-Path $refined $selection.Name
    New-Item -ItemType Directory -Path $target -Force | Out-Null
    Copy-Item -Path (Join-Path $selection.Source '*') -Destination $target -Recurse -Force
  }
  $v4 = Join-Path $refined 'CrazyAuto-4.5-Weight-Shift'
  foreach ($folder in @('HTML GAME DATA','GOOGLE PUBLISH VER','UPDATE NOTES')) { New-Item -ItemType Directory -Path (Join-Path $v4 $folder) -Force | Out-Null }
  foreach ($folder in @('Playable-Web','Rebuildable-Source')) {
    $to = Join-Path $v4 "HTML GAME DATA\$folder"
    New-Item -ItemType Directory -Path $to -Force | Out-Null
    Copy-Item -Path (Join-Path $legacyFour "HTML GAME DATA\$folder\*") -Destination $to -Recurse -Force
  }
  $v4Google = Join-Path $v4 'GOOGLE PUBLISH VER\Google-Apps-Script'
  New-Item -ItemType Directory -Path $v4Google -Force | Out-Null
  Copy-Item -Path (Join-Path $legacyFour 'GOOGLE PUBLISH VER\Google-Apps-Script\*') -Destination $v4Google -Recurse -Force
  foreach ($note in @('README.md','RELEASE-INDEX.md','UPDATE-LOG.md')) {
    Copy-Item -LiteralPath (Join-Path $legacyFour "UPDATE NOTES\$note") -Destination (Join-Path $v4 'UPDATE NOTES') -Force
  }
  $v4History = @('# CrazyAuto 4.5 retained build', '', 'This curated copy contains the playable web build, rebuildable source, Google Apps Script project, and release notes. The original complete archives remain at `Releases/SUB RELEASES/4.5-Weight-Shift/`; large nested historical ZIPs are not duplicated here.')
  New-Item -ItemType Directory -Path (Join-Path $v4 'HTML GAME DATA\Release-History') -Force | Out-Null
  Set-Content -LiteralPath (Join-Path $v4 'HTML GAME DATA\Release-History\README.md') -Value ($v4History -join "`n") -Encoding utf8
  Set-Content -LiteralPath (Join-Path $v4 'UPDATE NOTES\SELECTION.md') -Value 'Selected as the final preserved 4.x build because 4.5 is the latest 4.x gameplay package and carries the earlier cumulative 4.4/4.41 visual improvements plus steering and combined-slip changes.' -Encoding utf8
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path -LiteralPath $tempZip) { Remove-Item -LiteralPath $tempZip -Force }
$archive = [System.IO.Compression.ZipFile]::Open($tempZip,[System.IO.Compression.ZipArchiveMode]::Create)
try {
  Get-ChildItem -LiteralPath $sub -Recurse -File | Where-Object { $_.Name -notin @('CrazyAuto-5.1-Complete.zip','CrazyAuto-5-Complete.zip') } | ForEach-Object {
    $entry = $_.FullName.Substring($sub.Length).TrimStart('\').Replace('\','/')
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive,$_.FullName,$entry,[System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
  }
} finally { $archive.Dispose() }
Copy-Item -LiteralPath $tempZip -Destination (Join-Path $sub 'HTML GAME DATA\CrazyAuto-5.1-Complete.zip') -Force
Copy-Item -LiteralPath $tempZip -Destination (Join-Path $sub 'HTML GAME DATA\CrazyAuto-5-Complete.zip') -Force
Copy-Item -LiteralPath $tempZip -Destination (Join-Path $official 'HTML GAME DATA\CrazyAuto-5-Complete.zip') -Force
Copy-Item -LiteralPath $tempZip -Destination (Join-Path $official 'HTML GAME DATA\CrazyAuto-5.1-Complete.zip') -Force
