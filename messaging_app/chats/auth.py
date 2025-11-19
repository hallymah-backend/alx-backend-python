from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    This class simply extends JWTAuthentication.
    You can add custom logic if ALX requires it later.
    For now, it behaves the same as JWTAuthentication.
    """
    pass
