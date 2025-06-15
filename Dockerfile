# Use a base Ubuntu image
FROM ubuntu:22.04

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV CONDA_DIR=/opt/conda

# Install necessary system dependencies
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    wget \
    bzip2 \
    gzip \
    ca-certificates \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libopenmpi-dev openmpi-bin

# Download and install Miniforge (includes Miniconda and defaults to conda-forge)
# Using the /latest/download/ link from GitHub releases
RUN wget --quiet https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /tmp/miniforge.sh && \
    bash /tmp/miniforge.sh -b -p ${CONDA_DIR} && \
    rm /tmp/miniforge.sh

# Initialize Conda for bash to use `conda activate` later
RUN ${CONDA_DIR}/bin/conda init bash

# Explicitly configure conda-forge channel (optional with Miniforge, but good practice)
# This adds conda-forge to the list of channels and sets its priority
RUN ${CONDA_DIR}/bin/conda config --add channels conda-forge && \
    ${CONDA_DIR}/bin/conda config --add channels defaults && \
    # Optional: Set channel priority to strict for more predictable installs
    ${CONDA_DIR}/bin/conda config --set channel_priority strict

# Set the PATH environment variable to include Conda's bin directory
ENV PATH=${CONDA_DIR}/bin:$PATH

# Set the working directory inside the container
WORKDIR /app

# Command to keep the container running (can be changed to your entrypoint)
CMD ["/bin/bash"]