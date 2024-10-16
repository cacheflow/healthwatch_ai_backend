from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .models import User



def register_user(inmate_id, password):
  try:
    user = User.objects.get(inmate_id=inmate_id)
    return {
      "inmate_id": user.inmate_id,
      "tokens": get_jwt_tokens(user)
    }
  except User.DoesNotExist:
    user = user.objects.create(
      inmate_id=inmate_id,
      password=make_password(password)
    )
    user.save()
    return {
      "inmate_id": user.inmate_id,
      "tokens": get_jwt_tokens(user)
    }
  
def get_jwt_tokens(user):
  refresh = RefreshToken.for_user(user)
  return {
    "refresh": str(refresh),
    "access": str(refresh.access_token)
  }