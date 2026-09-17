from django.urls import path

from . import views

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='property_list'),
    path('register/', views.OwnerRegisterView.as_view(), name='owner_register'),
    path('login/', views.OwnerLoginView.as_view(), name='owner_login'),
    path('logout/', views.OwnerLogoutView.as_view(), name='owner_logout'),
    path('dashboard/', views.OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('property/create/', views.PropertyCreateView.as_view(), name='create_property'),
    path('property/<int:pk>/edit/', views.PropertyUpdateView.as_view(), name='edit_property'),
    path('property/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='delete_property'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('save-favorite/<int:property_id>/', views.SaveFavoriteView.as_view(), name='save_favorite'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
]
