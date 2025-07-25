"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from main.core.backend.get_hash.internal.get_hash_view import get_hash
from main.core.backend.load_data.clean.internal.clean_database_view import clean_database
from main.core.backend.load_data.upload_images.internal.upload_images_endpoint import upload_images
from main.core.frontend.carte.internal.carte_view import carte
from main.core.frontend.home.internal.home_view import home
from main.core.frontend.errors.internal.errors_view import error_500_view, error_404_view
from main.core.frontend.login.internal.login_view import login_view
from main.core.frontend.photos.internal.photos_view import photos
from main.core.frontend.profile.profile import profile_view, change_collection_view, change_map_tiles_view, \
    change_theme_view

handler500 = error_500_view
handler404 = error_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Reset password flow
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('', home, name='home'),
    path('profile', profile_view, name='profile'),
    path('change-collection/<int:collection_id>/', change_collection_view, name='change_collection'),
    path('change-map-tiles/<int:map_tiles_id>/', change_map_tiles_view, name='change_map_tiles'),
    path('change-themes/<int:theme_id>/', change_theme_view, name='change_theme'),
    path('carte/', carte, name='carte'),
    path('photos/', photos, name='photos'),
    path('upload-images/<int:collection_id>/', upload_images, name='upload'),
    path('hash/<int:collection_id>/', get_hash, name='hash'),
    path('clean/<int:collection_id>/', clean_database, name='hash'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
