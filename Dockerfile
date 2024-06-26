ARG BASE_IMAGE=ubuntu:20.04
# Builder stage
FROM $BASE_IMAGE AS builder

SHELL ["/bin/bash", "-c"]

# This is being set so that no interactive components are allowed when updating.
ARG DEBIAN_FRONTEND=noninteractive

# show backtraces
ENV RUST_BACKTRACE 1

# Necessary libraries for Rust execution
RUN apt-get update && \
    apt-get install -y curl build-essential protobuf-compiler clang git && \
    rm -rf /var/lib/apt/lists/*

# Install cargo and Rust
RUN set -o pipefail && curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Clone Subtensor repository and build
RUN git clone https://github.com/opentensor/subtensor.git
WORKDIR /subtensor
RUN /subtensor/scripts/init.sh
RUN cargo build --release --features runtime-benchmarks --locked

# Final stage
FROM $BASE_IMAGE AS hip-subnet
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y sudo curl git software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev
# Set python3.10 as default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
# Install pm2
RUN curl -sL https://raw.githubusercontent.com/Unitech/pm2/master/packager/setup.deb.sh | sudo -E bash -

# Copy built binaries from builder stage
COPY --from=builder /subtensor/target/release/node-subtensor /usr/local/bin/
COPY --from=builder /subtensor/raw_testspec.json /subtensor/raw_testspec.json
RUN chmod +x /usr/local/bin/node-subtensor
COPY . /HIP-Subnet
WORKDIR /HIP-Subnet
RUN git checkout main
RUN python3.10 -m venv venv
RUN source venv/bin/activate
RUN python3.10 -m pip install -e .
RUN pm2 start ecosystem.config.js
RUN pm2 save
RUN pm2 startup

# Expose necessary ports
EXPOSE 30333 9933 9944 3001


CMD ["pm2-runtime", "start", "ecosystem.config.js"]