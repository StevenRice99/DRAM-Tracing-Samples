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

# Helpers

These files do not need to be called on their own but help the bash scripts.

## trace_valgrind.py

Helps format the results from ``trace-valgrind.sh``.

## trace_pin.py

Helps format the results from ``trace-pin.sh``.

## main.py

Simple placeholder script which simply prints ``Hello World!`` to the console.