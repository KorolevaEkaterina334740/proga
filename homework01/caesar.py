import typing as tp


def encrypt_caesar(unciphered_text: str, shift: int = 3) -> str:
    ciphered_text = ""
    for i in range(len(unciphered_text)):
        if unciphered_text[i].isalpha():
            a = ord(unciphered_text[i])
            if unciphered_text[i].isupper() and a >= 91 - shift:
                ciphered_text += chr(a - 26 + shift)
            else:
                if unciphered_text[i].islower() and a >= 123 - shift:
                    ciphered_text += chr(a - 26 + shift)
                else:
                    ciphered_text += chr(a + shift)
        else:
            ciphered_text += unciphered_text[i]
    return ciphered_text


def decrypt_caesar(ciphered_text: str, shift: int = 3) -> str:
    unciphered_text = ""
    for i in range(len(ciphered_text)):
        if ciphered_text[i].isalpha():
            a = ord(ciphered_text[i])
            if ciphered_text[i].isupper() and a <= 64 + shift:
                unciphered_text += chr(a + 26 - shift)
            else:
                if ciphered_text[i].islower() and a <= 96 + shift:
                    unciphered_text += chr(a + 26 - shift)
                else:
                    unciphered_text += chr(a - shift)
        else:
            if ciphered_text.isspace():
                continue
            else:
                unciphered_text += ciphered_text[i]
    return unciphered_text


"""d = decrypt_caesar("SBWKRQ") #'PYTHON'
d = decrypt_caesar("sbwkrq") #'python'
d = decrypt_caesar("Sbwkrq3.6") #'Python3.6'
d = decrypt_caesar("") #''
print(d)"""
