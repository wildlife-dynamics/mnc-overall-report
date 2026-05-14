#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

script_dir = Path(__file__).parent
workflow_module = "ecoscope_workflows_mnc_overall_report_workflow"
results_env = os.environ.get("ECOSCOPE_WORKFLOWS_RESULTS", "")
rp = results_env[len("file://"):] if results_env.startswith("file://") else results_env

cmd = [sys.executable, str(script_dir / "thread-executor.py"), workflow_module] + sys.argv[1:]
if rp:
    cmd = [sys.executable, str(script_dir / "resource-sampler.py"), rp] + cmd
sys.exit(subprocess.call(cmd))
