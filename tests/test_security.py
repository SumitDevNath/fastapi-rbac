from app.core.security import get_password_hash, verify_password

password_raw = "SuperSecret123!"

# 1. Hash the same password twice
hash_1 = get_password_hash(password_raw)
hash_2 = get_password_hash(password_raw)

print(f"Hash 1: {hash_1}\n")
print(f"Hash 2: {hash_2}\n")

# Notice how the hashes are completely different because each has a unique random salt!
print(f"Hashes are distinct: {hash_1 != hash_2}")

# 2. Verify correct password
is_valid = verify_password("SuperSecret123!", hash_1)
print(f"Verification with correct password: {is_valid}")  # True

# 3. Verify incorrect password
is_invalid = verify_password("WrongPassword!", hash_1)
print(f"Verification with wrong password: {is_invalid}")  # False