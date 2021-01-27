from HD_app.models import User
from rest_framework.authtoken.models import Token
admin = User.objects.get(username='admin')
token = Token.objects.create(user=admin)
print("To jest token admina: %s\n" % token.key)
print("---------------------------------------")