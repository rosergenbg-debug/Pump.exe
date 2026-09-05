[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$SourceBase = 'https://raw.githubusercontent.com/rosergenbg-debug/Pump.exe/main/tools/global-codex-skills'
$SkillRoot = Join-Path $HOME '.agents\skills'
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$GlobalAgentsPath = Join-Path $CodexHome 'AGENTS.md'

$Skills = @(
    'skill-orchestrator',
    'core-engineering-discipline',
    'core-systematic-debugging',
    'core-tdd-review',
    'core-verification'
)

function Get-RemoteText([string]$Url) {
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing
    return [string]$response.Content
}

function Write-Utf8NoBom([string]$Path, [string]$Text) {
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $utf8NoBom)
}

Write-Host 'Installing Serge global Codex skill system...'
New-Item -ItemType Directory -Path $SkillRoot -Force | Out-Null
New-Item -ItemType Directory -Path $CodexHome -Force | Out-Null

foreach ($skill in $Skills) {
    $url = "$SourceBase/$skill/SKILL.md"
    $targetDir = Join-Path $SkillRoot $skill
    $targetFile = Join-Path $targetDir 'SKILL.md'
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    $content = Get-RemoteText $url
    Write-Utf8NoBom $targetFile $content
    Write-Host "  installed: $skill"
}

$snippet = Get-RemoteText "$SourceBase/GLOBAL_AGENTS_SNIPPET.md"
$beginMarker = '<!-- SERGE_GLOBAL_SKILL_POLICY_BEGIN -->'
$endMarker = '<!-- SERGE_GLOBAL_SKILL_POLICY_END -->'

if (Test-Path $GlobalAgentsPath) {
    $existing = [System.IO.File]::ReadAllText($GlobalAgentsPath)
    $pattern = '(?s)' + [regex]::Escape($beginMarker) + '.*?' + [regex]::Escape($endMarker)

    if ([regex]::IsMatch($existing, $pattern)) {
        $merged = [regex]::Replace($existing, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $snippet }, 1)
    } else {
        $merged = $existing.TrimEnd() + "`r`n`r`n" + $snippet.Trim() + "`r`n"
    }
} else {
    $merged = $snippet.Trim() + "`r`n"
}

Write-Utf8NoBom $GlobalAgentsPath $merged

Write-Host ''
Write-Host 'Done.'
Write-Host "Global skills: $SkillRoot"
Write-Host "Global instructions: $GlobalAgentsPath"
Write-Host 'Codex should detect skill changes automatically. If they do not appear in the current session, start a new Codex session or restart Codex.'
