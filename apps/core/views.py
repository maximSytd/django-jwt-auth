from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, RedirectView):
    """Index view that redirect to open api schema"""

    pattern_name = "open_api:ui"
    permanent = False
