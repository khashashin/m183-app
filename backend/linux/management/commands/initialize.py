import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from linux.models import Command as LinuxCommand, Option
from .commands import COMMANDS

SITE_NAME = os.environ.get("SITE_NAME", "example.com")
DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "example.com")


class Command(BaseCommand):
    help = "Initialize Site Name."

    def handle(self, *args, **options):

        # Create Site
        initialize_site(stdout=self.stdout, style=self.style)
        # Create Commands
        initialize_commands(stdout=self.stdout, style=self.style)


def initialize_site(stdout, style):
    site, created = Site.objects.get_or_create(
            name='example.com',
            domain='example.com',
        )
    if created:
        stdout.write(
            style.SUCCESS(
                "Site Name: {}".format(site.name)
            )
        )
    else:
        stdout.write(
            style.SUCCESS(
                "Site Name: {}".format(Site.objects.get(pk=1).name)
            )
        )

    site.domain = f'{DOMAIN_NAME}'
    site.name = f'{SITE_NAME}'
    site.save()

    try:
        call_command("migrate")
    except CommandError as e:
        stdout.write(
            style.ERROR(
                "Migration Failed: {}".format(e)
            )
        )
    else:
        stdout.write(
            style.SUCCESS(
                "Migration Successful"
            )
        )


def initialize_commands(stdout, style):
    for command in COMMANDS:
        if LinuxCommand.objects.filter(name=command['name']).count() == 0:
            linux_command = LinuxCommand.objects.create(
                command=command['name'],
                name=command['name'],
                description=command['description']
            )
            linux_command.option_set.add(*initialize_options(stdout, style, command['options'], linux_command))
            linux_command.save()
            stdout.write(
                style.SUCCESS(
                    "Command: {}".format(command['name'])
                )
            )
        else:
            stdout.write(
                style.SUCCESS(
                    "Command: {}".format(command['name'])
                )
            )


def initialize_options(stdout, style, options, command):
    option_list = []
    for option in options:
        if Option.objects.filter(name=option['name']).count() == 0:
            option_list.append(
                Option.objects.create(
                    option=option['name'],
                    name=option['name'],
                    description=option['description'],
                    command=command,
                )
            )
            stdout.write(
                style.SUCCESS(
                    "Option: {}".format(option['name'])
                )
            )
        else:
            stdout.write(
                style.SUCCESS(
                    "Option: {}".format(option['name'])
                )
            )
    return option_list
