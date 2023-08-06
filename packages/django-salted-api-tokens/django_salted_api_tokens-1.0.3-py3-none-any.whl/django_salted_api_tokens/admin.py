# Register your models here.

from django.contrib import admin

from django_salted_api_tokens.models import ApiToken


class AdminApiToken(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'user',
        'token_id',
        'deactivated',
        'created_at',
        'modified_on',
    )
    ordering = ('-created_at', 'user')
    search_fields = (
        'user',
        'token_id',
    )
    fields = ('created_at', 'modified_on', 'user', 'token_id', 'revoked')
    readonly_fields = (
        'user',
        'token_id',
        'created_at',
        'modified_on',
    )

    @admin.display(description='active', boolean=True)
    def deactivated(self, obj):
        return not obj.revoked


admin.site.register(ApiToken, AdminApiToken)
