from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('event_app/', include('events.urls')),
    path('members_app/', include('django.contrib.auth.urls')),
    path('members_app/', include('members.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# Configure Admin Titles
admin.site.site_header = "My club Administration Page"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome to the Admin Area"