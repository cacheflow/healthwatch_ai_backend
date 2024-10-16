from rest_framework import serializers
from .models.medical_request import MedicalRequest, MedicalRequestSeverity
from django.conf import settings
import requests
import jwt
from .models import User

class SeverityMapping: 
  mapping = {
    0: 'Low',
    1: 'Moderate',
    2: 'Severe',
    3: 'Very Severe'
  }

  @classmethod 
  def get_label(cls, severity_num):
    return cls.mapping[severity_num].upper()

class MedicalRequestSerializer(serializers.ModelSerializer):
  severity_label = serializers.SerializerMethodField()
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'severity_label', 'duration_amount', 'duration_type', 'severity', 'escalating_cost', 'original_cost']

  def get_severity_label(self, obj):
    severity = obj.severity
    if isinstance(severity, str):
      return ' '.join(word.capitalize() for word in severity.split('_'))
    
    return SeverityMapping.get_label(severity)

class MedicalCreateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalRequest
    fields = ['inmate_id', 'description', 'category', 'duration_amount', 'duration_type', 'severity']


class AuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        # Verify the Auth0 token by decoding it using the public keys from Auth0
      auth0_domain = settings.AUTH0_DOMAIN
      jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
      try:
          jwks = requests.get(jwks_url).json()
      except requests.exceptions.RequestException as e:
          raise serializers.ValidationError(f"Failed to fetch JWKS: {e}")

      header = jwt.get_unverified_header(auth_token)
      rsa_key = {}
      for key in jwks["keys"]:
          if key["kid"] == header["kid"]:
              rsa_key = {
                  "kty": key["kty"],
                  "kid": key["kid"],
                  "use": key["use"],
                  "n": key["n"],
                  "e": key["e"],
              }
      if not rsa_key:
          raise serializers.ValidationError("Unable to find the appropriate key.")
      
      try:
          decoded_token = jwt.decode(auth_token, rsa_key, algorithms=["RS256"], audience=settings.AUTH0_AUDIENCE, issuer=f"https://{auth0_domain}/")
          inmate_id = decoded_token.get("sub")
      except jwt.ExpiredSignatureError:
          raise serializers.ValidationError("Token has expired.")
      except jwt.JWTClaimsError:
          raise serializers.ValidationError("Invalid token claims.")
      except Exception as e:
          raise serializers.ValidationError(f"Token validation error: {e}")

      # If token is valid, register user or retrieve the existing user
      user, created = User.objects.get_or_create(inmate_id=inmate_id)
      return user