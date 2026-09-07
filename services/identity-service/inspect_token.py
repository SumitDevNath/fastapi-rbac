import jwt


token = input(
    "Paste access token: "
).strip()


print(
    "HEADER:",
    jwt.get_unverified_header(token),
)


print(
    "CLAIMS:",
    jwt.decode(
        token,
        options={
            "verify_signature": False
        },
    ),
)