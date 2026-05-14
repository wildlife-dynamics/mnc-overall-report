#!/bin/bash
rp="${ECOSCOPE_WORKFLOWS_RESULTS#file://}"
if [ -n "$rp" ]; then
    python3 "$PIXI_PROJECT_ROOT/resource-sampler.py" "$rp" python3 "$PIXI_PROJECT_ROOT/thread-executor.py" "ecoscope_workflows_mnc_overall_report_workflow" "$@"
else
    python3 "$PIXI_PROJECT_ROOT/thread-executor.py" "ecoscope_workflows_mnc_overall_report_workflow" "$@"
fi
exit $?
