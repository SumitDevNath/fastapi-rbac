from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


KID = "dev-2026-09-a"

ROOT = Path(__file__).resolve().parents[1]

PRIVATE_DIR = ROOT / "keys" / "private"
PUBLIC_DIR = ROOT / "keys" / "public"

PRIVATE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PUBLIC_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)


private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)


public_key = private_key.public_key()

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)


private_path = (
    PRIVATE_DIR / f"{KID}.pem"
)

public_path = (
    PUBLIC_DIR / f"{KID}.pem"
)


private_path.write_bytes(private_pem)
public_path.write_bytes(public_pem)


print("Generated:")
print(private_path)
print(public_path)