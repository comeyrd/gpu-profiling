import subprocess
import os
import logging
import hydra


subtools = [
    ['compute-sanitizer', '--tool', 'memcheck', '--leak-check=full'],
    ['compute-sanitizer', '--tool', 'racecheck'],
    ['compute-sanitizer', '--tool', 'initcheck'],
    ['compute-sanitizer', '--tool', 'synccheck']
]

class ComputeSanitizer:

    def run_all(command, cfg):
        result_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
        output = ''
        for subtool in subtools:
            running_command = subtool + command
            logging.info(f'Running compute sanitizer subtool {subtool[2]}')
            if cfg.dry_run:
                logging.info(' '.join(running_command))
            else:
                output += subprocess.run(running_command, capture_output=True)

        output_file_path = os.path.join(result_dir, 'output_compute_sanitizer.txt')
        logging.info(f'Writing output of all compute sanitizer tools to {output_file_path}')
        if not cfg.dry_run:
            with open(output_file_path) as output_file:
                output_file.writelines(output)
