import os

import Logger

def load():
    """
    This function parses a .env file and returns its content as a map.
    """
    if not os.path.exists('.env') and not os.path.exists('../.env'):
        Logger.error('Could not find any .env in the current or parent folder!')
        return dict()

    result = dict()

    # Load text content
    env_text = ''
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_text = f.readlines()

    if len(env_text) == 0 and os.path.exists('../.env'):
        with open('../.env', 'r') as f:
            env_text = f.readlines()

    if len(env_text) == 0:
        Logger.error('Could not load env file!')
        return dict()

    for line in env_text:
        if line == '\n':
            continue

        if line.startswith('#'):
            continue

        if line.endswith('\n'):
            line = line.strip('\n')

        key_value_pairs = line.split('=')
        key = key_value_pairs[0]
        value = key_value_pairs[1]

        result[key] = value

    Logger.success('Successfully loaded .env file')
    return result

def loadByKey(key: str):
    """
    This function parses a .env file and retrieves the value by the given key.
    """
    if not os.path.exists('.env') and not os.path.exists('../.env'):
        Logger.error('Could not find any .env in the current or parent folder!')
        return dict()

    result = None

    # Load text content
    env_text = ''
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_text = f.readlines()

    if len(env_text) == 0 and os.path.exists('../.env'):
        with open('../.env', 'r') as f:
            env_text = f.readlines()

    if len(env_text) == 0:
        Logger.error('Could not load env file!')
        return dict()

    for line in env_text:
        if line == '\n':
            continue

        if line.startswith('#'):
            continue

        if line.endswith('\n'):
            line = line.strip('\n')

        key_value_pairs = line.split('=')
        current_key = key_value_pairs[0]
        value = key_value_pairs[1]

        if current_key == key:
            result = value
            break

    Logger.success(f'Successfully loaded key {key}')
    return result