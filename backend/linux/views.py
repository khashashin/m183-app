import json
import os
import re
import subprocess
import html

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from core.settings_dev import BASE_DIR
from linux.models import Command


BLACK_LIST_CHARACTERS = [';', '&&', '||', '|', '>', '<', '$', '`', '{', '}', '~',  '=', '\n']


class IndexView(TemplateView):
    template_name = 'linux/index.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login page if not logged in
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        commands = Command.objects.all()
        context = super().get_context_data(**kwargs)
        context['allowed_commands'] = [{
            'name': command.name,
            'description': command.description,
            'options': [{
                'name': option.name,
                'description': option.description,
            } for option in command.get_options()]
        } for command in commands]
        return context


class RunView(View):

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login page if not logged in
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def post(request):
        # Users can run commands only each 7 seconds
        last_run = BASE_DIR / 'logs/last_run.json'
        if not os.path.isfile(last_run):
            with open(last_run, 'w') as f:
                json.dump({'file_initiated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f)

        with open(last_run, 'r+') as f:
            last_usage = json.load(f)
            if request.user.username in last_usage:
                command_by_user = last_usage[request.user.username]
                command_dt = datetime.strptime(command_by_user, '%Y-%m-%d %H:%M:%S')
                # If last command was made less than 7 seconds ago, skip
                if (datetime.now() - command_dt) < timedelta(seconds=7):
                    return JsonResponse(
                        {'error': 'You can run commands only each 7 seconds'},
                        status=400
                    )
                else:
                    last_usage[request.user.username] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                last_usage[request.user.username] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            f.seek(0)
            json.dump(last_usage, f)

        # Get command from body
        command = json.loads(request.body.decode("utf-8"))
        if not commant_is_valid(command['input']):
            # Run command
            return JsonResponse(
                {'error': 'Invalid command'},
                status=400
            )

        result = subprocess.run(
            [command['input']],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            # universal_newlines=True,
            timeout=10
        )

        result.stdout = html.escape(result.stdout)
        result.stderr = html.escape(result.stderr)

        result.stdout = re.sub(r'\n', '<br>', result.stdout)
        result.stderr = re.sub(r'\n', '<br>', result.stderr)

        return JsonResponse(
            status=200,
            data={
                'output': result.stdout,
                'error': result.stderr,
            }
        )


def commant_is_valid(command):

    command = get_command(command)
    options = get_options(command)

    for character in BLACK_LIST_CHARACTERS:
        if character in command:
            return False

    # Check if command is valid
    is_valid_command = validate_command(command)

    if not options:
        is_valid_option = True
    else:
        is_valid_option = validate_option(options, command)

    return is_valid_command and is_valid_option


def get_command(command):
    command = command.split(' ')
    return command[0]


def get_options(command):
    command = command.split(' ')
    if len(command) > 1:
        return command[1:]

    return []


def validate_command(command):
    # Check if command is valid
    allowed_commands = Command.objects.all()
    for allowed_command in allowed_commands:
        if allowed_command.name == command:
            return True

    return False


def validate_option(options, command):
    # Check if option is valid
    allowed_commands = Command.objects.filter(command=command)
    is_valid = True
    for allowed_options in allowed_commands:
        for allowed_option in allowed_options.get_options():
            if allowed_option.name not in options:
                is_valid = False

    return is_valid



