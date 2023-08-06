import crypt

_CRYPT_METHOD = crypt.METHOD_SHA512
_CRYPT_ROUNDS = 10000


def encrypt(plaintext_password: str, salt: str = None):
    """
    Encrypts a password for storage or comparison.
    :param plaintext_password: plaintext password
    :param salt: salt to use in the encryption; specify None to generate a new salt, or specify the salt of the
        password to be compared (only that substring that represents a salt will be used)
    :return: the encyrpted password
    """
    # Generate a temporary salt so that we know the length of the salt
    temp_salt = crypt.mksalt(_CRYPT_METHOD, rounds=_CRYPT_ROUNDS)
    if salt is not None:
        # Extract the salt from whatever else is in the string
        salt = salt[:len(temp_salt)]
    else:
        # Use the generated salt
        salt = temp_salt

    crypto = crypt.crypt(plaintext_password, salt)
    return f"{salt}{crypto}"


def is_valid(plaintext_password: str, encrypted_password: str):
    """
    Tests whether a plaintext password matches an encrypted password.
    :param plaintext_password: the password to be test
    :param encrypted_password: the basis for the comparison
    :return: s
    """
    # encrypt the plaintext password using the salt of the encrypted password
    pw = encrypt(plaintext_password, encrypted_password)
    # compare the resulting strings
    return pw == encrypted_password
