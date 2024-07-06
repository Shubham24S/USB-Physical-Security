import pyotp

# Generate a new Base32 secret
secret = pyotp.random_base32()
print(f"Your new Base32 secret is: {secret}")
