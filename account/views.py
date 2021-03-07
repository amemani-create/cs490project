from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy

from blog.models import Profile
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm, CreateProfileForm


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ProfilePageView(generic.DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        # profile_menu = Profile.objects.all()
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
        page_profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_profile"] = page_profile
        return context

class CreateProfilePageView(generic.CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'registration/create_profile_page.html'
    #fields = ['bio', 'profile_pic', 'linkedin_url', 'fb_url', 'instagram_url', 'personal_url', 'is_eduprovider', 'is_teacher', 'is_parent', 'is_student']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'registration/edit_profile_page.html'
    #fields = ['bio', 'profile_pic', 'linkedin_url', 'fb_url', 'instagram_url', 'personal_url', 'is_eduprovider', 'is_teacher', 'is_parent', 'is_student']

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('password_success')


def PasswordSuccessView(request):
    return render(request, 'registration/password_success.html')
