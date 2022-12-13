from django.db import models
from django.contrib.auth.models import User


class PanelModel(models.Model):

    class Meta:
        permissions = (
            ("can_acces_panel", "Can acces to Worker's panel"),
        )
