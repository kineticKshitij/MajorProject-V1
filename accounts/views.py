from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserUpdateForm
from .models import User, UserProfile


class CustomLoginView(LoginView):
    """Custom login view"""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('googledorks:home')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name() or form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('googledorks:home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('googledorks:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def api_key_setup_view(request):
    """API key setup view"""
    if request.method == 'POST':
        api_key = request.POST.get('gemini_api_key', '').strip()
        if api_key:
            request.user.gemini_api_key = api_key
            request.user.save()
            messages.success(request, 'Gemini API key updated successfully! You can now use the AI chatbot.')
            return redirect('chatbot:home')
        else:
            messages.error(request, 'Please enter a valid API key.')
    
    context = {
        'has_api_key': request.user.has_gemini_api_key(),
        'api_key': request.user.gemini_api_key if request.user.has_gemini_api_key() else '',
    }
    return render(request, 'accounts/api_key_setup.html', context)