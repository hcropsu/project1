from django.urls import path
from . import views

app_name = "berries"
urlpatterns = [
    path('', views.entry_list, name="entry_list"),
    path('entry/<int:entry_id>/', views.entry_detail, name="entry_detail"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('sign_out/', views.sign_out, name="sign_out"),
    path('entry/<int:entry_id>/new_comment/', views.new_comment, name="new_comment"),
    path('entry/<int:entry_id>/comment/<int:comment_id>/delete', views.delete_comment, name="delete_comment"),
]