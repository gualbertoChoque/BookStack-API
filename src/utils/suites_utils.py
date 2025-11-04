import random
import string

def generate_random_code_project(n):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    return random_string

def generate_random_id_suite():
    integer_part = random.randint(1, 10)
    decimal_part = random.random()
    return f"{integer_part:.1f}"

def generate_random_destination_id(type):
    match type:
        case "string":
            return random.choice(string.ascii_letters)
        case "float":
            return random.uniform(0.1, 0.9)
        case _:
            return None
