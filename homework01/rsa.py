import random
import typing as tp


def is_prime(n: int) -> bool:
    if n == 2:
        return True
    else:
        if n == 1:
            return False
    if n % 2 == 0:
        return False
    b = 3
    while b ** 2 <= n and n % b != 0:
        b += 2
    return b ** 2 > n


def gcd(a: int, b: int) -> int:
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def multiplicative_inverse(e: int, phi: int) -> int:
    x = 1
    xx = 0
    y = 0
    yy = 1
    w = phi
    while phi:
        q = e // phi
        e, phi = phi, e % phi
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    k = x % w
    return k


def def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], unciphered_text: str) -> tp.List[int]:
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in unciphered_text]
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphered_text: tp.List[int]) -> str:
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphered_text]
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_message = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_message)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_message))
