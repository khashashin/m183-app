from django.shortcuts import redirect
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'linux/index.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login page if not logged in
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Linux'
        return context
