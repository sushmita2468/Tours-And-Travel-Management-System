from django.contrib import admin
from django.urls import path, include
from signup.views import login_view,signup


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
]

    # Add other URL patterns as needed

