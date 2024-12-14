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
    email=models.CharField(max_length=20,null=True,blank=True)

class medicineTable(models.Model): 
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True) 
    medicinename=models.CharField(max_length=20,null=True,blank=True)
    brandname=models.CharField(max_length=20,null=True,blank=True)
    category=models.CharField(max_length=20,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    dosageform=models.CharField(max_length=20,null=True,blank=True)
    strength=models.CharField(max_length=20,null=True,blank=True)
    expdate=models.CharField(max_length=20,null=True,blank=True)
class userTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    firstname=models.CharField(max_length=20,null=True,blank=True)
    lastname=models.CharField(max_length=20,null=True,blank=True)
    dob=models.CharField(max_length=20,null=True,blank=True)
    mobile=models.BigIntegerField(null=True,blank=True)
    email=models.CharField(max_length=20,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    city=models.CharField(max_length=20,null=True,blank=True)
    state=models.CharField(max_length=20,null=True,blank=True)
class bookinginfoTable(models.Model):
    USERID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True,related_name='userid')
    DOCTORID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True,related_name='doctorid')
    APPOINTMENTDATE=models.CharField(max_length=100,null=True,blank=True)
    APPOINTMENTTIME=models.CharField(max_length=100,null=True,blank=True)
    visitReason=models.CharField(max_length=300,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
class prescriptionTable(models.Model):
    APPOINTMENTID=models.ForeignKey(bookinginfoTable,on_delete=models.CASCADE,null=True,blank=True)
    prescription=models.CharField(max_length=20,null=True,blank=True)
    issueddate=models.CharField(max_length=20,null=True,blank=True)
    expirydate=models.CharField(max_length=20,null=True,blank=True)
    remark=models.CharField(max_length=20,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
class reviewTable(models.Model):
    USERID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True,related_name='USERID')
    DOCTORID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True,related_name='DOCTORID')
    rating=models.CharField(max_length=20,null=True,blank=True)
    reviewcomment=models.CharField(max_length=20,null=True,blank=True)
    reviewtime=models.DateField(auto_now_add=True,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
class postsTable(models.Model):
    DOCTORID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=20,null=True,blank=True)
    content=models.CharField(max_length=20,null=True,blank=True)
    imgurl=models.FileField(upload_to='posts',null=True,blank=True)
    tags=models.CharField(max_length=20,null=True,blank=True)
    createdat=models.DateField(auto_now_add=True,null=True,blank=True)
    updatedat=models.DateTimeField(auto_now=True,null=True,blank=True)
    status=models.CharField(max_length=20,null=True,blank=True)
    



    
    
    
    


 

