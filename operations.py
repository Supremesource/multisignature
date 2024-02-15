from communex.client import CommuneClient
from communex.compat.key import classic_load_key
from substrateinterface import (ExtrinsicReceipt, Keypair)  # type: ignore
from typing import Any
from communex.types import NetworkParams
from communex.types import Ss58Address


params: NetworkParams = {
    "max_allowed_subnets": 256,
    "max_allowed_modules": 10000,
    "max_registrations_per_block": 1,
    "unit_emission": 23148148148,
    "tx_rate_limit": 1,
    "vote_threshold": 50,
    "vote_mode": "authority",
    "max_proposals": 128,
    "max_name_length": 32,
    "burn_rate": 0,
    "min_burn": 0,
    "min_stake": 0,
    "min_weight_stake": 0
}


def update_global_multisig(
    client: CommuneClient,
    key: Keypair,
    signatories: list[Ss58Address],
    threshold: int,
    params: Any,
) -> ExtrinsicReceipt:
    """
    Executes global mutlisig extrinsic
    """
    general_params = dict(params)

    response = client.compose_call_multisig(
        fn='update_global',
        module="SubspaceModule",
        params=general_params,
        signatories=signatories,
        threshold=threshold,
        key=key,
    )

    return response


if __name__ == "__main__":
    client = CommuneClient(url="wss://commune.api.onfinality.io/public-ws")

    my_multisig = classic_load_key("ronaldo")

    threshold = 3

    signatories: list[Ss58Address] = [
        "5ELSoV9ntKSgjLQ2UQzUqkvQnpGoJyHWjo4cSp2w5yiEuSwW",  # Ho
        "5GWDrAW9sUTAwB53wjBYyBUngncnGww7b4GAnaGPp7PjRpQD",  # Ti
        "5HHPz5GdvSCw3WNZWVGy6ejgqwVA3oAKUPeaqw9aEDxDokaS",  # Hu
        "5E49Ry24q9JwB9AvUR2igfJHeqsDXmPuXRzC6jBqdHEgpE1X",  # Fa
        "5FHqJ94yptoK4ELSBqvJV4k3PKJXLsRUrKpVc6VFLUBgUZfG",  # Co
    ]

    input(f"enter if you agree with the parameters ? {params}")

    result = (update_global_multisig(
        client, my_multisig, signatories, threshold, params))

    print(f"it ended up like this: {result}")
