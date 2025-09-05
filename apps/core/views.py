from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class IndexView(LoginRequiredMixin, TemplateView):
    """Class-based view for index page."""

    template_name = "index.html"

class OwnerAccessMixin(UserPassesTestMixin):
    """Class based mixin for views to protect user's records."""

    def test_func(self):
        """Ensure that user can't gain access to other's records."""
        return self.request.user == self.get_object().user