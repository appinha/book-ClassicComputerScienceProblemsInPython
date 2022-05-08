from secrets import token_bytes


def generate_random_key(length: int) -> int:
    random_bytes: bytes = token_bytes(length)
    return int.from_bytes(random_bytes, "big")  # convert bytes into bit string

def encrypt(original: str) -> tuple[int, int]:
    original_bytes: bytes = original.encode()
    original_key: int = int.from_bytes(original_bytes, "big")
    dummy: int = generate_random_key(len(original_bytes))
    encrypted: int = original_key ^dummy  # XOR
    return dummy, encrypted

def decrypt(key1: int, key2: int) -> str:
    decrypted: int = key1 ^ key2  # XOR
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()


if __name__ == "__main__":
    original: str = "Amanda"

    key1, key2 = encrypt(original)
    print("-> encrypted key pair: {} + {}".format(key1, key2))

    decrypted: str = decrypt(key1, key2)
    print("-> original and decrypted are the same: {}".format(original == decrypted))
    print("-> original: {}".format(original))
    print("-> decrypted: {}".format(decrypted))
