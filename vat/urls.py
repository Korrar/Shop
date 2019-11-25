from django.urls import path , include
from vat.views import *

urlpatterns = [
    path('', home),
    path('list/', main_view),
    path('cart/', cart_view),
    path('edit/<str:name>/', edit_view),
    path('accounts/', include("django.contrib.auth.urls")),

]
