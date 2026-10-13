"""Run reproducible local Lighthouse audits without adding a frontend runtime."""

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(args):
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if args.chrome:
        env["CHROME_PATH"] = str(Path(args.chrome).resolve())
    results = []
    for name, route in [("home", "/"), ("case", "/projetos/glados-assitente-ti")]:
        for mode in ["desktop", "mobile"]:
            destination = output / f"lighthouse-{name}-{mode}"
            command = [
                args.node,
                args.lighthouse,
                args.base_url.rstrip("/") + route,
                "--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage",
                "--output=json",
                "--output=html",
                f"--output-path={destination}",
                "--quiet",
            ]
            if mode == "desktop":
                command.append("--preset=desktop")
            subprocess.run(command, env=env, check=True, timeout=180)
            report = json.loads(destination.with_suffix(".report.json").read_text())
            if report.get("runtimeError"):
                raise RuntimeError(report["runtimeError"])
            results.append(
                {
                    "page": name,
                    "mode": mode,
                    "url": report["finalDisplayedUrl"],
                    "lighthouse_version": report["lighthouseVersion"],
                    "scores": {
                        key: round(value["score"] * 100)
                        for key, value in report["categories"].items()
                    },
                    "metrics": {
                        key: {
                            "value": report["audits"][key].get("numericValue"),
                            "display": report["audits"][key].get("displayValue"),
                        }
                        for key in [
                            "first-contentful-paint",
                            "largest-contentful-paint",
                            "cumulative-layout-shift",
                            "total-blocking-time",
                            "speed-index",
                        ]
                    },
                    "throttling": report["configSettings"]["throttling"],
                }
            )
            summary = {
                "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
                "scope": "Local laboratory; field INP is not measured.",
                "results": results,
            }
            (output / "summary.json").write_text(
                json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
            )
            print(name, mode, results[-1]["scores"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    parser.add_argument("--node", default="node")
    parser.add_argument("--lighthouse", required=True, help="Path to lighthouse/cli/index.js")
    parser.add_argument("--chrome", help="Optional path to Chromium executable")
    parser.add_argument("--output", default="test-results/lighthouse")
    run(parser.parse_args())
