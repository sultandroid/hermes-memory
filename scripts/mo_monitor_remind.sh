#!/bin/bash
# Wrapper for the "تذكير بصرف المواد" cron job.
# Runs mo_monitor.py in 'remind' mode and delivers its stdout verbatim.
exec /opt/homebrew/bin/python3 /Users/mohamedessa/.hermes/scripts/mo_monitor.py remind
