import json
import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

from core import settings
from core.settings_dev import BASE_DIR
from linux.models import Command as LinuxCommand, Option
from .commands import COMMANDS

SITE_NAME = os.environ.get("SITE_NAME", "example.com")
DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "example.com")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@mail.ch")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', None)
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', None)
GITLAB_CLIENT_ID = os.getenv('GITLAB_CLIENT_ID', None)
GITLAB_CLIENT_SECRET = os.getenv('GITLAB_CLIENT_SECRET', None)

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize Site Name."

    def handle(self, *args, **options):
        # Create Site
        initialize_site(stdout=self.stdout, style=self.style)
        # Create Commands
        initialize_commands(stdout=self.stdout, style=self.style)
        # Create user
        initialize_user(stdout=self.stdout, style=self.style)
        # Configure Social Accounts
        initialize_social_accounts(stdout=self.stdout, style=self.style)
        # Configure logs files
        initialize_logs(stdout=self.stdout, style=self.style)


def initialize_site(stdout, style):
    site, created = Site.objects.get_or_create(
        domain=DOMAIN_NAME,
    )
    if created:
        site.name = SITE_NAME
        site.save()
        stdout.write(style.SUCCESS(
            "Successfully created Site: {}".format(site.name)
        ))
    else:
        stdout.write(style.SUCCESS(
            "Site name already exists: {}".format(Site.objects.get(pk=1).name)
        ))

    try:
        call_command("migrate")
    except CommandError as e:
        stdout.write(style.ERROR(
            "Migration Failed: {}".format(e)
        ))
    else:
        stdout.write(style.SUCCESS(
            "Migration Successful"
        ))


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
            stdout.write(style.SUCCESS(
                "Successfully created command: {}".format(command['name'])
            ))
        else:
            stdout.write(style.SUCCESS(
                "Command already exists: {}".format(command['name'])
            ))


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
            stdout.write(style.SUCCESS(
                "Successfully created option: {} for command: {}".format(option['name'], command.name)
            ))
        else:
            stdout.write(style.SUCCESS(
                "Option: {} for command: {} already exists: ".format(option['name'], command.name)
            ))
    return option_list


def initialize_user(stdout, style):
    if User.objects.filter(username="admin").count() == 0:
        admin = User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
        admin.save()
        stdout.write(style.SUCCESS(
            "Successfully created Admin user: {}".format(admin.username)
        ))


def initialize_social_accounts(stdout, style):
    if GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
        try:
            github, created = SocialApp.objects.get_or_create(
                provider='github',
                name='m183 - GitHub',
                client_id=GITHUB_CLIENT_ID,
                secret=GITHUB_CLIENT_SECRET,
            )
            github.sites.add(settings.SITE_ID)
            github.save()

            if created:
                stdout.write(style.SUCCESS("GitHub Social App already exists"))
            else:
                stdout.write(style.SUCCESS("Successfully created GitHub Social App"))
        except:
            raise CommandError('Error creating GitHub social app.')
    else:
        stdout.write(style.WARNING("GitHub Social App not configured"))

    if GITLAB_CLIENT_ID and GITLAB_CLIENT_SECRET:
        try:
            gitlab, created = SocialApp.objects.get_or_create(
                provider='gitlab',
                name='m183 - GitLab',
                client_id=GITLAB_CLIENT_ID,
                secret=GITLAB_CLIENT_SECRET,
            )
            gitlab.sites.add(settings.SITE_ID)
            gitlab.save()

            if created:
                stdout.write(style.SUCCESS("GitLab Social App already exists"))
            else:
                stdout.write(style.SUCCESS("Successfully created GitLab Social App"))
        except:
            raise CommandError('Error creating GitLab social app.')
    else:
        stdout.write(style.WARNING("GitLab Social App not configured"))


def initialize_logs(stdout, style):
    # Create logs/last_run.json file
    try:
        file_path = BASE_DIR / 'logs/last_run.json'
        with open(file_path, 'w') as f:
            json.dump({}, f)

        stdout.write(style.SUCCESS("Successfully created logs/last_run.json"))
    except:
        raise CommandError('Error creating last_run.json file.')
