from constants import *

def token_error(token: str) -> bool:
    if len(token) != 16 or any(character not in BASE62 for character in token):
        print(f"Error: invalid token")
        print(f"Token should be 16 characters {f'(not {len(token)}) ' if len(token) != 16 else ' '}and every character should be in this set:")
        print(BASE62 + '\n')
        return True
    return False

def name_error(name: str) -> bool:
    if name is None:
        print("Warning: name is None\n")
        return False
    if not NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH:
        print(f"Error: name {name!r} of bad length {len(name)}")
        print(f"Minimum is {NAME_MIN_LENGTH} and maximum is {NAME_MAX_LENGTH}\n")
        return True
    return False

def description_error(description: str) -> bool:
    if description is None:
        print("Warning: description is None\n")
        return False
    if not DESCRIPTION_MIN_LENGTH <= len(description) <= DESCRIPTION_MAX_LENGTH:
        print(f"Error: description {description!r} of bad length {len(description)}")
        print(f"Minimum is {DESCRIPTION_MIN_LENGTH} and maximum is {DESCRIPTION_MAX_LENGTH}\n")
        return True
    return False

def score_error(score: float) -> bool:
    if not 0 <= score <= 1:
        print("Invalid score! (nice try)")
        print(f"Score {score!r} not between 0 and 1\n")
        return True
    return False

def hostname_error(hostname: str) -> bool:
    if not hostname.startswith("http"):
        print(f"Error: bad hostname {hostname!r} does not start with 'http'")
        print(f"Did you mean: {'https://' + hostname!r}\n")
        return True
    if hostname.endswith("/"):
        print(f"Error: bad hostname {hostname!r} ends with '/'")
        print(f"Did you mean: {hostname.removeprefix('/')!r}\n")
        return True
    return False