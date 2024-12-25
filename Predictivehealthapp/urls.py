
from django.contrib import admin
from django.urls import path

from Predictivehealthapp.views import *

urlpatterns = [
    path('admindashboard',administratordashboard.as_view(),name="admindashboard"),
    path('dashboard',dashboard.as_view(),name="dashboard"),
    path('doctorregister',docreg.as_view(),name="doctorregister"),
    path('editdoc/<int:doc_id>/',editdoc.as_view(), name='editdoc'),
    path('deletedoc/<int:doc_id>/',deletedoc.as_view(), name='deletedoc'),
    path('forgotpassword',forgotpass.as_view(),name="forgotpassword"),
    path('',login.as_view(),name="login"),
    path('viewdoctors',viewdoc.as_view(),name="viewdoctors"),
    path('viewappointment',viewappointment.as_view(),name="viewappointment"),
    path('addprescription/<int:b_id>',addprescription.as_view(),name="addprescription"),
    path('docaddpost',docaddpost.as_view(),name="docaddpost"),
    path('docdashboard',docdashboard.as_view(),name="docdashboard"),
    path('docposts',docposts.as_view(),name="docposts"),
    path('docsendnotification',docsendnotification.as_view(),name="docsendnotification"),
    path('docviewappointment',docviewapppointment.as_view(),name="docviewappointment"),
    path('viewprescription/<int:p_id>',viewprescription.as_view(),name="viewprescription")
]

