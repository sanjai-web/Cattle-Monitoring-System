from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Define the urlpatterns first
urlpatterns = [
    path('', views.login_view, name='login'),            # Login page
    path('signup/',views.signup_view, name='signup'),   # Signup page
    path('home/', views.home_view, name='home'),         # Home page
   path('adminpage/', views.admin_page, name='admin_page'),
     # Admin page
    path('adminlogin/', views.adminlogin_view, name='adminlogin'),  # Admin login page
    path('cattle/', views.cattle_view, name='cattle'),   # Cattle page
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),         # Cart page
     path('generate-invoice/', views.generate_invoice_pdf, name='generate_invoice'),
    path('scheme/', views.scheme_view, name='scheme'),  # Scheme page
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('dashboard/', views.get_user_profile, name='dashboard'),  # Dashboard page
      path('checkout/', views.checkout_view, name='checkout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
 path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/sensor-data/', views.get_sensor_data, name='get_sensor_data'),
    path('veterinary/', views.veterinary_view, name='veterinary'),
     path('detect_disease/', views.detect_disease, name='detect_disease'),
    path('edit_scheme/<int:scheme_id>/', views.edit_scheme, name='edit_scheme'),
    path('delete_scheme/<int:scheme_id>/', views.delete_scheme, name='delete_scheme'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_cart_quantity/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    # path('admin/add_scheme/', views.add_scheme, name='add_scheme'),
#    path('admin-page/', views.admin_page, name='admin_page'),
    # path('add_product/', views.add_product, name='add_product'),
    # path('add_scheme/', views.add_scheme, name='add_scheme'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

