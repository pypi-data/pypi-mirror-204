import os
from cryptography.fernet import Fernet

class PasswordHandler():
    key_file = os.path.join(os.getcwd(),"bigtest_automator","key.key")
    # key_file = os.path.join(key_path,"key.key")

    def key_loader():
        # Generate or load the key
        if os.path.exists(PasswordHandler.key_file):
            with open(PasswordHandler.key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(PasswordHandler.key_file, "wb") as f:
                f.write(key)

        # Create a Fernet object with the key
        return Fernet(key)


    def encrypt_password(plaintext_password):
        fernet = PasswordHandler.key_loader()
        return fernet.encrypt(plaintext_password.encode()).decode("utf-8")
        

    def decrypt_password(encrypted_password):
        try:
            fernet = PasswordHandler.key_loader()
            return fernet.decrypt(encrypted_password).decode("utf-8")
        except Exception as e:
            print(e)
            raise ValueError("Keys did not match! Did you modify key.key file?")
            #return None

