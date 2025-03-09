from .models import *
from rest_framework.serializers import ModelSerializer,FileField,SerializerMethodField
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model=userTable
        fields=['firstname','lastname','dob','gender','mobile','email','address','password']

class LoginSerializer(ModelSerializer):
    class Meta:
        model=LoginTable
        fields=['username','password']

class viewDocSerializer(ModelSerializer):
    class Meta:
        model=DoctorTable
        fields=['id','Name','specialization','qualification','phone','email','avg_rating','status']

class viewPrescriptionSerializer(ModelSerializer):
    doctor_name = serializers.CharField(source='APPOINTMENTID.DOCTORID.Name')

    class Meta:
        model=prescriptionTable
        fields=['doctor_name','diagnosis','medicine_name','medicine_dosage','medicine_itd','expirydate','remark', 'issueddate']

class viewPostSerializer(ModelSerializer):
    doctor_name = serializers.CharField(source="DOCTORID.Name", read_only=True)
    class Meta:
        model=postsTable
        fields=['doctor_name','title','category','content','filepost','createdat']

class viewNotificationSerializer(ModelSerializer):
    class Meta:
        model=NotificationTable
        fields=['content','attachement','createdat']

class viewAppointmentSerializer(ModelSerializer):
    doctor_name = serializers.CharField(source='DOCTORID.Name')
    class Meta:
        model=bookinginfoTable
        fields=['doctor_name', 'patient_name','patient_age','patient_height','patient_weight','patient_addr','APPOINTMENTDATE','APPOINTMENTTIME','visitReason', 'status']

class viewSlotSerializer(ModelSerializer):
    class Meta:
        model=SlotTable
        fields='__all__'

class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = bookinginfoTable
        fields=['patient_name', 'patient_age', 'patient_height', 'patient_weight', 'patient_addr', 'visitReason', 'status', 'APPOINTMENTDATE']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = reviewTable
        fields = [ 'DOCTORID', 'USERID', 'rating', 'reviewcomment', 'reviewtime']