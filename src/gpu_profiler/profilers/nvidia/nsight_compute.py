import subprocess
import os
import logging
import hydra


class NsightCompute():

    def run_all(command, cfg):
        result_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
        output = ''
        # TODO: Set graph-profiling mode to graph to profile entire graphs as one workload if needed
        # TODO: look at how sections and sets of counters are defined to enable all counters
        running_command = ['ncu', '-o', 'profile', '--export', result_dir] + command
        logging.info(f'Running Nsight Compute')
        if cfg.dry_run:
            logging.info(' '.join(running_command))
        else:
            output += subprocess.run(running_command, capture_output=True)

        output_file_path = os.path.join(result_dir, 'output_nsight_compute.txt')
        logging.info(f'Writing output of nsight compute to {output_file_path}')
        if not cfg.dry_run:
            with open(output_file_path) as output_file:
                output_file.writelines(output)

