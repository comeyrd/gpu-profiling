import hydra
import logging
from omegaconf import DictConfig
from gpu_profiler.profilers.amd.rocprofiler_compute import RocprofilerCompute
from gpu_profiler.profilers.hpctoolkit import HpcToolkit
from gpu_profiler.profilers.nvidia.compute_sanitizer import ComputeSanitizer
from gpu_profiler.profilers.nvidia.nsight_compute import NsightCompute


@hydra.main(version_base=None, config_path='config', config_name='config')
def main(cfg: DictConfig):
    logging.info(f'Using backend: {cfg.backend}')

    for command in cfg.commands:
        command = command.split(' ')
        if cfg.backend == 'amd':
            RocprofilerCompute.run_all(command, cfg)
        elif cfg.backend == 'nvidia':
            NsightCompute.run_all(command, cfg)
            ComputeSanitizer.run_all(command, cfg)
        HpcToolkit.run_all(command, cfg)

