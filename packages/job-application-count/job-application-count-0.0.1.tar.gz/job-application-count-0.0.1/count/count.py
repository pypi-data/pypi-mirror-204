import random
import string

def get_application_count():
    # generate a random integer between 1 and 50 (inclusive)
    app_count = random.randint(1, 50)
    return app_count

def generate_password():
    # define the characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # generate a random password of length 8
    password = ''.join(random.choice(characters) for i in range(8))

    return password

# call the function and print the result
password = generate_password()
print("Generated password:", password)