from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('event_app/', include('events.urls')),
    path('members_app/', include('django.contrib.auth.urls')),
    path('members_app/', include('members.urls'))
]
# Configure Admin Titles
admin.site.site_header = "My club Administration Page"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome to the Admin Area"