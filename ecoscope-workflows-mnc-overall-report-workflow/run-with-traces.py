#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

script_dir = Path(__file__).parent
workflow_module = "ecoscope_workflows_mnc_overall_report_workflow"


def _file_uri_to_path(uri):
    if not uri.startswith("file://"):
        return uri
    path = uri[7:]
    if len(path) > 2 and path[0] == "/" and path[2] == ":":
        path = path[1:]
    return path


results_env = os.environ.get("ECOSCOPE_WORKFLOWS_RESULTS", "")
rp = _file_uri_to_path(results_env) if results_env else ""

env = os.environ.copy()
if results_env and rp != results_env:
    env["ECOSCOPE_WORKFLOWS_RESULTS"] = rp

cmd = [sys.executable, str(script_dir / "thread-executor.py"), workflow_module] + sys.argv[1:]
if rp:
    cmd = [sys.executable, str(script_dir / "resource-sampler.py"), rp] + cmd
sys.exit(subprocess.call(cmd, env=env))
