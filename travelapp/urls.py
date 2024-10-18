

from django.urls import path
from travelapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('register',views.register),
    path('login',views.userlogin),
    path('aboutus',views.aboutus),
    path('contactus',views.contactus),
    path('details/<int:travelid>', views.travelDetails),
    path('logout',views.userLogout),
    path('search/<str:searchBy>',views.searchByCatagory),
    # path('searchbyrange',views.searchByRange),
    # path('sort/<str:dir>',views.sortPetByPrice)
    path('addtocart/<int:travelid>',views.addToCart),
    path ('mycart',views.showMyCart),
    path('removecart/<int:cartid>',views.removeCart),
    path('updatecount/<int:cartid>/<str:oprn>', views.updateQuantity),
    path('confirmorder',views.confirmOrder),
    path('makepayment',views.makePayment),
    path('placeorder/<str:oid>',views.placeOrder),
    path('profile',views.editProfile),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
