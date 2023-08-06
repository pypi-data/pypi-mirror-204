import secrets

def del_key(key: str|int, d: dict):
    if key in d:
        del d[key]

def int_to_bool(i: int)->bool:
    if i == 0:
        return True
    else:
        return False

def old_gen_id(n: int=3):
    def a():
        choices = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        return "".join(list(map(lambda _: secrets.choice(choices), range(0, 5))))
    return "-".join(list(map(lambda _: a(), range(0, n))))

def gen_id(prefix: str, length: int=12):
    """
    Random generates an id with the particular prefix
    """
    if len(prefix) != 2:
        raise Exception("Prefixs must be 2 characters long")
    elif length <= 0:
        raise Exception("Length needs to be more then 0")

    choices = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
    id = "".join(list(map(lambda _: secrets.choice(choices), range(0, length))))
    return f"{prefix.lower()}:{id}"

