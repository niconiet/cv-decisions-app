from django.db import models


class MailAccount(models.Model):
    mail = models.EmailField(max_length=40,
                             default=None,
                             null=True,
                             blank=True)

    def __str__(self):
        return self.mail
