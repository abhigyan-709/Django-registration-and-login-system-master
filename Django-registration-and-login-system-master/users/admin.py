from django.contrib import admin
from .models import Profile

admin.site.register(Profile)

from .models import Question, UserResponse

admin.site.register(Question)
admin.site.register(UserResponse)