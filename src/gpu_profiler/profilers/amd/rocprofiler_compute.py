import subprocess
import os
import logging
import hydra


class RocprofilerCompute():

    def run_all(command, cfg):
        result_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
        output = ''
        running_command = ['rocprof-compute', 'profile', '-p', result_dir, '--name', command[0], '--'] + command
        logging.info(f'Running rocprofiler_compute')
        if cfg.dry_run:
            logging.info(' '.join(running_command))
        else:
            output += subprocess.run(running_command, capture_output=True)

        output_file_path = os.path.join(result_dir, 'output_rocprofiler_compute.txt')
        logging.info(f'Writing output of rocprofiler_compute to {output_file_path}')
        if not cfg.dry_run:
            with open(output_file_path) as output_file:
                output_file.writelines(output)

