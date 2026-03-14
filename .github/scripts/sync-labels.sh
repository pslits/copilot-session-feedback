#!/usr/bin/env bash
# sync-labels.sh — create or update all HITL labels defined in docs/hitl/labels.md.
#
# Usage:
#   ./.github/scripts/sync-labels.sh [--repo OWNER/REPO] [--delete-unlisted]
#
# Requirements: gh CLI authenticated (gh auth login).
#
# By default the script only creates/updates labels; it does NOT delete anything.
# Pass --delete-unlisted to also remove labels whose names start with
# state:, risk:, event:, or decision: but are not in this taxonomy.

set -euo pipefail

# ── Parse args ────────────────────────────────────────────────────────────────
REPO=""
DELETE_UNLISTED=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)           REPO="$2"; shift 2 ;;
    --delete-unlisted) DELETE_UNLISTED=true; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

REPO_FLAG=""
[[ -n "$REPO" ]] && REPO_FLAG="--repo $REPO"

# ── Label definitions (name|color|description) ────────────────────────────────
# Colours are hex without the leading #.
LABELS=(
  # State
  "state:intake|BFD4F2|Issue submitted; awaiting completeness triage."
  "state:triage|E4E669|Being reviewed for completeness and risk classification."
  "state:awaiting-human|F9A825|Blocked on a human approve/reject decision."
  "state:approved|0E8A16|Approved by an authorized human; execution may proceed."
  "state:rejected|B60205|Rejected by an authorized human; execution must not proceed."
  "state:executing|1D76DB|Approved action is actively in progress."
  "state:postmortem|5319E7|Action complete; post-intervention outcome documentation required."
  "state:closed|CCCCCC|All documentation complete; issue closed."
  # Event
  "event:need-info|FEF2C0|Reviewer has requested additional information from requester."
  "event:escalated|E99695|SLA breach or elevated risk triggered an escalation."
  # Risk
  "risk:low|C2E0C6|Impact is bounded and easily reversible."
  "risk:medium|FEF2C0|Moderate impact; rollback is well-defined."
  "risk:high|F9A825|Significant impact; rollback is complex or time-consuming."
  "risk:critical|B60205|Potentially irreversible or wide-blast-radius impact."
  # Decision
  "decision:accepted|0E8A16|Action was accepted and approved."
  "decision:rejected|B60205|Action was rejected with documented rationale."
  "decision:deferred|BFD4F2|Decision postponed pending additional information or conditions."
)

# ── Sync ──────────────────────────────────────────────────────────────────────
echo "Syncing HITL labels…"

TAXONOMY_NAMES=()

for entry in "${LABELS[@]}"; do
  IFS='|' read -r name color description <<< "$entry"
  TAXONOMY_NAMES+=("$name")

  # Check if label already exists
  if gh label list $REPO_FLAG --json name --jq '.[].name' | grep -qx "$name"; then
    echo "  UPDATE  $name"
    gh label edit "$name" $REPO_FLAG \
      --color "$color" \
      --description "$description"
  else
    echo "  CREATE  $name"
    gh label create "$name" $REPO_FLAG \
      --color "$color" \
      --description "$description"
  fi
done

# ── Optional: delete unlisted HITL labels ─────────────────────────────────────
if [[ "$DELETE_UNLISTED" == true ]]; then
  echo ""
  echo "Checking for unlisted HITL labels to delete…"
  while IFS= read -r existing; do
    if [[ "$existing" =~ ^(state:|risk:|event:|decision:) ]]; then
      listed=false
      for t in "${TAXONOMY_NAMES[@]}"; do
        [[ "$t" == "$existing" ]] && listed=true && break
      done
      if [[ "$listed" == false ]]; then
        echo "  DELETE  $existing"
        gh label delete "$existing" $REPO_FLAG --yes
      fi
    fi
  done < <(gh label list $REPO_FLAG --json name --jq '.[].name')
fi

echo ""
echo "Done. ${#LABELS[@]} labels synced."
