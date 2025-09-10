# GPU Profiling tool

This tool uses a collection of GPU kernel profiling tools to generate a detailed analysis.

### Usage

Install with `pip install .`
Run with `gpu_profiler`

The config folder contains a config.yaml file that can be edited. The backend specifies which type of GPU and therefore the tools that will be used to profile the compute kernels. The commands are the list of command that will be used with the GPU profilers.

It is possible to override these variables either by modifying the yaml file or by specifying them as a cli argument `gpu_profiler foo.bar=value`. For a detailed explaination refer to the following [documentation](https://hydra.cc/docs/advanced/override_grammar/basic/)

### Development

With your preferred virtual environment, run `pip installed -e .`