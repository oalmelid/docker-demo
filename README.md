# docker-demo

This is a small demo repository, intended to show how one can build, package and run code with dependencies in a docker container.

## Layout

### Python code

The script in [demo/demo.py](demo/demo.py) will take two or more bedfiles as input, and write their intersection to a file.
A single unit test can be found in the test directory.
The test_data directory contains two input files and their expected result.

### The Dockerfile

The Dockerfile does the following things

- Fetches the pre-built python:3.8 container from the docker hub and builds on top of it
- Copies the entire contents of this repository into the directory `/src/` within the container
- Sets the working directory to `/src/`
- Installs the project and its dependencies
- Sets the newly created container's entrypoint to run `/src/demo/demo.py`

This creates a container which, when run, will run the demo script. The container also creates all required dependencies for the project. It's worth noting that a container does not have to have an entrypoint. It can contain multiple binaries and tools as appropriate. In those cases, the program to run within the container is specified on the command line when the container is executed.

## Requirements
- To build this locally on your computer, you will need to install [docker](https://www.docker.com/get-started)
- A [docker hub](https://hub.docker.com/) account is required to create a repository and push your image to it.
- The final run on the compute cluster assumes you have access to [singularity](https://singularity.lbl.gov/), which you would need to get installed on your compute infrastructure.

## Usage

The instructions below show how to build, run, tag, push and pull the container. Anything within angle brackets should be substituted according to preference.

### Local build
To build the container, clone the repository by running the command
```bash
git clone https://github.com/oalmelid/docker-demo.git
```
Then change directory to the newly cloned docker-demo repository and run
```bash
docker build . -t <choose-your-own-container-name>
```
The above command causes docker to read the Dockerfile in the current directory (the `.` above references the current directory). Docker then pulls the `python:3.8` container and executes the provided commands inside of it. At the end, docker stores a container image in your local cache for further use.

You should be able to list your built and downloaded containers by running
```bash
docker images
```

### Running the container with docker
You'll need some data files in BED format. There are two included in the test_data folder within this repository. To run the script on those files, run
```bash
cd test_data
docker run -v ${PWD}:/data/ <container-name-from-build-step> /data/file1.bed /data/file2.bed /data/output.bed
```
The option `-v ${PWD}:/data/` above tells docker to mount the current working directory as `/data/` inside the container.
This is required because docker is designed to isolate anything running inside the container from the surrounding file system.

If all goes well, you should now have a file called `output.bed` in your current directory with the following content
```
chr1	800	900	.	.	.
chr3	200	220	.	.	.
```

### Pushing to Docker Hub
Create a repository on the docker hub. To push your image there, run
```bash
docker tag <container-name-from-build-step> <docker-hub-repository>:<tag>
docker push <docker-hub-repository>:<tag>
```
You can choose the tag name yourself. It's conventional for the tag name latest to correspond to the most recent commit on the main branch of your code repository.

### Running the container elsewhere with docker
After pushing the container, it can be run from anywhere, simply by referencing the tag you pushed to the Docker hub. Simply run
```bash
docker run <docker-hub-repository>:<tag>
```
And use flags and file inputs/outputs as needed.

### Running the container on eddie with singularity
This step is only intended for users on the university of the Edinburgh eddie compute cluster, though should be broadly applicable to anyone using singularity. Substitute directories and module names as appropriate if you are not working on eddie.

Like many HPC clusters, eddie does not permit the use of docker, since the docker daemon has root privileges and can be used for privilege escalation attacks. The singularity container engine provides many of the same features as docker, but runs with the privileges of the scheduling user and hence is preferred by many HPC administrators. Singularity also supports MPI, which can be useful in an HPC environment.

Singularity will download and cache container images, so it's important to make sure this cache is stored somewhere with plenty of space. To do so, set the `SINGULARITY_CACHEDIR` environment variable.
```bash
export SINGULARITY_CACHEDIR=/path/to/use/for/cache
```
Like other environment variables, this can be added to e.g. `.profile` or `.bashrc` for more permanent use.

You will also need to load a singularity module. At the time of writing, 3.5.3 is the most recent version available on eddie, so run
```bash
module load singularity/3.5.3
```
Finally, grab some bed files you want to intersect, put them in your current working directory and run
```bash
singularity run docker://<docker-hub-repository>:<tag> <input_file1> <input_file2> <output_file>
```
Note that singularity automatically mounts the current working directory and runs your container command from it, so you don't have to pass mount flags like you did with docker.
