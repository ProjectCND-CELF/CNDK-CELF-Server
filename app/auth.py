from fastapi import status, HTTPException


def process_token(token):
    if token == "m7Qp9Vx2KfT6nR8aL3zH1cW5yJ0uS4dE":
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
