#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rp="${ECOSCOPE_WORKFLOWS_RESULTS#file://}"
if [ -n "$rp" ]; then
    python3 "$SCRIPT_DIR/resource-sampler.py" "$rp" python3 "$SCRIPT_DIR/thread-executor.py" "ecoscope_workflows_mnc_overall_report_workflow" "$@"
else
    python3 "$SCRIPT_DIR/thread-executor.py" "ecoscope_workflows_mnc_overall_report_workflow" "$@"
fi
exit $?
