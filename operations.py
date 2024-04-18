import argparse
from typing import Any, Iterable

from communex.client import CommuneClient
from communex.compat.key import classic_load_key
from communex.types import NetworkParams, Ss58Address
from substrateinterface import Keypair  # type: ignore
from substrateinterface.base import ExtrinsicReceipt  # type: ignore

# shouldn't this be passed via cli/file?
DEFAULT_PARAMS: NetworkParams = {
    "max_allowed_subnets": 256,
    "max_allowed_modules": 10000,
    "max_registrations_per_block": 10,
    "unit_emission": 23148148148,
    "tx_rate_limit": 1,
    "vote_threshold": 50,
    "vote_mode": "authority",
    "max_proposals": 128,
    "max_name_length": 32,
    "burn_rate": 0,
    "min_stake": 100_000_000_000,
    "min_weight_stake": 20_000_000_000,
    "min_burn": 2_500_000_000,
    "max_burn": 100_000_000_000,
    "target_registrations_interval": 200,
    "target_registrations_per_interval" : 25, 
    "floor_delegation_fee": 5,
    "adjustment_alpha": 4611686018427388000,
    "nominator": "5Gk2YXNEhKRPop2roXWqa2idXH4JbP1Wmgx7Gcpdj1wq54vx",
    "subnet_stake_threshold" : 2,
}


def update_global_multisig(
    client: CommuneClient,
    key: Keypair,
    signatories: list[Ss58Address],
    threshold: int,
    x,
) -> ExtrinsicReceipt:
    """
    Executes global mutlisig extrinsic
    """

    response = client.compose_call_multisig(
        fn="set_key",
        module="Sudo",
        params={"new" : "5GX2vR9EKHuTSTHqg3CLFSRmt8PT6hM8yUbkk9HZRU5kmkeA"},
        signatories=signatories,
        threshold=threshold,
        key=key,
        sudo=False,
    )
    return response


def update_params(
    client: CommuneClient,
    key: Keypair,
    signatories: list[Ss58Address],
    threshold: int,
    params: Any,
):
    
    # with open(params, "r") as file:
    #     params = json.load(file)
    ask_confirm_or_exit(
        f"We will upgrade the runtime wasm blog to the contents of `{DEFAULT_PARAMS}` file. Are you sure? (y/n) "
    )

    response = client.compose_call_multisig(
        fn="update_global",
        module="SubspaceModule",
        params=DEFAULT_PARAMS,
        signatories=signatories,
        threshold=threshold,
        key=key,
        sudo=True,
    )
    return response


def ask_confirm(txt: str):
    answer = input(txt)
    return answer.lower() in ["y", "yes"]

def ask_confirm_or_exit(txt: str):
    confirmed = ask_confirm(txt)
    if not confirmed:
        print("Aborted.")
        exit(1)

def runtime_upgrade(
    client: CommuneClient,
    key: Keypair,
    signatories: list[Ss58Address],
    threshold: int,
    wasm_path: Any,
):
    ask_confirm_or_exit(
       f"We will upgrade the runtime wasm blog to the contents of `{wasm_path}` file. Are you sure? (y/n) "
    )

    with open(wasm_path, "rb") as file:
        wasm = file.read()

    response = client.compose_call_multisig(
        module="System",
        fn="set_code",
        params={
            "code": wasm,
        },
        signatories=signatories,
        threshold=threshold,
        key=key,
        sudo=True,
    )
    return response


def config_parser(rpc_choices: Iterable[str]):
    parser = argparse.ArgumentParser(description="Update global multisig")
    parser.add_argument("keyname", help="Name of the key to use")
    parser.add_argument("threshold", help="minimum number of signatures", type=int)
    parser.add_argument(
        "function",
        help="rpc call to execute",
        choices=rpc_choices,
    )
    parser.add_argument("--wasm-path", help="path to the wasm file", required=False, default=None)
    parser.add_argument("--params-json", help="path to the params file", required=False)

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    rpc_map = {
        "runtime_upgrade": runtime_upgrade,
        "update_params": update_global_multisig,
    }

    args = config_parser(rpc_map.keys())
    ronaldo_key = args.keyname
    rpc_method = args.function
    rpc_func = rpc_map[rpc_method]
    threshold = args.threshold
    wasm_path = args.wasm_path
    params_path = args.params_json

    if rpc_method == "runtime_upgrade":
        assert wasm_path, "wasm path is required for runtime_upgrade"
        params = wasm_path

    # elif rpc_method == "update_params":
    #     assert params_path, "params path is required for update_params"
    #     params = params_path



    my_multisig = classic_load_key(ronaldo_key)
    # client = CommuneClient(url="wss://needed-mammoth-suitably.ngrok-free.app")
    client = CommuneClient(url="wss://commune-api-node-1.communeai.net")
    # client = CommuneClient("wss://testnet-commune-api-node-0.communeai.net")
    signatories: list[Ss58Address] = [
    "5GnXkyoCGVHD7PL3ZRGM2oELpUhDG6HFqAHZT3hHTmFD8CZF",  # Ho
    "5HYB5wVSTfnnpdZhCghk4qpoz8AjZzRiJNXdTLVNkZme18nN",  # Ti
    "5DAFjxqp9anjBNJfji2eLsYAj8L1tjsT4kfnFNpbhZtvA9u5",  # Hu
    "5GZBhMZZRMWCiqgqdDGZCGo16Kg5aUQUcpuUGWwSgHn9HbRC",  # Fa
    "5Ccp9v5nwQTHhbe7uc2qKu5sv86YZ9wVEwGNCTcSWozPvUV1",  # Co
    ]


    result = rpc_func(client, my_multisig, signatories, threshold, wasm_path)

    print(f"it ended up like this: {result}")
