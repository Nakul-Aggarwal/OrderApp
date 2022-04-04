from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='accounts/update_item.html', success_url=reverse_lazy("accounts:items_list")),name='change_password'),
    path('', views.Index.as_view(), name="index"),
    path('items_list/', views.items_list, name='items_list'),
    path('options_list/', views.options_list, name='options_list'),
    path('update_item/<int:pk>', views.ItemsUpdateView.as_view(), name="update_item"),
    path('update_menu/<int:pk>', views.MenuUpdateView.as_view(), name="update_menu"),
    path('update_category/<int:pk>', views.CategoryUpdateView.as_view(), name="update_category"),
    path('item_availaible/<int:pk>', views.item_availaible, name="item_availaible"),
    path('menu_availaible/<int:pk>', views.menu_availaible, name="menu_availaible"),
    path('create_category/', views.CategoryCreateView.as_view(), name='create_category'),
    path('create_menu/', views.MenuCreateView.as_view(), name='create_menu'),
    path('create_item/', views.ItemsCreateView.as_view(), name='create_item'),
    path('create_table/', views.TableCreateView.as_view(), name='create_table'),
    path('view_table/<int:pk>', views.view_table, name='view_table'),
    path('view_order/<int:pk>', views.view_order, name='view_order'),
    path('feedback_list/', views.feedback_list, name="feedback_list"),
    path('create_option1/', views.Option1CreateView.as_view(), name='create_option1'),
    path('create_option2/', views.Option2CreateView.as_view(), name='create_option2'),
    path('create_extras/', views.ExtrasCreateView.as_view(), name='create_extras'),
    path('update_option1/<int:pk>', views.Option1UpdateView.as_view(), name='update_option1'),
    path('update_option2/<int:pk>', views.Option2UpdateView.as_view(), name='update_option2'),
    path('update_extras/<int:pk>', views.ExtrasUpdateView.as_view(), name='update_extras'),
    path('delete_option1/<int:pk>', views.Option1DeleteView.as_view(), name='delete_option1'),
    path('delete_option2/<int:pk>', views.Option2DeleteView.as_view(), name='delete_option2'),
    path('delete_extras/<int:pk>', views.ExtrasDeleteView.as_view(), name='delete_extras'),
    path('delete_feedback/<int:pk>', views.FeedbackDeleteView.as_view(), name='delete_feedback'),
    path('table_availaible/<int:tableNumber>', views.table_availaible, name='table_availaible'),
    path('table_unavailaible/<int:tableNumber>', views.table_unavailaible, name='table_unavailaible'),
    path('create_orderitem/<int:tableNumber>', views.create_orderitem, name='create_orderitem'),
    path('update_cart/', views.update_cart, name='update_cart'),
]
