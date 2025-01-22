from django.forms import ModelForm

from .models import *


class DocregForm(ModelForm):
    class Meta:
        model=DoctorTable
        fields=['Name','specialization','qualification','phone','email']
class UpdatedocForm(ModelForm):
     class Meta:
        model=DoctorTable
        fields=['Name','specialization','qualification','phone','email']
class AddprescriptionForm(ModelForm):
    class Meta:
        model=prescriptionTable
        fields=['diagnosis','medicine_name','medicine_dosage','medicine_itd','expirydate','remark']
class AddpostForm(ModelForm):
    class Meta:
        model=postsTable
        fields=['title','category','content','filepost']
class SendnotificationForm(ModelForm):
    class Meta:
        model=NotificationTable
        fields=['content','attachement']
class docaddslotForm(ModelForm):
    class Meta:
        model = SlotTable
        fields = ['date','time']