import random
import hashlib


class PwdGenerator:

    numbers_list = [chr(i) for i in range(48, 57+1)]
    alphabet_list = ([chr(i) for i in range(97, 122+1)]
                + [chr(i) for i in range(65, 90+1)])
    special_characters_list = ([chr(i) for i in range(33, 47+1)]
                          + [chr(i) for i in range(58, 64+1)])


    def __init__(self) -> None:
        ...

    @classmethod
    def generate_pwd(cls, pwd_length: int, allow_special_characters: bool=False) -> str:

        available_characters_list = list()
        available_characters_list += cls.numbers_list
        available_characters_list += cls.alphabet_list

        if allow_special_characters:
            available_characters_list += cls.special_characters_list
        
        password = str()
        for _ in range(pwd_length):
            password += random.choice(available_characters_list)
        
        return password

    @classmethod
    def hash_pwd_sha256(cls, password: str, salt: str=None, pepper: str=None) -> str:

        text_to_hash = password
        if salt:
            text_to_hash += salt
        if pepper:
            text_to_hash += pepper

        bytes_from_text = text_to_hash.encode('utf8')
        hash_value = hashlib.sha256(bytes_from_text)

        return hash_value


if __name__ == "__main__":
    pwd = PwdGenerator.generate_pwd(15, allow_special_characters=True)
    print(pwd)
