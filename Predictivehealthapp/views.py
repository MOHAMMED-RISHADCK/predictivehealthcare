from django.shortcuts import render,redirect
from django.views import View

from Predictivehealthapp.form import *
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
        


class docreg(View):
    def get(self,request):
        return render(request,'administrator/doc-reg.html')
    def post(self,request):
        form=DocregForm(request.POST)
        print(form)
        if form.is_valid():
             login_instance = LoginTable.objects.create(
                    type='doctor',
                    username=request.POST['username'],
                    password=request.POST['password']
                )
             print(login_instance)
                
                # Save the shop details with reference to the created user
             reg_form = form.save(commit=False)
             reg_form.LOGINID = login_instance
             reg_form.save()

        return HttpResponse('''<script>alert("Registered successfully!");window.location="/viewdoctors"</script>''')
        
class viewdoc(View):
    def get(self,request):
        obj=DoctorTable.objects.all()
        print(obj)
        return render(request,'administrator/view-doc.html',{'val':obj})
        
class editdoc(View):
    def get(self,request,doc_id):
        obj = DoctorTable.objects.get(id=doc_id)
        print(obj)
        return render(request, 'administrator/edit-doc.html', {'val': obj})


    def post(self,request,doc_id):
        obj = DoctorTable.objects.get(id=doc_id)
        form = UpdatedocForm(request.POST,instance=obj)

        if form.is_valid():
            form.save()
        return HttpResponse('''<script>alert("Updated successfully!");window.location="/"</script>''')
    
class deletedoc(View):
    def get(self,request,doc_id):
        obj=DoctorTable.objects.get(id=doc_id)
        obj.delete()
        return redirect('viewdoctors')

class dashboard(View):
     def get(self,request):
        return render(request,'administrator/dashboard.html')
class administratordashboard(View):
    def get(self,request):
        return render(request,'administrator/administrator-dashboard.html')


class forgotpass(View):
    def get(self,request):
        return render(request,'administrator/forgot-pass.html')


class viewappointment(View):
    def get(self,request):
        obj=bookinginfoTable.objects.all()
        return render(request,'administrator/view-appointment.html',{'obj':obj})
    

class addprescription(View):
    def get(self,request, b_id):
        obj=bookinginfoTable.objects.get(id=b_id)
        return render(request,'doctor/add-prescription.html',{'obj':obj})
    def post(self,request,b_id):
        obj = bookinginfoTable.objects.get(id=b_id)
        form = AddprescriptionForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.APPOINTMENTID=obj
            f.save()

        return HttpResponse('''<script>alert("Updated successfully!");window.location="/docviewappointment"</script>''')
    
class docaddpost(View):
    def get(self,request):
        return render(request,'doctor/doc-add-post.html')
    def post(self,request):
        form = AddpostForm(request.POST,request.FILES)
        print("lllllllll")
        if form.is_valid():
            print("hhhh")
            f=form.save(commit=False)
            obj = DoctorTable.objects.get(LOGINID__id=request.session.get('user_id'))
            f.DOCTORID=obj
            f.save()
            return HttpResponse('''<script>alert("Created successfully!");window.location="/docposts"</script>''')
    
class docdashboard(View):
    def get(self,request):
        return render(request,'doctor/doc-dashboard.html')
    
class docposts(View):
    def get(self,request):
        doc_obj=DoctorTable.objects.get(LOGINID_id=request.session['user_id'])
        obj=postsTable.objects.filter(DOCTORID_id=doc_obj.id)
        return render(request,'doctor/doc-posts.html',{'obj':obj})
    
class docsendnotification(View):
    def get(self,request):
        obj=bookinginfoTable.objects.filter(DOCTORID__LOGINID_id=request.session['user_id'],status="approve")
        return render(request,'doctor/doc-send-notification.html',{'obj':obj})
    def post(self,request):
        form = SendnotificationForm(request.POST,request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            doc_obj = DoctorTable.objects.get(LOGINID__id=request.session.get('user_id'))
            user_id=request.POST['p_id']
            user_obj = userTable.objects.get(id=user_id)
            print("^^^^^^^^^^^^^^^^^^", user_obj)
            f.DOCTORID=doc_obj
            f.PATIENTID=user_obj
            f.save()
            return HttpResponse('''<script>alert("Send successfully!");window.location="/docsendnotification"</script>''')
    
    
class docviewapppointment(View):
    def get(self,request):
        doc_obj=DoctorTable.objects.get(LOGINID_id=request.session['user_id'])
        obj=bookinginfoTable.objects.filter(DOCTORID_id=doc_obj.id)
        return render(request,'doctor/view-appo-doc.html',{'obj':obj})

class viewprescription(View):
    def get(self,request,p_id):
        obj=prescriptionTable.objects.filter(APPOINTMENTID__id=p_id)
        print(obj)
        return render(request,'doctor/view-prescriptions.html',{'obj':obj})









    
    
    