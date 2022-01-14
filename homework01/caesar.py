import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for i in plaintext:
        if i.isalpha():
            if i.istitle():
                i = chr(ord(i) + shift)
                if ord(i) > ord("Z"):
                    i = chr(ord(i) - 26)
            else:
                i = chr(ord(i) + shift)
                if ord(i) > ord("z"):
                    i = chr(ord(i) - 26)
        ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for i in ciphertext:
        if i.isalpha():
            if i.istitle():
                i = chr(ord(i) - shift)
                if ord(i) < ord("A"):
                    i = chr(ord(i) + 26)
            else:
                i = chr(ord(i) - shift)
                if ord(i) < ord("i"):
                    i = chr(ord(i) + 26)
        plaintext += i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    return best_shift
