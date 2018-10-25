from django.conf.urls import url
from seatview import views

urlpatterns = [
    url(r'^login/$',views.login),
    url(r'^login_check/$',views.login_check),
    url(r'^userInfo/$',views.userInfo),
    url(r'^show_message/$',views.show_message),
    url(r'^register/$',views.register),
    url(r'^register_check/$',views.register_check),
    url(r'^seat/$',views.seat),
    url(r'^upload_seat/$',views.upload_seat),
    url(r'^download_seat/$',views.download_seat),
    url(r'^download_comment/$',views.download_comment),
    url(r'^download_ordertime/$',views.download_ordertime),
    url(r'^cancel_reservation/$',views.cancel_reservation),
    url(r'^Submit_Commit/$',views.Submit_Commit),
]