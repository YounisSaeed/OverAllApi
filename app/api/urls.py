from django.urls import path , include
from app.api.viewsets import( 
    FBV_LIST , 
    FBV_pk , 
    CBV_LIST ,
    CBV_PK ,

    mixins_list ,
    mixins_pk ,

    generics_list,
    generics_pk,

    viewsets_guest ,
    viewsets_movie,
    viewsets_reservation,
    
    find_movie,
    reservation,
    )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests',viewsets_guest)
router.register('movie',viewsets_movie)
router.register('reservation',viewsets_reservation)

urlpatterns = [
    #FBV
    path('guest/',FBV_LIST,name='list-guest'),
    path('guest/<str:pk>/',FBV_pk,name='RUD-Guest'),
    #CBV
    path('guestCBV/',CBV_LIST.as_view(),name='list-guest-cbv'),
    path('guestCBV_RUD/<str:pk>/',CBV_PK.as_view(),name='operation-guests'),
    #MIXINS
    path('guest_mixins/',mixins_list.as_view(),name='mixins-guest'),
    path('guest_mixins/<str:pk>/',mixins_pk.as_view(),name='mixins-guest-pk'),
    # GENERICS
    path('guest_generics/',generics_list.as_view(),name='generics-list-guest'),
    path('guest_generics/<str:pk>/',generics_pk.as_view(),name='generics-guest-pk'),

    # VIEWSETS
    path('viewsets/',include(router.urls)),

    # Find (movie)
    path('find/',find_movie,name='find-movie'),

    # Reservation
    path('reservation/',reservation,name='Reservation'),

]
