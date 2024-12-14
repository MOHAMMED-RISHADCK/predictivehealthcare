from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.



class login(View):
    def get(self,request):
        return render(request,'administrator/login.html')
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']

        try:
            obj = LoginTable.objects.get(username=username,password=password)
            request.session['user_id'] = obj.id
            if obj.type == 'admin':
                return render(request,'administrator/dashboard.html')
            if obj.type == 'doctor':
                return render(request,'doctor/doc-dashboard.html')
            else:
                return HttpResponse("User type not recognized")
        except LoginTable.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect(login)

class administratordashboard(View):
    def get(self,request):
        return render(request,'administrator/administrator-dashboard.html')
class docreg(View):
    def get(self,request):
        return render(request,'administrator/doc-reg.html')
class editdoc(View):
    def get(self,request):
        return render(request,'administrator/edit-doc.html')
class forgotpass(View):
    def get(self,request):
        return render(request,'administrator/forgot-pass.html')

class viewdoc(View):
    def get(self,request):
        return render(request,'administrator/view-doc.html')
class viewappointment(View):
    def get(self,request):
        return render(request,'administrator/view-apppointment.html')
class addprescription(View):
    def get(self,request):
        return render(request,'doctor/add-presription.html')
class docaddpost(View):
    def get(self,request):
        return render(request,'doctor/doc-add-post.html')
class docdashboard(View):
    def get(self,request):
        return render(request,'doctor/doc-dashboard.html')
class docposts(View):
    def get(self,request):
        return render(request,'doctor/doc-posts.html')
class docsendnotification(View):
    def get(self,request):
        return render(request,'doctor/doc-send-notification.html')
class docviewapppointment(View):
    def get(self,request):
        return render(request,'doctor/view-appo-doc.html')
class viewprescription(View):
    def get(self,request):
        return render(request,'doctor/view-prescription.html')









    
    
    