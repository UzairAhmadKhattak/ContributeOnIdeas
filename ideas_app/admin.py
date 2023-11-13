from django.contrib import admin
from .models import UserProfile
from .models import UserEducation
from .models import UserExperience
from .models import Comment
from .models import NewFeed
from .models import UserStatistic
from .models import Contributor


admin.site.register(UserProfile)
admin.site.register(UserEducation)
admin.site.register(UserExperience)
admin.site.register(Comment)
admin.site.register(NewFeed)
admin.site.register(UserStatistic)
admin.site.register(Contributor)