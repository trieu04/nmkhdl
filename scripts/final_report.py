#!/usr/bin/env python
"""Phase L: Final report — aggregate top results, write summary markdown."""
import json
from pathlib import Path
import csv

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.experiment import ExperimentLogger


def generate_final_report():
    """Aggregate results and write to REPORT.md."""
    
    log_csv = Path("experiments/log.csv")
    if not log_csv.exists():
        print("ERROR: experiments/log.csv not found")
        return
    
    # Parse CSV manually (no pandas)
    rows = []
    with open(log_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['mean_macroF1'] = float(row['mean_macroF1'])
                rows.append(row)
            except ValueError:
                pass
    
    # Get top 3 per phase
    report = "# Final ML Pipeline Report\n\n"
    report += "## Overview\n"
    report += f"Total runs: {len(rows)}\n"
    baseline_f1 = next((r['mean_macroF1'] for r in rows if r['name']=='B01_baseline'), None)
    report += f"Baseline (B01): {baseline_f1}\n\n"
    
    # Top 10 overall
    report += "## Top 10 Overall\n"
    top10 = sorted(rows, key=lambda r: r['mean_macroF1'], reverse=True)[:10]
    report += "| phase | name | F1 | ± |\n|---|---|---|---|\n"
    for r in top10:
        report += f"| {r['phase']} | {r['name']} | {r['mean_macroF1']} | {r['std_macroF1']} |\n"
    report += "\n"
    
    # Best per phase
    report += "## Best per Phase\n"
    phases = sorted(set(r['phase'] for r in rows))
    for phase in phases:
        phase_rows = [r for r in rows if r['phase'] == phase]
        if not phase_rows:
            continue
        best = max(phase_rows, key=lambda r: r['mean_macroF1'])
        report += f"- **{phase}**: {best['name']} = {best['mean_macroF1']} ± {best['std_macroF1']}\n"
    report += "\n"
    
    # Key insights
    report += "## Key Insights\n"
    best_overall = max(rows, key=lambda r: r['mean_macroF1'])
    baseline_rows = [r for r in rows if r['phase']=='B']
    baseline = max(baseline_rows, key=lambda r: r['mean_macroF1'])['mean_macroF1'] if baseline_rows else 0
    if baseline:
        gain = best_overall['mean_macroF1'] - baseline
        report += f"- **Best model**: {best_overall['name']} (phase {best_overall['phase']}) = {best_overall['mean_macroF1']}\n"
        report += f"- **Absolute gain**: +{gain:.4f} (+{100*gain/baseline:.1f}% from phase B)\n"
        report += f"- **Winning approach**: {best_overall['notes']}\n\n"
    
    report += "## Recommendations\n"
    report += "1. Deploy best model with rotation-only augmentation (no jitter/scale)\n"
    report += "2. Use ResNet1D or BiLSTM architecture for inference\n"
    report += "3. Apply softmax entropy for open-set detection (AUROC ~0.7-0.8)\n"
    report += "4. Monitor per-activity accuracy in production\n\n"
    
    # Write to file
    report_path = Path("FINAL_REPORT.md")
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"✅ Final report written to {report_path}")
    print(report)


def main():
    generate_final_report()
    
    # Log as Phase L
    logger = ExperimentLogger(
        name="L_final_report",
        phase="L",
        config={},
        notes="Final report generated"
    )
    logger.set_metric("mean_macroF1", 0.0)  # Dummy metric
    logger.__exit__(None, None, None)


if __name__ == "__main__":
    main()
