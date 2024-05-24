from werkzeug.security import generate_password_hash

# Your demo data
data = [
    {
        'email': 'demo1@example.com',
        'username': 'demo1',
        'password': 'password1',
        'first_name': 'Demo',
        'last_name': 'User1',
    },
    {
        'email': 'demo2@example.com',
        'username': 'your_friend',
        'password': 'password2',
        'first_name': 'Friend',
        'last_name': 'User2',
    },
]

# Hash the passwords
for user in data:
    user['password'] = generate_password_hash(user['password'], method='pbkdf2:sha256')

# Print the data with hashed passwords
for user in data:
    print(user)