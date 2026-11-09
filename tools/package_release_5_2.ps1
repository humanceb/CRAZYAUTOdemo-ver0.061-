$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$browser = Split-Path -Parent $project
$demo = Split-Path -Parent $browser
$gameRoot = Split-Path -Parent $demo
$releases = Join-Path $gameRoot 'Releases'
$sub = Join-Path $releases 'SUB RELEASES\5.2-Grip-Before-Glory'
$official = Join-Path $releases 'CrazyAuto-5'
$desktopSource = Join-Path $demo 'Desktop\CrazyAuto-Demo'
$skill = Join-Path $env:USERPROFILE '.codex\skills\crazykids-car-engine'
if (Test-Path -LiteralPath $sub) { throw "Refusing to overwrite retained release: $sub" }
foreach ($path in @($official,$desktopSource,$skill,(Join-Path $project 'dist'),(Join-Path $project 'apps-script\Index.html'))) {
  if (-not (Test-Path -LiteralPath $path)) { throw "Required path missing: $path" }
}
$html = Join-Path $sub 'HTML GAME DATA'; $google = Join-Path $sub 'GOOGLE PUBLISH VER'; $notes = Join-Path $sub 'UPDATE NOTES'
New-Item -ItemType Directory -Path $html,$google,$notes -Force | Out-Null
$playable = Join-Path $html 'Playable-Web'; New-Item -ItemType Directory -Path $playable | Out-Null
Copy-Item -Path (Join-Path $project 'dist\*') -Destination $playable -Recurse -Force
$source = Join-Path $html 'Rebuildable-Source'; New-Item -ItemType Directory -Path $source | Out-Null
Get-ChildItem -LiteralPath $project -Force | Where-Object { $_.Name -notin @('node_modules','dist','.git','qa') } | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $source -Recurse -Force }
Set-Content -LiteralPath (Join-Path $source 'VERSION') -Value '5.2.0' -NoNewline
$desktop = Join-Path $html 'Desktop-Pygame'; New-Item -ItemType Directory -Path $desktop | Out-Null
Get-ChildItem -LiteralPath $desktopSource -Force | Where-Object { $_.Name -notin @('saves','__pycache__','.git','.venv') } | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $desktop -Recurse -Force }
Set-Content -LiteralPath (Join-Path $desktop 'VERSION') -Value '5.2.0' -NoNewline
Copy-Item -LiteralPath (Join-Path $project 'apps-script\Code.gs') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\appsscript.json') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\Index.html') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\README.md') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\PUBLISH-AFTER-CLASS.ps1') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'docs\references\PHYSICS-5.2-GRIP-LED-DRIFT-ENTRY.md') -Destination $notes
Copy-Item -LiteralPath (Join-Path $project 'docs\releases\UPDATE-LOG.md') -Destination $notes
Copy-Item -LiteralPath (Join-Path $project 'docs\releases\RELEASE-INDEX.md') -Destination $notes
$skillCopy = Join-Path $notes 'AI-Skill\crazykids-car-engine'; New-Item -ItemType Directory -Path (Split-Path -Parent $skillCopy) -Force | Out-Null
Copy-Item -LiteralPath $skill -Destination $skillCopy -Recurse -Force
$history = Join-Path $html 'Release-History'; New-Item -ItemType Directory -Path $history | Out-Null
$lines = @('# Preserved release checkpoints','','All earlier releases remain in `Releases/SUB RELEASES/`. This 5.2 package is cumulative; earlier source checkpoints and complete packages are not overwritten.','','| Release | Location |')
Get-ChildItem -LiteralPath (Join-Path $releases 'SUB RELEASES') -Directory | Sort-Object Name | ForEach-Object { $lines += "| $($_.Name) | SUB RELEASES/$($_.Name)/ |" }
Set-Content -LiteralPath (Join-Path $history 'README.md') -Value ($lines -join "`n") -Encoding utf8
$tempGoogle = Join-Path $env:TEMP 'CrazyAuto-5.2-Google-Apps-Script.zip'; if (Test-Path $tempGoogle) { Remove-Item $tempGoogle -Force }
Compress-Archive -Path (Join-Path $google '*') -DestinationPath $tempGoogle -CompressionLevel Optimal
Copy-Item -LiteralPath $tempGoogle -Destination (Join-Path $google 'CrazyAuto-5.2-Google-Apps-Script.zip')
$tempComplete = Join-Path $env:TEMP 'CrazyAuto-5.2-Complete.zip'; if (Test-Path $tempComplete) { Remove-Item $tempComplete -Force }
Compress-Archive -Path (Join-Path $sub '*') -DestinationPath $tempComplete -CompressionLevel Optimal
Copy-Item -LiteralPath $tempComplete -Destination (Join-Path $html 'CrazyAuto-5.2-Complete.zip')
foreach ($folder in @('HTML GAME DATA','GOOGLE PUBLISH VER','UPDATE NOTES')) { Copy-Item -Path (Join-Path $sub $folder) -Destination $official -Recurse -Force }
Copy-Item -LiteralPath $tempComplete -Destination (Join-Path $official 'HTML GAME DATA\CrazyAuto-5-Complete.zip') -Force
Copy-Item -LiteralPath $tempComplete -Destination (Join-Path $official 'HTML GAME DATA\CrazyAuto-5.2-Complete.zip') -Force
Write-Host "Packaged CrazyAuto 5.2 and refreshed official CrazyAuto-5. Previous 5.1 package remains preserved."
