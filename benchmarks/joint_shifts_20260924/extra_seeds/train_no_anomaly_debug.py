"""Run the pinned DCASE trainer without PyTorch's diagnostic backward trace.

This changes only the autograd anomaly-detection flag, which checks backward
operations for NaNs and records stack traces. It does not change the model,
loss, optimizer, data, random seeds, or training hyperparameters.
"""
import runpy
import sys
from pathlib import Path
import torch


def main():
    original = torch.autograd.set_detect_anomaly

    def disable_debug(_requested_mode):
        return original(False)

    torch.autograd.set_detect_anomaly = disable_debug
    print('RUNTIME_OPTIMIZATION: autograd anomaly detection disabled; model math unchanged', flush=True)
    sys.argv[0] = 'train.py'
    sys.path.insert(0, str(Path.cwd()))
    runpy.run_path('train.py', run_name='__main__')


if __name__ == '__main__':
    main()
