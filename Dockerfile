ARG BASE_IMAGE=ubuntu:20.04

# Builder stage
FROM $BASE_IMAGE AS builder

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y make build-essential git clang curl libssl-dev llvm libudev-dev protobuf-compiler

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    /bin/bash -c "source $HOME/.cargo/env"

# Clone Subtensor repository and build
RUN git clone https://github.com/opentensor/subtensor.git && \
    cd subtensor && \
    cargo build --release --features=runtime-benchmarks

# Final stage
FROM $BASE_IMAGE AS hip-subnet

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl git python3.10-venv
RUN curl -sL https://raw.githubusercontent.com/Unitech/pm2/master/packager/setup.deb.sh | sudo -E bash -

# Copy built binaries from builder stage
COPY --from=builder /subtensor/target/release/node-subtensor /usr/local/bin/
COPY --from=builder /subtensor/raw_testspec.json /subtensor/raw_testspec.json
RUN chmod +x /usr/local/bin/node-subtensor
COPY . /HIP-Subnet
WORKDIR /HIP-Subnet
RUN git checkout main
RUN python3.10 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
RUN pm2 start ecosystem.config.js
RUN pm2 save
RUN pm2 startup

# Expose necessary ports
EXPOSE 30333 9933 9944 3001


CMD ["pm2-runtime", "start", "ecosystem.config.js"]