"""
.. module:: checkin_parking.core.views
   :synopsis: Checkin Parking Reservation Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""


from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from rmsconnector.forms import RMSAuthenticationForm
from rmsconnector.utils import Resident


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        # TODO: Add Session data to context

        return context


class LoginView(FormView):
    """

    Displays the login form and handles the login action.

    Sets user's display name and specializations as session variables upon authentication:
       request.session["user_display_name"] and
       request.session["user_specializations"]

    """

    template_name = 'core/login.html'
    form_class = AuthenticationForm
    rms_form_class = RMSAuthenticationForm

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        rms_form = self.get_form(self.rms_form_class)

        return self.render_to_response(self.get_context_data(form=form, rms_form=rms_form))

    def post(self, *args, **kwargs):
        form = self.get_form(self.form_class)
        rms_form = self.get_form(self.rms_form_class)

        if self.request.POST["user_type"] == "resident":
            if rms_form.is_valid():
                return self.form_valid(rms_form)
        else:
            if form.is_valid():
                return self.form_valid(form)

        return self.forms_invalid(form, rms_form)

    def form_valid(self, form):
        # Authenticate the user against LDAP
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user.is_authenticated():
            auth_login(self.request, user)

        self.success_url = self.request.GET.get("next", reverse_lazy('home'))

        return super(LoginView, self).form_valid(form)

    def rms_form_valid(self, form):
        # Authenticate the user against RMS
        alias = form.cleaned_data['alias']
        dob = form.cleaned_data['dob']
        user = authenticate(alias=alias, dob=dob)

        if user.is_authenticated():
            resident = Resident(alias=alias)

            try:
                resident.get_address()
            except ObjectDoesNotExist:
                raise ValidationError("The alias provided does not match University Housing records for the current term.")
            else:
                auth_login(self.request, user)

        self.success_url = self.request.GET.get("next", reverse_lazy('home'))

        return super(LoginView, self).form_valid(form)

    def forms_invalid(self, form, rms_form):
        return self.render_to_response(self.get_context_data(form=form, rms_form=rms_form))


def logout(request):
    """Logs the current user out."""

    auth_logout(request)
    redirection = reverse_lazy('home')
    return HttpResponseRedirect(redirection)
