$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$gameRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $project))
$releases = Join-Path $gameRoot 'Releases'
$subs = Join-Path $releases 'SUB RELEASES'
$oldOfficial = Join-Path $releases 'CrazyAuto-4'
$oldArchive = Join-Path $subs '4-Official-Front-Faces-Stay-Put'
$subrelease = Join-Path $subs '5.1-Spring-and-Smoke'
$newOfficial = Join-Path $releases 'CrazyAuto-5'
$skill = Join-Path $env:USERPROFILE '.codex\skills\crazykids-car-engine'

foreach ($path in @($releases, $subs, $oldOfficial, $project, $skill)) {
  if (-not (Test-Path -LiteralPath $path)) { throw "Required path missing: $path" }
}
foreach ($path in @($oldArchive, $subrelease, $newOfficial)) {
  if (Test-Path -LiteralPath $path) { throw "Refusing to overwrite existing release: $path" }
}

Move-Item -LiteralPath $oldOfficial -Destination $oldArchive
$html = Join-Path $subrelease 'HTML GAME DATA'
$google = Join-Path $subrelease 'GOOGLE PUBLISH VER'
$notes = Join-Path $subrelease 'UPDATE NOTES'
New-Item -ItemType Directory -Path $html,$google,$notes -Force | Out-Null

$playable = Join-Path $html 'Playable-Web'
New-Item -ItemType Directory -Path $playable | Out-Null
Copy-Item -Path (Join-Path $project 'dist\*') -Destination $playable -Recurse -Force

$source = Join-Path $html 'Rebuildable-Source'
New-Item -ItemType Directory -Path $source | Out-Null
Get-ChildItem -LiteralPath $project -Force | Where-Object { $_.Name -notin @('node_modules','dist','.git','qa') } | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination $source -Recurse -Force
}

Copy-Item -LiteralPath (Join-Path $project 'apps-script\Code.gs') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\appsscript.json') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\Index.html') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\README.md') -Destination $google
Copy-Item -LiteralPath (Join-Path $project 'apps-script\PUBLISH-AFTER-CLASS.ps1') -Destination $google

Copy-Item -LiteralPath (Join-Path $project 'docs\references\PHYSICS-5.1-BRAKING-SUSPENSION.md') -Destination $notes
Copy-Item -LiteralPath (Join-Path $project 'docs\releases\UPDATE-LOG.md') -Destination $notes
Copy-Item -LiteralPath (Join-Path $project 'docs\releases\RELEASE-INDEX.md') -Destination $notes
$skillCopy = Join-Path $notes 'AI-Skill\crazykids-car-engine'
New-Item -ItemType Directory -Path (Split-Path -Parent $skillCopy) -Force | Out-Null
Copy-Item -LiteralPath $skill -Destination $skillCopy -Recurse -Force

$history = Join-Path $html 'Release-History'
New-Item -ItemType Directory -Path $history | Out-Null
$lines = @('# Preserved release checkpoints', '', 'All earlier packages remain in the neighboring `Releases/SUB RELEASES/` tree. Their full ZIPs are not recopied into each cumulative release, avoiding nested duplicate archives.', '', '| Release folder | Location from `Releases/` |')
Get-ChildItem -LiteralPath $subs -Directory | Where-Object { $_.FullName -ne $subrelease } | Sort-Object Name | ForEach-Object {
  $lines += "| $($_.Name) | SUB RELEASES/$($_.Name)/ |"
}
Set-Content -LiteralPath (Join-Path $history 'README.md') -Value ($lines -join "`n") -Encoding utf8

$tempGoogle = Join-Path $env:TEMP 'CrazyAuto-5.1-Google-Apps-Script.zip'
if (Test-Path -LiteralPath $tempGoogle) { Remove-Item -LiteralPath $tempGoogle -Force }
Compress-Archive -Path (Join-Path $google '*') -DestinationPath $tempGoogle -CompressionLevel Optimal
Copy-Item -LiteralPath $tempGoogle -Destination (Join-Path $google 'CrazyAuto-5.1-Google-Apps-Script.zip')

$tempComplete = Join-Path $env:TEMP 'CrazyAuto-5.1-Complete.zip'
if (Test-Path -LiteralPath $tempComplete) { Remove-Item -LiteralPath $tempComplete -Force }
Compress-Archive -Path (Join-Path $subrelease '*') -DestinationPath $tempComplete -CompressionLevel Optimal
Copy-Item -LiteralPath $tempComplete -Destination (Join-Path $html 'CrazyAuto-5.1-Complete.zip')

Copy-Item -LiteralPath $subrelease -Destination $newOfficial -Recurse -Force
Copy-Item -LiteralPath $tempComplete -Destination (Join-Path $newOfficial 'HTML GAME DATA\CrazyAuto-5-Complete.zip')

$releaseReadme = @'
# CrazyAuto releases

`CrazyAuto-5/` is the current official major release, built from subrelease 5.1 **Spring & Smoke**. Official releases use whole major numbers only. Decimal updates are retained in `SUB RELEASES/`.

Each release folder has exactly three top-level folders: `HTML GAME DATA`, `GOOGLE PUBLISH VER`, and `UPDATE NOTES`. Earlier source checkpoints and packages remain intact under `SUB RELEASES/`; the current release includes a `Release-History/README.md` index to those archives without duplicating nested ZIPs.

The previous official major 4 package was moved intact to `SUB RELEASES/4-Official-Front-Faces-Stay-Put/`. Prior decimal releases remain alongside it.
'@
Set-Content -LiteralPath (Join-Path $releases 'README.md') -Value $releaseReadme -Encoding utf8
