from django.urls import path
from . import views

urlpatterns = [
    path('note/', views.Note.as_view(), name='note'),
    path('notemixins/', views.NoteMixins.as_view(), name='notemixins'),
    path('notemixins/<int:pk>', views.NoteMixins.as_view(), name='notemixins'),
    path('noteviewset/', views.NoteViewSet.as_view({'post': 'create', 'get': 'list', 'put': 'update',
                                                    'delete': 'destroy'}), name='noteviewset'),
]
