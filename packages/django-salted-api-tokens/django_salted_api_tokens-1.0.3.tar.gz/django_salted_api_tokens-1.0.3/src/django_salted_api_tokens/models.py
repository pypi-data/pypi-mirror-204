# Create your models here.
from django.conf import settings
from django.db import models
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext_lazy as _

user_model = settings.AUTH_USER_MODEL


class ApiToken(models.Model):
    created_at = DateTimeField(auto_now_add=True, db_index=True)
    modified_on = DateTimeField(auto_now=True, db_index=True)
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name='tokens'
    )
    token_id = models.CharField(
        _('Token_Id'), max_length=40, unique=True, db_index=True
    )
    token = models.CharField(_('Token'), max_length=256)
    revoked = models.BooleanField(_('Revoked'), default=False)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'DSAT User token'
        verbose_name_plural = 'DSAT User tokens'
