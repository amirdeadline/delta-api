#delta_sase/urls_public

from django.conf.urls import include
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
    # path('api/v1/manage/staging/', include('staging_app.urls')),
    path('', include('tenants_app.urls')),
]