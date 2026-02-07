<br>

> [!NOTE]
> [rapids.ai application programming interface](https://docs.rapids.ai/api/)

<br>

## Environments

**Note**, the [requirements.txt](/.devcontainer/requirements.txt) file includes

* dask[complete]

and

* --extra-index-url=https://pypi.nvidia.com
  * cudf-cu12==25.12.*
  * dask-cudf-cu12==25.12.*

for GitHub Actions code analysis purposes.  These packages are included in the base image

* nvcr.io/nvidia/rapidsai/base:25.12-cuda12-py3.13

by default.  Hence, during the Dockerfile building steps each applicable Docker file filters out the above packages.

<br>

### Remote Development

For this Python project/template, the remote development environment requires

* [Dockerfile](/.devcontainer/Dockerfile)
* [requirements.txt](/.devcontainer/requirements.txt)

An image is built via the command

```shell
docker build . --file .devcontainer/Dockerfile -t distributing
```

On success, the output of

```shell
docker images
```

should include

<br>

| repository   | tag    | image id | created  | size     |
|:-------------|:-------|:---------|:---------|:---------|
| distributing | latest | $\ldots$ | $\ldots$ | $\ldots$ |


<br>

Subsequently, run an instance of the image `distributing` via:


```shell
docker run --rm --gpus all -i -t -p 8000:8000 -w /app --mount 
    type=bind,src="$(pwd)",target=/app 
      -v ~/.aws:/home/rapids/.aws distributing
```

<br>

Herein, `-p 8000:8000` maps the host port `8000` to container port `8000`.  Note, the container's working environment,
i.e., `-w`, must be inline with this project's top directory.  Additionally, visit the links for more about the flags/options $\rightarrow$

* --rm: [automatically remove container](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the)
* -i: [interact](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di)
* -t: [tag](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your)
* -p: [publish the container's port/s to the host](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s)
* --mount type=bind: [a bind mount](https://docs.docker.com/engine/storage/bind-mounts/#syntax)
* -v: [volume](https://docs.docker.com/engine/storage/volumes/)

<br>

The part `-v ~/.aws:/home/rapids/.aws` ascertains Amazon Web Services interactions via containers. Get the name of a running instance of ``distributing`` via:

```shell
docker ps --all
```

**Never deploy a root container, study the production** [Dockerfile](/Dockerfile); cf. [`.devcontainer/Dockerfile`](../.devcontainer/Dockerfile).

<br>

### Remote Development & Integrated Development Environments

An IDE (integrated development environment) is a helpful remote development tool.  The **IntelliJ
IDEA** set up involves connecting to a machine's Docker [daemon](https://www.jetbrains.com/help/idea/docker.html#connect_to_docker), the steps are

<br>

> * **Settings** $\rightarrow$ **Build, Execution, Deployment** $\rightarrow$ **Docker** $\rightarrow$ **WSL:** {select the linux operating system}
> * **View** $\rightarrow$ **Tool Window** $\rightarrow$ **Services** <br>Within the **Containers** section connect to the running instance of interest, or ascertain connection to the running instance of interest.

<br>

**Visual Studio Code** has its container attachment instructions; study [Attach Container](https://code.visualstudio.com/docs/devcontainers/attach-container).


<br>
<br>


## Code Analysis

The GitHub Actions script [main.yml](../.github/workflows/main.yml) conducts code analysis within a Cloud GitHub Workspace.  Depending on the script, code analysis may occur `on push` to any repository branch, or `on push` to a specific branch.

The sections herein outline remote code analysis.

### pylint

The directive

```shell
pylint --generate-rcfile > .pylintrc
```

generates the dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).  Analyse a directory via the command

```shell
python -m pylint --rcfile .pylintrc {directory}
```

The `.pylintrc` file of this template project has been **amended to adhere to team norms**, including

* Maximum number of characters on a single line.
  > max-line-length=127

* Maximum number of lines in a module.
  > max-module-lines=135

<br>

### pytest & pytest coverage

The directive patterns

```shell
python -m pytest tests/{directory.name}/...py
pytest --cov-report term-missing  --cov src/{directory.name}/...py tests/{directory.name}/...py
```

for test and test coverage, respectively.

<br>

### flake8

For code & complexity analysis.  A directive of the form

```bash
python -m flake8 --count --select=E9,F63,F7,F82 --show-source --statistics src/...
```

inspects issues in relation to logic (F7), syntax (Python E9, Flake F7), mathematical formulae symbols (F63), undefined variable names (F82).  Additionally

```shell
python -m flake8 --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics src/...
```

inspects complexity.

<br>
<br>

## Snippets

Determining a file's modification or creation date & time stamp

```python
import os
import time

# seconds since epoch
seconds: float = os.path.getctime(...)
stamp: str = time.ctime(seconds)
structure: time.struct_time = time.strptime(stamp)
time.strftime('%Y-%m-%d %H:%M:%S', structure)
```

<br>
<br>

## References

Large Scale Computation

* [DASK, EMR, Clusters](https://yarn.dask.org/en/latest/aws-emr.html)
* [Use the Nvidia RAPIDS Accelerator for Apache Spark](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-rapids.html)
  * [RAPIDS Base](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/rapidsai/containers/base)
  * [RAPIDS Accelerator for Apache Spark Deployment Guide](https://docs.nvidia.com/ai-enterprise/deployment/spark-rapids-accelerator/latest/emr.html)
  * [NVIDIA AI Enterprise with RAPIDS Accelerator Deployment Guide](https://docs.nvidia.com/ai-enterprise/deployment/spark-rapids-accelerator/latest/index.html)
  * [rapids.ai & Amazon EMR](https://docs.nvidia.com/ai-enterprise/deployment/spark-rapids-accelerator/latest/emr.html)
  * [rapids.ai, EMR, EKS](https://aws.amazon.com/blogs/containers/run-spark-rapids-ml-workloads-with-gpus-on-amazon-emr-on-eks/)
  * [Quickstart](https://docs.nvidia.com/spark-rapids/user-guide/latest/qualification/quickstart.html)
  * Images: **a.** [rapids.ai & EMR](https://gallery.ecr.aws/emr-on-eks/spark/emr-7.0.0-spark-rapids), **b.** [EMR](https://gallery.ecr.aws/emr-on-eks?page=1)
  * [Amazon EMR & Dockerfile](https://github.com/awslabs/data-on-eks/blob/main/ai-ml/emr-spark-rapids/examples/xgboost/Dockerfile)
  * [cutting cost](https://developer.nvidia.com/blog/accelerated-data-analytics-faster-time-series-analysis-with-rapids-cudf/)
* [Getting Started: Amazon EMR, Python, Spark](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html#emr-getting-started-plan-and-configure)
* [Configure Docker for use with Amazon EMR clusters](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-docker.html)
* [EMR & Custom Images](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/docker-custom-images-steps.html)
* [EMR Pricing](https://aws.amazon.com/emr/pricing/)

<br>

ECS
* [Amazon ECS task definitions for GPU workloads](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html)
* [Run Amazon ECS or Fargate tasks with Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html)

<br>

BATCH
* [Use a GPU workload AMI](https://docs.aws.amazon.com/batch/latest/userguide/batch-gpu-ami.html)

<br>

Engineering
* [requirements.txt](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
* [Development Containers](https://containers.dev)
  * [Development Containers & Dockerfile](https://containers.dev/guide/dockerfile)
  * [Development Containers & Features](https://containers.dev/features)
  * [Dockerfile](https://docs.docker.com/reference/dockerfile/)
* [GitHub Actions](https://docs.github.com/en/actions)
    * [build & test](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration): [Java + Maven](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-java-with-maven), [Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
    * [syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
    * [contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)
    * [variables](https://docs.github.com/en/actions/learn-github-actions/variables)


<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
