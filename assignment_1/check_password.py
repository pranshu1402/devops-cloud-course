# Q1. In DevOps, security is a crucial aspect, and ensuring strong passwords is essential. Create a Python script to check the strength of the password. 
# ●       Implement a Python function called check_password_strength that takes a password string as input.
# ●       The function should check the password against the following criteria:
# ○       Minimum length: The password should be at least 8 characters long.
# ○       Contains both uppercase and lowercase letters.
# ○       Contains at least one digit (0-9).
# ○       Contains at least one special character (e.g., !, @, #, $, %).
# ●       The function should return a boolean value indicating whether the password meets the criteria.
# ●       Write a script that takes user input for a password and calls the check_password_strength function to validate it.
# ●       Provide appropriate feedback to the user based on the strength of the password.

def check_password_strength(password):
    flag = True

    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        flag = False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        if char.islower():
            has_lower = True
        if char.isdigit():
            has_digit = True
        if char in '!@#$%^&*()_+':
            has_special = True

    if not has_upper:
        print("Password must contain at least one uppercase letter.")
        flag = False

    if not has_lower:
        print("Password must contain at least one lowercase letter.")
        flag = False

    if not has_digit:
        print("Password must contain at least one digit.")
        flag = False
    
    if not has_special:
        print("Password must contain at least one special character.")
        flag = False

    return flag

if __name__ == "__main__":
    user_password = input("Enter your password to check its strength: ")

    if check_password_strength(user_password):
        print("Your password is strong and meets the criteria!")
    else:
        print("Your password does not meet the required criteria.")

