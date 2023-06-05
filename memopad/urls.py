from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('memo/', views.ListMemoView.as_view(), name='memo-list'),
    path('memo/detail/<int:pk>/', views.DetailMemoView.as_view(), name='memo-detail'),
    path('memo/create/', views.creatememo_func, name='new-memo'),
    # path('memo/create/', views.CreateMemoView.as_view(), name='memo-create'),
    path('memo/<int:pk>/delete/', views.DeleteMemoView.as_view(), name='mamo-delete'),
    path('memo/<int:pk>/update/', views.UpdateMemoView.as_view(), name='memo-update'),
    path('memo/orderchange/', views.memo_orderchange, name='memo-orderchange'),
]