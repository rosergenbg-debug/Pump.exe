[CmdletBinding()]
param(
    [switch]$SkipPluginEval
)

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

function Invoke-External([string]$Exe, [string[]]$Arguments) {
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed ($LASTEXITCODE): $Exe $($Arguments -join ' ')"
    }
}

function Install-OfficialPluginEvalCli {
    if ($SkipPluginEval) {
        Write-Host '  Plugin Eval: skipped by -SkipPluginEval'
        return $false
    }

    $node = Get-Command node -ErrorAction SilentlyContinue
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    $git = Get-Command git -ErrorAction SilentlyContinue

    if (-not $node -or -not $npm -or -not $git) {
        Write-Warning 'Plugin Eval CLI not installed: Node.js >=20, npm, and Git are required. Core skills were still updated.'
        return $false
    }

    $nodeVersionText = (& $node.Source --version).Trim()
    $nodeMajor = 0
    try {
        $nodeMajor = [int](($nodeVersionText -replace '^v','').Split('.')[0])
    } catch {
        Write-Warning "Plugin Eval CLI not installed: could not parse Node version '$nodeVersionText'."
        return $false
    }

    if ($nodeMajor -lt 20) {
        Write-Warning "Plugin Eval CLI not installed: OpenAI requires Node.js >=20; found $nodeVersionText."
        return $false
    }

    $VendorRoot = Join-Path $HOME '.agents\vendor\openai-plugins'
    $VendorParent = Split-Path -Parent $VendorRoot
    $PluginEvalRoot = Join-Path $VendorRoot 'plugins\plugin-eval'
    New-Item -ItemType Directory -Path $VendorParent -Force | Out-Null

    try {
        if (Test-Path (Join-Path $VendorRoot '.git')) {
            Push-Location $VendorRoot
            try {
                Invoke-External $git.Source @('fetch','--depth','1','origin','main')
                Invoke-External $git.Source @('checkout','main')
                Invoke-External $git.Source @('reset','--hard','origin/main')
                Invoke-External $git.Source @('sparse-checkout','set','plugins/plugin-eval')
            } finally {
                Pop-Location
            }
        } else {
            if (Test-Path $VendorRoot) {
                $backup = "$VendorRoot.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
                Move-Item -Path $VendorRoot -Destination $backup
                Write-Warning "Existing non-Git vendor folder moved to: $backup"
            }
            Invoke-External $git.Source @('clone','--depth','1','--filter=blob:none','--sparse','https://github.com/openai/plugins.git',$VendorRoot)
            Push-Location $VendorRoot
            try {
                Invoke-External $git.Source @('sparse-checkout','set','plugins/plugin-eval')
            } finally {
                Pop-Location
            }
        }

        if (-not (Test-Path (Join-Path $PluginEvalRoot 'package.json'))) {
            throw "Official Plugin Eval checkout is incomplete: $PluginEvalRoot"
        }

        Push-Location $PluginEvalRoot
        try {
            Invoke-External $npm.Source @('link')
        } finally {
            Pop-Location
        }

        $pluginEval = Get-Command plugin-eval -ErrorAction SilentlyContinue
        if (-not $pluginEval) {
            throw 'npm link completed but plugin-eval is not available on PATH.'
        }

        & $pluginEval.Source --help *> $null
        if ($LASTEXITCODE -ne 0) {
            throw 'plugin-eval --help verification failed.'
        }

        Write-Host "  Plugin Eval CLI: installed from official OpenAI source ($PluginEvalRoot)"
        Write-Host '  Plugin Eval policy: static analyze only by default; live benchmark is never automatic.'
        return $true
    } catch {
        Write-Warning "Plugin Eval CLI setup failed without affecting core skills: $($_.Exception.Message)"
        return $false
    }
}

Write-Host 'Updating Serge global Codex skill system...'
New-Item -ItemType Directory -Path $SkillRoot -Force | Out-Null
New-Item -ItemType Directory -Path $CodexHome -Force | Out-Null

foreach ($skill in $Skills) {
    $url = "$SourceBase/$skill/SKILL.md"
    $targetDir = Join-Path $SkillRoot $skill
    $targetFile = Join-Path $targetDir 'SKILL.md'
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    $content = Get-RemoteText $url
    Write-Utf8NoBom $targetFile $content
    Write-Host "  updated: $skill"
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
Write-Host "  updated global policy: $GlobalAgentsPath"

$pluginEvalInstalled = Install-OfficialPluginEvalCli

Write-Host ''
Write-Host 'Done.'
Write-Host "Global skills: $SkillRoot"
Write-Host "Global instructions: $GlobalAgentsPath"
if ($pluginEvalInstalled) {
    Write-Host 'Official Plugin Eval CLI is ready. Automatic policy allows static analysis only; live benchmarks require an explicit request.'
} else {
    Write-Host 'Official Plugin Eval CLI is not active; core skill system remains fully usable.'
}
Write-Host 'Codex Security is managed through the official OpenAI plugin directory and is intentionally not side-loaded by this script.'
Write-Host 'Start a new Codex session or restart Codex if the current session does not reload the updated instructions.'
