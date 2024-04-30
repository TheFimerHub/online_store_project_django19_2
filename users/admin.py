from django.contrib import admin

from users.models import User

@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions