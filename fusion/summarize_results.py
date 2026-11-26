"""Writes fusion_results_summary.csv: the most important columns of fusion_results.csv, one row per method and source.

Run it again after every FUSION_EVALUATION run (python fusion/summarize_results.py); fusion_results.csv stays the full
record.

Columns:
  SSIM_ref, PSNR_ref    closeness to the fog-free frame (higher is better; empty for sources without one, e.g. car)
  hazy_SSIM_ref,        the same scores of the hazy visible input: a method below these recovers nothing measurable
  hazy_PSNR_ref
  Qabf                  edges carried over from the two inputs (higher is better)
  Labf                  information of the inputs lost (lower is better)
  Nabf                  artefacts: edges in the output that neither input has (lower is better)
  SD                    contrast (standard deviation of the output). Not better or worse by itself, but it explains a
                        lot of the other columns: low-contrast outputs score few artefacts and high loss.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
COLUMNS = {'method': 'method', 'source': 'source',
           'SSIM_ref': 'SSIM_ref', 'PSNR_ref': 'PSNR_ref',
           'SSIM_ref_vis': 'hazy_SSIM_ref', 'PSNR_ref_vis': 'hazy_PSNR_ref',
           'Qabf': 'Qabf', 'Labf': 'Labf', 'Nabf': 'Nabf', 'SD': 'SD'}


def main():
    results = pd.read_csv(HERE / 'fusion_results.csv')
    summary = results[[c for c in COLUMNS if c in results.columns]].rename(columns=COLUMNS)
    summary = summary.sort_values(['source', 'SSIM_ref', 'Qabf'], ascending=[True, False, False], na_position='last')
    decimals = {c: 2 if c in ('PSNR_ref', 'hazy_PSNR_ref', 'SD') else 3 for c in summary.columns[2:]}
    summary.round(decimals).to_csv(HERE / 'fusion_results_summary.csv', index=False)
    print('wrote %s (%d rows)' % (HERE / 'fusion_results_summary.csv', len(summary)))


if __name__ == '__main__':
    main()
