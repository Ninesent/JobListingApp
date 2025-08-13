from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'common/homepage.html'

class AboutPageView(TemplateView):
    template_name = 'common/about.html'
