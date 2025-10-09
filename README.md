Samples of how you could perform memory tracing.

# trace-valgrind.sh

Trace memory using [Valgrind](https://valgrind.org "Valgrind").

- ``-t`` - The temporary file path. Defaults to ``${HOME}/DRAM-Tracing-Samples/temp-trace.log``.
- ``-o`` - The output trace file path. Defaults to ``${HOME}/DRAM-Tracing-Samples/trace-valgrind.stl``.
- ``-s`` - The target command to be traced. Defaults to ``/usr/bin/python3 ${HOME}/DRAM-Tracing-Samples/main.py``.

# trace-pin.sh

Trace memory using [Intel Pin](https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-dynamic-binary-instrumentation-tool.html "Intel Pin").

- ``-p`` - The "pin" executable. Defaults to ``{HOME}/pin/pin``.
- ``-e`` - The pin tracer program executable. Defaults to ``${HOME}/pin/source/tools/SimpleExamples/obj-intel64/pinatrace.so``.
- ``-t`` - The temporary file path. Defaults to ``${HOME}/DRAM-Tracing-Samples/temp-trace.log``.
- ``-o`` - The output trace file path. Defaults to ``${HOME}/DRAM-Tracing-Samples/trace-pin.stl``.
- ``-s`` - The target command to be traced. Defaults to ``/usr/bin/python3 ${HOME}/DRAM-Tracing-Samples/main.py``.

# synthetic.py

Script to generate very basic synthetic data. The synthetic data this produces is very basic and entirely random. You may want to use this as a base and expand it to have more systematic reads and writes at times. For instance, reading and writing to sequential addresses to simulate array reads and writes, rather than entirely random accesses.

- ``-e`` or `--entries` - Number of lines to generate. Defaults to ``1000``.
- ``-m`` or `--megabytes` - Megabytes to generate up to. Defaults to ``4096``.
- ``-r`` or `--read` - Percentage of operations which are reads. Defaults to ``0.9``.
- ``-o`` or `--output` - Output file path. Defaults to ``synthetic.stl``.
- ``-s`` or `--seed` - Random generation seed. Defaults to ``42``.
- ``-l`` or `--level` - Logging level. Defaults to ``INFO``.

# Helpers

These files do not need to be called on their own but help the bash scripts.

## trace_valgrind.py

Helps format the results from ``trace-valgrind.sh``.

## trace_pin.py

Helps format the results from ``trace-pin.sh``.

## main.py

Simple placeholder script which simply prints ``Hello World!`` to the console.

# Sample Configuration Files

``hello-world-1866.json`` and ``hello-world-2400.json`` provide sample bases to run against the captured traces.