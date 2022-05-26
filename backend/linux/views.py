from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from linux.models import Command


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

    @staticmethod
    def post(request):
        command = request.POST.get('command')
        options = request.POST.get('options')
        if not command:
            return JsonResponse({'error': 'Command is required'})
        if not options:
            return JsonResponse({'error': 'Options are required'})
        return JsonResponse({'command': command, 'options': options})
