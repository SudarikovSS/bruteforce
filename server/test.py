import hashlib

login = 'ssudarikov'
password_not_hashed = 'qmiLT4O5S0bTYZc'
password_hashed = hashlib.sha256(password_not_hashed.encode())
print(password_hashed.hexdigest())