# Development container based on the production Dockerfile
FROM python:3.9

# Install system dependencies for development
RUN apt-get update && apt-get install -y \
    git \
    curl \
    neovim \
    sudo \
    fish \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set up workspace
WORKDIR /workspace
COPY requirements.txt /workspace/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install minimal development tools
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio

# Switch to non-root user
USER $USERNAME

# Create .kube directory for the user
RUN mkdir -p /home/$USERNAME/.kube

