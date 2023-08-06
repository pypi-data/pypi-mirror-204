from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from huscy.consents.models import Consent, ConsentFile
from huscy.project_consents.models import ProjectConsent, ProjectConsentFile, ProjectConsentToken
from huscy.consents.views import CreateConsentView, SignConsentView
from huscy.project_consents.forms import TokenForm
from huscy.projects.models import Project
from huscy.subjects.models import Subject


class CreateProjectConsentView(CreateConsentView):

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(self, request, *args, **kwargs)
        consent = Consent.objects.latest('id')
        ProjectConsent.objects.create(consent=consent, project=self.project)
        return response

    def get_success_url(self):
        return reverse('consent-created')


class CreateTokenView(generic.FormView):
    form_class = TokenForm
    template_name = 'project_consents/projectconsenttoken.html'

    def form_valid(self, form):
        token, _created = ProjectConsentToken.objects.get_or_create(
            project=form.cleaned_data.get('project'),
            subject=form.cleaned_data.get('subject'),
        )
        return HttpResponseRedirect(
            '{}?token={}'.format(reverse('create-project-consent-token'), token.id)
        )

    def get_context_data(self):
        context = super().get_context_data()
        if 'token' in self.request.GET:
            token = get_object_or_404(ProjectConsentToken, pk=self.request.GET.get('token'))
            context['sign_project_consent_url'] = '{protocol}://{host}{url}'.format(
                protocol=self.request.scheme,
                host=self.request.get_host(),
                url=reverse('sign-project-consent', kwargs=dict(token=token.id))
            )
        return context


class SignProjectConsentView(SignConsentView):

    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(ProjectConsentToken, pk=self.kwargs['token'])
        self.consent = self.token.project.projectconsent.consent  # required by parent class
        return super(SignConsentView, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(self, request, *args, **kwargs)
        consent_file = ConsentFile.objects.latest('id')
        ProjectConsentFile.objects.create(
            consent_file=consent_file,
            project_consent=self.project_consent,
            subject=self.token.subject
        )
        self.token.delete()
        return response
