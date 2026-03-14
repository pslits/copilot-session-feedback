# sync-labels.ps1 — create or update all HITL labels defined in docs/hitl/labels.md.
#
# Usage:
#   .\..\scripts\sync-labels.ps1 [-Repo OWNER/REPO] [-DeleteUnlisted] [-DryRun]
#
# Requirements: gh CLI authenticated (gh auth login).
#
# By default the script only creates/updates labels.
# Pass -DeleteUnlisted to also remove labels whose names start with
# state:, risk:, event:, or decision: but are not in this taxonomy.
# Pass -DryRun to print what would happen without making any changes.

param(
    [string] $Repo = "",
    [switch] $DeleteUnlisted,
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoFlag = @()
if ($Repo) { $RepoFlag = @('--repo', $Repo) }

# ── Label definitions ─────────────────────────────────────────────────────────
$Labels = @(
    # State
    [pscustomobject]@{ Name = 'state:intake'; Color = 'BFD4F2'; Description = 'Issue submitted; awaiting completeness triage.' }
    [pscustomobject]@{ Name = 'state:triage'; Color = 'E4E669'; Description = 'Being reviewed for completeness and risk classification.' }
    [pscustomobject]@{ Name = 'state:awaiting-human'; Color = 'F9A825'; Description = 'Blocked on a human approve/reject decision.' }
    [pscustomobject]@{ Name = 'state:approved'; Color = '0E8A16'; Description = 'Approved by an authorized human; execution may proceed.' }
    [pscustomobject]@{ Name = 'state:rejected'; Color = 'B60205'; Description = 'Rejected by an authorized human; execution must not proceed.' }
    [pscustomobject]@{ Name = 'state:executing'; Color = '1D76DB'; Description = 'Approved action is actively in progress.' }
    [pscustomobject]@{ Name = 'state:postmortem'; Color = '5319E7'; Description = 'Action complete; post-intervention outcome documentation required.' }
    [pscustomobject]@{ Name = 'state:closed'; Color = 'CCCCCC'; Description = 'All documentation complete; issue closed.' }
    # Event
    [pscustomobject]@{ Name = 'event:need-info'; Color = 'FEF2C0'; Description = 'Reviewer has requested additional information from requester.' }
    [pscustomobject]@{ Name = 'event:escalated'; Color = 'E99695'; Description = 'SLA breach or elevated risk triggered an escalation.' }
    # Risk
    [pscustomobject]@{ Name = 'risk:low'; Color = 'C2E0C6'; Description = 'Impact is bounded and easily reversible.' }
    [pscustomobject]@{ Name = 'risk:medium'; Color = 'FEF2C0'; Description = 'Moderate impact; rollback is well-defined.' }
    [pscustomobject]@{ Name = 'risk:high'; Color = 'F9A825'; Description = 'Significant impact; rollback is complex or time-consuming.' }
    [pscustomobject]@{ Name = 'risk:critical'; Color = 'B60205'; Description = 'Potentially irreversible or wide-blast-radius impact.' }
    # Decision
    [pscustomobject]@{ Name = 'decision:accepted'; Color = '0E8A16'; Description = 'Action was accepted and approved.' }
    [pscustomobject]@{ Name = 'decision:rejected'; Color = 'B60205'; Description = 'Action was rejected with documented rationale.' }
    [pscustomobject]@{ Name = 'decision:deferred'; Color = 'BFD4F2'; Description = 'Decision postponed pending additional information or conditions.' }
)

# ── Fetch existing label names once ───────────────────────────────────────────
if ($DryRun) { Write-Host "[DRY RUN] No changes will be made.`n" -ForegroundColor Cyan }
Write-Host "Syncing HITL labels..."
$Existing = (gh label list @RepoFlag --json name --jq '.[].name' 2>$null) -split "`n" |
Where-Object { $_ -ne '' }

$TaxonomyNames = $Labels | Select-Object -ExpandProperty Name

foreach ($label in $Labels) {
    if ($Existing -contains $label.Name) {
        Write-Host "  UPDATE  $($label.Name)  (#$($label.Color))"
        if (-not $DryRun) {
            gh label edit $label.Name @RepoFlag `
                --color $label.Color `
                --description $label.Description
        }
    }
    else {
        Write-Host "  CREATE  $($label.Name)  (#$($label.Color))"
        if (-not $DryRun) {
            gh label create $label.Name @RepoFlag `
                --color $label.Color `
                --description $label.Description
        }
    }
}

# ── Optional: delete unlisted HITL labels ─────────────────────────────────────
if ($DeleteUnlisted) {
    Write-Host ""
    Write-Host "Checking for unlisted HITL labels to delete..."
    $prefixes = @('state:', 'risk:', 'event:', 'decision:')
    foreach ($name in $Existing) {
        $isHitl = $prefixes | Where-Object { $name.StartsWith($_) }
        if ($isHitl -and ($TaxonomyNames -notcontains $name)) {
            Write-Host "  DELETE  $name"
            if (-not $DryRun) {
                gh label delete $name @RepoFlag --yes
            }
        }
    }
}

Write-Host ""
Write-Host "Done. $($Labels.Count) labels synced."
