#!/bin/bash
# design-tracker-daily-status — no_agent wrapper
# Runs the Design Phase Deliverables Tracker status report and prints it verbatim.
# Delivered as-is by the cron scheduler (no LLM involved).
cd /Users/mohamedessa/aseer-museum-pm || exit 1
exec python3 scripts/design_tracker_overdue.py
