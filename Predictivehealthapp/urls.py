
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
    path('viewprescription/<int:lid>',viewprescription.as_view(),name="viewprescription"),
    path('docaddslot',docaddslot.as_view(),name="docaddslot"),
    path('patientoverview',patientoverview.as_view(),name="patientoverview"),
    path('docdash',docdash.as_view(),name="docdash"),



    path('register',register.as_view(),name="userregister"),
    path('loginapi',LoginPage.as_view(),name="loginapi"),
    path('Docview',userviewDoc.as_view(),name="Docview"),
    path('prescriptionview/<int:lid>',DoctorDetailsView.as_view(),name="prescriptionview"),
    path('postview',userViewpost.as_view(),name="postview"),
    path('notificationview',userViewnotification.as_view(),name="notificationview"),
    path('bookinginfo',userViewappointment.as_view(),name="appointmentview"),
    path('chatbotapi',chatbotapi.as_view(),name='chatbotapi'),
    path('slotview',userViewSlot.as_view(),name="slotview"),
    path('bookslot',bookslot.as_view(),name='bookslot'),
    path('createappointment/<int:LID>',AppointmentCreateView.as_view(),name='createappointment'),
    path('forgot-password',ForgotPasswordView.as_view(), name='forgot_password'),
    path('user-profile/<int:lid>', UserProfileView.as_view(), name='user-profile'),
    path('addreview/<int:lid>', ReviewView.as_view(), name='addreview'),
    path('getreviews/<int:doc_id>/', UserViewreview.as_view(), name='getreviews'), 








]

