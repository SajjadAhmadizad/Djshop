from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.ContactUsView,name='contact-us'),
    path("create-profile/",views.CreateProfileView.as_view(),name='create-profile'),
    # path('',views.contact_us,name='contact-us'),
    path('profiles/',views.ProfileListView.as_view(),name='profile-list'),
]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
