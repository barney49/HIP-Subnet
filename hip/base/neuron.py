# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import copy
import typing

import bittensor as bt

from abc import ABC, abstractmethod

# Sync calls set weights and also resyncs the metagraph.
from hip.utils.config import check_config, add_args, config
from hip.utils.misc import ttl_get_block
from hip import __spec_version__ as spec_version
from hip.mock import MockSubtensor, MockMetagraph


class BaseNeuron(ABC):
    """
    Base class for Bittensor miners. This class is abstract and should be inherited by a subclass. It contains the core logic for all neurons; validators and miners.

    In addition to creating a wallet, subtensor, and metagraph, this class also handles the synchronization of the network state via a basic checkpointing mechanism based on epoch length.
    """

    neuron_type: str = "BaseNeuron"

    @classmethod
    def check_config(cls, config: "bt.Config"):  # type: ignore
        check_config(cls, config)

    @classmethod
    def add_args(cls, parser):
        add_args(cls, parser)

    @classmethod
    def config(cls):
        return config(cls)

    subtensor: "bt.subtensor"
    wallet: "bt.wallet"
    metagraph: "bt.metagraph"
    spec_version: int = spec_version

    @property
    def block(self):
        return ttl_get_block(self)

    def __init__(self, config=None):
        print("BaseNeuron init")
        base_config = copy.deepcopy(config or BaseNeuron.config())
        self.config = self.config()  # type: ignore
        self.config.merge(base_config)
        self.check_config(self.config)

        # Set up logging with the provided configuration and directory.
        bt.logging(config=self.config, logging_dir=self.config.full_path)  # type: ignore

        # If a gpu is required, set the device to cuda:N (e.g. cuda:0)
        self.device = self.config.neuron.device  # type: ignore

        # Log the configuration for reference.
        bt.logging.info(self.config)  # type: ignore

        # Build Bittensor objects
        # These are core Bittensor classes to interact with the network.
        bt.logging.info("Setting up bittensor objects.")

        # The wallet holds the cryptographic key pairs for the miner.
        self.wallet = bt.wallet(config=self.config)  # type: ignore
        self.subtensor = bt.subtensor(config=self.config)  # type: ignore
        self.metagraph = self.subtensor.metagraph(self.config.netuid)  # type: ignore

        bt.logging.info(f"Wallet: {self.wallet}")
        bt.logging.info(f"Subtensor: {self.subtensor}")
        bt.logging.info(f"Metagraph: {self.metagraph}")

        # Check if the miner is registered on the Bittensor network before proceeding further.
        self.check_registered()

        # Each miner gets a unique identity (UID) in the network for differentiation.
        self.uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
        bt.logging.info(
            f"Running neuron on subnet: {self.config.netuid} with uid {self.uid} using network: {self.subtensor.chain_endpoint}"
        )
        self.step = 0

    @abstractmethod
    async def forward(self, synapse: bt.Synapse) -> bt.Synapse: ...

    @abstractmethod
    def run(self): ...

    def sync(self):
        """
        Wrapper for synchronizing the state of the network for the given miner or validator.
        """
        # Ensure miner or validator hotkey is still registered on the network.
        self.check_registered()
        if self.should_sync_metagraph():
            self.resync_metagraph()  # type: ignore

        if self.should_set_weights():
            print("sync(): set_weights is called")
            self.set_weights()  # type: ignore

        # Always save state.
        self.save_state()

    def check_registered(self):
        # --- Check for registration.
        if not self.subtensor.is_hotkey_registered(
            netuid=self.config.netuid,
            hotkey_ss58=self.wallet.hotkey.ss58_address,
        ):
            bt.logging.error(
                f"Wallet: {self.wallet} is not registered on netuid {self.config.netuid}."
                f" Please register the hotkey using `btcli subnets register` before trying again"
            )
            exit()

    def should_sync_metagraph(self):
        """
        Check if enough epoch blocks have elapsed since the last checkpoint to sync.
        """
        return (
            self.block - self.metagraph.last_update[self.uid]
        ) > self.config.neuron.epoch_length

    def should_set_weights(self) -> bool:
        bt.logging.info(f"should_set_weights() called")
        # Don't set weights on initialization.
        if self.step == 0:
            bt.logging.debug("should_set_weights(): step == 0")
            return False

        # Check if enough epoch blocks have elapsed since the last epoch.
        if self.config.neuron.disable_set_weights:
            bt.logging.debug("should_set_weights(): disable_set_weights is True")
            return False

        # If neuron has validator permit we assume its running the validator code. If it is a dual permit neuron then we check that it also has a set_weights method (only true if it is running validator neuron)
        if not self.metagraph.validator_permit[self.uid] or not hasattr(
            self, "set_weights"
        ):
            bt.logging.debug(
                "should_set_weights(): not validator_permit or no set_weights method"
            )
            return False

        # Define appropriate logic for when set weights.
        bt.logging.debug(
            f"should_set_weights(): block - last_update = {self.block - self.metagraph.last_update[self.uid]}"
        )
        bt.logging.debug(
            f"should_set_weights(): epoch_length = {self.config.neuron.epoch_length}"
        )
        bt.logging.debug(f"should_set_weights(): neuron_type = {self.neuron_type}")
        return (
            self.block - self.metagraph.last_update[self.uid]
        ) > self.config.neuron.epoch_length and self.neuron_type != "MinerNeuron"  # don't set weights if you're a miner

    # TODO: Implement this function
    def save_state(self):
        return
        # bt.logging.warning(
        #     "save_state() not implemented for this neuron. You can implement this function to save model checkpoints or other useful data."
        # )

    # TODO: Implement this function
    def load_state(self):
        return
        # bt.logging.warning(
        #     "load_state() not implemented for this neuron. You can implement this function to load model checkpoints or other useful data."
        # )
