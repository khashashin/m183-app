from django.db import models


class Command(models.Model):
    command = models.CharField(
        max_length=10
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    def get_options(self):
        return self.option_set.all()

    def __str__(self):
        return self.command


class Option(models.Model):
    option = models.CharField(
        max_length=10
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    command = models.ForeignKey(
        Command,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.option
