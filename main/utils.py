from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGen(PasswordResetTokenGenerator):
    pass

token_gen = TokenGen()