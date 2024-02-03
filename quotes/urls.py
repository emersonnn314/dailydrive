from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('saved-quotes/<str:author>/', views.saved_quotes, name='saved_quotes_by_author'),
    path('saved-quotes/', views.saved_quotes, name='saved_quotes'),

    path('save-quote/<str:quote_text>/<str:quote_author>/', views.save_quote, name='save_quote'),
    path('delete-saved-quote/<int:saved_quote_id>/', views.delete_saved_quote, name='delete_saved_quote'),
    path('delete-selected-quotes/', views.delete_selected_quotes, name='delete_selected_quotes'), 
]