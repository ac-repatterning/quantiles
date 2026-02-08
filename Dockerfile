# Base Image
FROM nvcr.io/nvidia/rapidsai/base:25.12-cuda12-py3.13


USER root


# readlink -f /usr/bin/java | sed "s:/bin/java::"
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64


# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY /.devcontainer/requirements.txt /app


# Environment
SHELL [ "/bin/bash", "-c" ]


RUN apt update && apt -q -y upgrade && apt -y install sudo && sudo apt -y install graphviz && \
    sudo apt -y install wget && sudo apt -y install curl && sudo apt -y install unzip && \
    sudo apt -y install openjdk-17-jdk && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp/ && cd /tmp && sudo ./aws/install && cd ~ && \
    pip install --upgrade pip && \
    pip install $(grep -ivE "dask\[complete\]|cudf-cu12|dask-cudf-cu12" /app/requirements.txt) --no-cache-dir && \
    mkdir /app/warehouse && \
    chown -R rapids /app/warehouse


# Specific COPY
COPY src /app/src
COPY config.py /app/config.py


# Port
EXPOSE 8050


# Create mountpoint
VOLUME /app/warehouse


# automaton
USER rapids


# ENTRYPOINT
ENTRYPOINT ["python"]


# CMD
CMD ["src/main.py"]
