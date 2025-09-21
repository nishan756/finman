from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

USER = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username = None , password = None , **kwargs):
        try:
            user = USER.objects.get(Q(username = username)|Q(email = username)|Q(phone = username))
        except USER.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
    

        