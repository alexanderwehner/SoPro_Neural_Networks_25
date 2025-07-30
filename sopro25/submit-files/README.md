# Specifying submit files

## The basics

Your submit file fulfills four important roles:

1. It specifies the docker image based on which HTCondor will create a docker container to run your code.

2. It specifies the bash script to execute. 

3. It specifies where outputs produced by your script will be saved.

4. It specifies the requirements of your job. 

## Providing arguments to the executable file

You can provide arguments to the bash script specified as the `executable` via the `arguments` line. E.g.

    arguments = arg1 arg2 arg3

These will be acessible inside the executable bash script via `$1, $2, $3`.

## Mounting /nethome/<username>

To mount your entiry `/nethome/<username>` inside the docker container, make the path of your nethome the `initialdir`. E.g

    initialdir = /nethome/<username>

## Logfiles

Make sure to put your log files under `/data/users/<username>`. Three separate logfiles will be produced for each job. Make sure that the paths you specify for `output`, `error`, and `log` exist.

You can use `tail -f <output-file>` to monitor the contents of a file in real time. See [here](https://man7.org/linux/man-pages/man1/tail.1.html) for more information on the tail command.

## Resource requirements

- You can request a specific number of CPU threads using `request_CPUs`.
- You can request a specific amount of RAM memory using `request_memory`.
- You can request a specific number of CPU threads using `request_GPUs`.
- You can define further GPU requirements as follows:
    - `GPUs_GlobalMemoryMb` defines the mimimum amount of GPU memory your job needs.
    - `machine` allows you to send your job to a specific machine.

Additional arguments are described [here](https://research.cs.wisc.edu/htcondor/wiki-archive/pages/HowToManageGpus/).
