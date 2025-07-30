# htcondor-test

This project documents how to use the LSV compute servers via HTCondor (all condor commands are to be executed on `submit.lsv.uni-saarland.de`).

## Overview

The overall workflow is the following:

1. You create a `.sub` submit file which specifies (among other things) the resource requirements of your job.
2. You submit your job via `condor_submit [path-to-submit-file]`.
3. HTCondor tries to find a suitable compute node that matches the requirements of your job.
4. If a match exists, your job is executed on the matching compute node. 


## Managing dependencies

HTCondor will execute your code **inside a docker container** running on the matching compute node. This docker container is created based on a docker image specified in the submit file. There are two options for how make required dependencies (e.g. numpy, transformers, wanbd) available **inside** this docker container.

1. You create your own docker image which contains all dependencies. 
2. You use a default docker image and manage your dependencies via a miniconda virtual environment which can be accessed from inside the docker container.

### Create your own docker image

1. Create a new docker file. An example is provided [here](./docker/Dockerfile). This is where you install all dependencies.

2. Run 

        docker build -f [path_to_docker_file] --build-arg USER_UID=$UID --build-arg USER_NAME=$(id -un) -t docker.lsv.uni-saarland.de/[lsv_user_name]/[image_name]:[tag_name] . 
    
    to create a new docker image based on your docker file. You can pick your own image and tag names, but the prefix "docker.lsv.uni-saarland.de/[lsv_user_name]/" must be there.
    
    For example: `docker build -f ./docker/Dockerfile --build-arg USER_UID=$UID --build-arg USER_NAME=$(id -un) -t docker.lsv.uni-saarland.de/mmosbach/htcondor-test:22.02-py3 .`

3. Push the docker file to the lsv docker registry by running

        docker push [image_name]:[tag_name]
    
    For example: `docker push docker.lsv.uni-saarland.de/mmosbach/htcondor-test:22.02-py3`.


You can access the lsv docker registry here: http://docker.lsv.uni-saarland.de/ .

### Manage dependencies via miniconda

TODO


## Creating a submit file

Documentation on how to create submit files can be found [here](./submit-files).

## Check availablily of compute nodes

Run the following command to get an overview of how many free GPUs are available per compute node:

    condor_status -autoformat Name GPUs -constraint "PartitionableSlot == true"


## Submitting a job

To submit a job run the following: 

    condor_submit <path-to-submit-file>


To submit an interactive job run:

    condor_submit [path-to-submit-file] -interactive

Make sure to remove the `executable` line from your submit file (you can comment it with #). Inside the interactive session, run your script manually via `bash [path-to-script]`.


## Monitor your jobs

To get an overview over all jobs run:

    condor_q


Check which machines satisfy the requirements of your job (this assumes the job was already submitted)

    condor_q -better-analyze


Check which machines are running your jobs:

    condor_status -constraint 'RemoteUser == "[lsv-email]"'

For example: `condor_status -constraint 'RemoteUser == "mmosbach@lsv.uni-saarland.de"'`


## Your job is on hold

Run the following command to get information about why your job is on hold:

    condor_q -hold [jobid]


## Delete a job

To delete a job run:

    condor_rm [job-id]
