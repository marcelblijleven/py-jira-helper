import os


def read_env_var(key: str) -> str:
    if not (value := os.getenv(key)):
        raise ValueError(f'No value set for env variable "{key}"')

    return value
