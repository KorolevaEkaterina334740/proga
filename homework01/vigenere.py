import typing as tp


def encrypt_vigenere(unciphered_text: str, keyword: str) -> str:
    ciphered_text = ""
    a = 0
    while len(unciphered_text) > len(keyword):
        keyword += keyword[a]
        a += 1
    for i in range(len(keyword)):
        if keyword[i].isupper():
            key = ord(keyword[i]) - 65
        elif keyword[i].islower():
            key = ord(keyword[i]) - 97
        if unciphered_text[i].isalpha():
            c = ord(unciphered_text[i])
            if unciphered_text[i].isupper() and c >= 91 - key:
                ciphered_text += chr(c - 26 + key)
            elif unciphered_text[i].islower() and c >= 123 - key:
                ciphered_text += chr(c - 26 + key)
            else:
                ciphered_text += chr(c + key)
        else:
            ciphered_text += unciphered_text[i]
    return ciphered_text


def decrypt_vigenere(ciphered_text: str, keyword: str) -> str:
    unciphered_text = ""
    a = 0
    while len(ciphered_text) > len(keyword):
        keyword += keyword[a]
        a += 1
    for i in range(len(keyword)):
        if keyword[i].isupper():
            key = ord(keyword[i]) - 65
        elif keyword[i].islower():
            key = ord(keyword[i]) - 97
        if ciphered_text[i].isalpha():
            c = ord(ciphered_text[i])
            if ciphered_text[i].isupper() and c <= 64 + key:
                unciphered_text += chr(c + 26 - key)
            elif ciphered_text[i].islower() and c <= 96 + key:
                unciphered_text += chr(c + 26 - key)
            else:
                unciphered_text += chr(c - key)
        else:
            unciphered_text += ciphered_text[i]
    return unciphered_text
