FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    language-pack-en-base \
    openssh-server \
    openssh-client \
    python3.6 \
    python3-pip \
    python3-setuptools \
    ssh \
    sudo \
    vim \
    wget \
    less \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --no-cache-dir --upgrade \
    autopep8 \
    doc8 \
    docutils \
    ipython \
    pip \
    pylint \
    pytest \
    rope \
    setuptools \
    wheel \
    torch \
    tqdm \
    pandas
    
                                                    
# Create non-root user
ARG UID=1000
ARG GID=1000
ARG USERNAME=vscode

# 1001 is the group id for data-mole on beast1
RUN groupadd -g ${GID} ${USERNAME} \
    && useradd -ms /bin/bash -u ${UID} -g ${GID} -G sudo ${USERNAME} \
    && echo "${USERNAME}:${USERNAME}" | chpasswd \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && groupadd -g 1001 data-mole \
    && usermod -a -G data-mole ${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}

RUN bash -c "$(curl -L micro.mamba.pm/install.sh)"
# mkdir conda_installation \
# && cd conda_installation \
# && curl -LO "http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" \
# && bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda \
# && ~/miniconda/bin/conda init bash



