from django.db import models

# Create your models here.
class LoginTable(models.Model):
    username=models.CharField(max_length=20,null=True,blank=True)
    password=models.CharField(max_length=20,null=True,blank=True)
    type=models.CharField(max_length=20,null=True,blank=True)
class DoctorTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=20,null=True,blank=True)
    specialization=models.CharField(max_length=20,null=True,blank=True)
    qualification=models.CharField(max_length=20,null=True,blank=True)
    phone=models.BigIntegerField(null=True,blank=True)
    email=models.CharField(max_length=255,null=True,blank=True)

class medicineTable(models.Model): 
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True) 
    medicinename=models.CharField(max_length=20,null=True,blank=True)
    brandname=models.CharField(max_length=20,null=True,blank=True)
    category=models.CharField(max_length=20,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    dosageform=models.CharField(max_length=20,null=True,blank=True)
    strength=models.CharField(max_length=20,null=True,blank=True)
    expdate=models.DateField(max_length=20,null=True,blank=True)
class userTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    firstname=models.CharField(max_length=20,null=True,blank=True)
    lastname=models.CharField(max_length=20,null=True,blank=True)
    dob=models.CharField(max_length=20,null=True,blank=True)
    gender=models.CharField(max_length=20,null=True,blank=True)
    mobile=models.BigIntegerField(null=True,blank=True)
    email=models.CharField(max_length=20,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    password=models.CharField(max_length=50,null=True,blank=True)
    state=models.CharField(max_length=20,null=True,blank=True)
class bookinginfoTable(models.Model):
    USERID=models.ForeignKey(userTable,on_delete=models.CASCADE,null=True,blank=True,related_name='userid')
    DOCTORID=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True,)
    patient_name=models.CharField(max_length=300,null=True,blank=True)
    patient_age=models.CharField(max_length=300,null=True,blank=True)
    patient_height=models.CharField(max_length=300,null=True,blank=True)
    patient_weight=models.CharField(max_length=300,null=True,blank=True)
    patient_addr=models.CharField(max_length=300,null=True,blank=True)
    APPOINTMENTDATE=models.DateField(null=True,blank=True)
    APPOINTMENTTIME=models.TimeField(null=True,blank=True)
    visitReason=models.CharField(max_length=300,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
class prescriptionTable(models.Model):
    APPOINTMENTID=models.ForeignKey(bookinginfoTable,on_delete=models.CASCADE,null=True,blank=True)
    diagnosis=models.CharField(max_length=20,null=True,blank=True)
    medicine_name=models.CharField(max_length=20,null=True,blank=True)
    medicine_dosage=models.CharField(max_length=20,null=True,blank=True)
    medicine_itd=models.CharField(max_length=20,null=True,blank=True)
    issueddate=models.DateField(auto_now_add=True,null=True,blank=True)
    expirydate=models.DateField(null=True,blank=True)
    remark=models.CharField(max_length=20,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
class reviewTable(models.Model):
    USERID=models.ForeignKey(userTable,on_delete=models.CASCADE,null=True,blank=True,related_name='USERID')
    DOCTORID=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True,related_name='DOCTORID')
    rating=models.CharField(max_length=20,null=True,blank=True)
    reviewcomment=models.CharField(max_length=20,null=True,blank=True)
    reviewtime=models.TimeField(auto_now_add=True,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
class postsTable(models.Model):
    DOCTORID=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    category=models.CharField(max_length=100,null=True,blank=True)
    content=models.CharField(max_length=100,null=True,blank=True)
    filepost=models.FileField(upload_to='posts',null=True,blank=True)
    createdat=models.DateField(auto_now_add=True,null=True,blank=True)
    updatedat=models.DateTimeField(auto_now=True,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
    
class NotificationTable(models.Model):
    DOCTORID=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    PATIENTID=models.ForeignKey(userTable,on_delete=models.CASCADE,null=True,blank=True)
    content=models.CharField(max_length=100,null=True,blank=True)
    attachement=models.FileField(upload_to='posts',null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
    createdat=models.DateField(auto_now_add=True,null=True,blank=True)


    
class SlotTable(models.Model):
    DOCTORID=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    PATIENTID=models.ForeignKey(userTable,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    time=models.TimeField(null=True,blank=True)
    createdat=models.DateField(auto_now_add=True,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
    token = models.CharField(max_length=50, unique=True, blank=True, null=True)  # New field for token

    def save(self, *args, **kwargs):
        if not self.token and self.DOCTORID and self.date:
            # Count the number of slots for this doctor on the given date
            slot_count = SlotTable.objects.filter(DOCTORID=self.DOCTORID, date=self.date).count() + 1
            
            # Generate token using doctor ID, date, and slot count
            self.token = f"D{self.DOCTORID.id}-{self.date.strftime('%Y%m%d')}-{slot_count}"
        
        super(SlotTable, self).save(*args, **kwargs)  # Call the parent class's save method


    
class ChatHistory(models.Model):
    user_query = models.TextField()  # User's query
    chatbot_response = models.TextField()  # Chatbot's response
    timestamp = models.DateTimeField(auto_now_add=True)



    
    
    


 

