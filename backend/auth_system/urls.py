from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('dashboard/', include('accounts.urls')),
    path('quiz/', include('quiz.urls')),
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
