from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _

from .models import GifImage


class NoValidateImageField(forms.ImageField):
    # https://code.djangoproject.com/ticket/28242
    default_validators = []


class ImageUploadForm(forms.Form):
    image = NoValidateImageField()
    color = forms.CharField()
    caption = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy forms stuff
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.html5_required = True
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(Field('image'), css_class='pb-3'),
            Div(Field('caption', placeholder='caption'), css_class='pb-1'),
            Div(Field('color'), css_class='pb-3', id='colorpicker'),
            HTML('''
            <script>
            $(function () {
                $('#colorpicker input').spectrum({
                    preferredFormat: "hex",
                    color: '#f00',
                });
            });
            </script>
            '''),
            Submit('upload', _('Upload'), css_class='text-white', style='width: 100%'),
        )


class PasswordForm(forms.Form):
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy forms stuff
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.html5_required = True
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(Field('password'), css_class='pb-3'),
            Submit('ok', _('ok'), css_class='text-white', style='width: 100%'),
        )

class PasswordView(FormView):
    template_name = 'feed/password.html'
    form_class = PasswordForm

    def form_valid(self, form):
        if form.data['password'] == settings.PASSWORD:
            self.request.session['password'] = settings.PASSWORD
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('feed:feed')


class LogoutView(View):
    def get(self, request):
        del self.request.session['password']
        return HttpResponseRedirect(reverse('feed:feed'))


class FeedView(FormView):
    template_name = 'feed/feed.html'
    form_class = ImageUploadForm

    def authenticated(self, request):
        if not settings.PASSWORD:
            return True
        if request.session.get('password') == settings.PASSWORD:
            return True
        return False

    def get(self, request, *args, **kwargs):
        if not self.authenticated(request):
            return HttpResponseRedirect(reverse('feed:password-required'))
        return super().get(request, *args, **kwargs)

    def may_upload(self, request):
        return request.user.is_superuser

    def get_success_url(self):
        return reverse('feed:feed')

    def post(self, request, *args, **kwargs):
        if not self.may_upload(request):
            return HttpResponseRedirect(reverse('feed:feed'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        GifImage.objects.create(
            image=self.request.FILES['image'],
            bgcolor=form.data['color'][1:],  # strip away the '#'
            caption=form.data['caption'],
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'images': GifImage.objects.order_by('-created_at').all(),
            'may_upload': self.may_upload(self.request),
        })
        return context
