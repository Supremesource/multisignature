# Commune multisig

Execute all sudo operations on Commune through the multisig of five.

## Install

```sh
python3 -m venv env
pip install -r requirements.txt
```

## CLI

To update global parameters

```sh
python3 operations.py <key_name> <threshold> update_params
```

To execute a runtime update

```sh
python3 operations.py <key_name> <threshold> runtime_upgrade --wasm-path <path_to_wasm>
```

### Note

Threshold on mainnet is "3".
