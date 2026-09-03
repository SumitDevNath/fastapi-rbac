from pydantic import ValidationError
from app.schemas.user import UserCreate

# 1. Test Valid Input
try:
    valid_data = UserCreate(
        email="test@domain.com",
        password="ValidPassword123"
    )
    print("✅ Validation Succeeded:", valid_data.model_dump())
except ValidationError as e:
    print("❌ Validation Failed:", e)

# 2. Test Invalid Email & Too Short Password
try:
    invalid_data = UserCreate(
        email="not-a-real-email",
        password="123"  # Less than 8 characters
    )
except ValidationError as e:
    print("\n✅ Pydantic Caught Invalid Inputs Successfully:")
    for err in e.errors():
        print(f"  - Field '{err['loc'][0]}': {err['msg']}")