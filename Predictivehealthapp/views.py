from datetime import date
from tracemalloc import Statistic
from django.shortcuts import render,redirect
from django.views import View

from Predictivehealthapp.form import *
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from django.contrib.auth.hashers import check_password
from django.db.models import Avg
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
                doc_count = DoctorTable.objects.filter(status=1).count()
                patient_count = bookinginfoTable.objects.count()
                return render(request,'administrator/dashboard.html',{'doc_count':doc_count,'patient_count':patient_count})
            if obj.type == 'doctor':
                return render(request,'doctor/doc-dash.html')
            else:
                return HttpResponse("User type not recognized")
        except LoginTable.DoesNotExist:
            messages.error(request,"Invalid username or password")
        return redirect('login')
        


class docreg(View):
    def get(self,request):
        return render(request,'administrator/doc-reg.html')
    def post(self,request):
        form=DocregForm(request.POST)
        # print(form)
        if form.is_valid():
             login_instance = LoginTable.objects.create(
                    type='doctor',
                    username=request.POST['username'],
                    password=request.POST['password']
                )
            #  print(login_instance)
                
                # Save the doctor details with reference to the created user
             reg_form = form.save(commit=False)
             reg_form.LOGINID = login_instance
             reg_form.status = 1
             reg_form.save()

        messages.success(request, "Registered successfully!")
        return redirect('viewdoctors')
        
class viewdoc(View):
    def get(self,request):
        obj=DoctorTable.objects.filter(status=1)
        obji = obj.filter(status=1)
        print("##################################################################",obj)
        
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
        messages.success(request, "Edit successfully!")
        return redirect('viewdoctors')
    
class deletedoc(View):
    def get(self,request,doc_id):
        obj=DoctorTable.objects.get(id=doc_id)
        # obj.delete()
        obj.status=0
        obj.save()
        return redirect('viewdoctors')

class dashboard(View):
     def get(self,request):
        doc_count = DoctorTable.objects.filter(status=1).count()
        patient_count = bookinginfoTable.objects.count()
        print("###################",doc_count)
        print("###################",patient_count)
        return render(request,'administrator/dashboard.html',{'doc_count':doc_count,'patient_count':patient_count})
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
            obj.status = "visited"
            obj.save(update_fields=['status']) 
        

        messages.success(request, "Added successfully!")
        return redirect('docviewappointment')
    
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
            messages.success(request, "Added successfully!")
        return redirect('docposts')

class patientoverview(View):
    def get(self,request):
        doc_obj = DoctorTable.objects.get(LOGINID__id=request.session.get('user_id'))
        upcoming_appointments = bookinginfoTable.objects.filter(DOCTORID=doc_obj, APPOINTMENTDATE__gte=date.today()).order_by('APPOINTMENTDATE')
        past_appointments = bookinginfoTable.objects.filter(DOCTORID=doc_obj, APPOINTMENTDATE__lt=date.today()).order_by('-APPOINTMENTDATE')

        listappo = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        }
        return render(request,'doctor/patient-overview.html',listappo)
    
class docdashboard(View):
    def get(self,request):
        return render(request,'doctor/doc-dashboard.html')
    
class docdash(View):
    def get(self,request):
        return render(request,'doctor/doc-dash.html')
    
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
    def get(self,request,lid):
        obj=prescriptionTable.objects.filter(APPOINTMENTID__id=lid)
        print(obj)
        return render(request,'doctor/view-prescriptions.html',{'obj':obj})
    
class docaddslot(View):
    def get(self,request):
        return render(request,'doctor/add-slots.html')
    def post(self,request):
        form = docaddslotForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            obj = DoctorTable.objects.get(LOGINID__id=request.session.get('user_id'))
            f.DOCTORID=obj
            f.save()
            return HttpResponse('''<script>alert(" Slot Created successfully!");window.location="/docaddslot"</script>''')
        
    
# //////////////////////////////////////////// API //////////////////////////////////////////////////    

class register(APIView):
    def post(self, request):
        print("###################",request.data)
        user_serial=UserSerializer(data=request.data)
        login_serial= LoginSerializer(data=request.data)
        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
       
            login_profile = login_serial.save(type='USER')
            user_serial.save(LOGINID=login_profile)
            return Response(user_serial.data, status=status.HTTP_201_CREATED)
        return Response({'login_error':login_serial.errors if not login_valid else None,
                         'user_error':user_serial.errors if not data_valid else None}, status=status.HTTP_400__BAD_REQUEST)
from django.http import JsonResponse
from django.views.generic import View
from .models import DoctorTable, medicineTable, bookinginfoTable, userTable
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.generic import View
from .models import DoctorTable, medicineTable, bookinginfoTable, userTable
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class DoctorDetailsView(APIView):
    @method_decorator(csrf_exempt)  # Optional: If you want to disable CSRF protection for this view
    def get(self, request, lid):

        # Get the doctor associated with this user (assuming a relationship exists)
        # doctor = get_object_or_404(DoctorTable, LOGINID=user.LOGINID)

        # Get the related booking info for this user and doctor
        bookings = bookinginfoTable.objects.filter(USERID__LOGINID__id=lid)
        bookings1 = bookinginfoTable.objects.filter(USERID__LOGINID__id=lid).first()
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",bookings1)

        # Format the medicines data for each booking
        medicine_list = []
        for booking in bookings:
            # Get associated medicines for this booking (prescription data)
            prescriptions = prescriptionTable.objects.filter(APPOINTMENTID=booking)

            for prescription in prescriptions:
                medicine_data = {
                    "NAME": prescription.medicine_name,
                    "DESCRIPTION": prescription.diagnosis,  # Assuming description is stored in diagnosis field
                    "EXPIRY": prescription.expirydate.strftime("%Y-%m-%d") if prescription.expirydate else "Not available",
                    "DOSE": prescription.medicine_dosage,
                    "remark":prescription.remark,
                    "isssuedate":prescription.issueddate.strftime("%Y-%m-%d") if prescription.issueddate else "Not available",
                }
                medicine_list.append(medicine_data)

        # Format the doctor data and include the associated medicines
        doctor_data = {
            "DOCTOR DETAILS": {
                "NAME": bookings1.DOCTORID.Name,
                # "CREATED AT": bookings1.created_at.strftime("%Y-%m-%d") if bookings1.created_at else "Not available",
            },
            "MEDICINES": medicine_list
        }
        print(doctor_data)
        # Return the data as JSON
        return JsonResponse([doctor_data], safe=False)

class LoginPage(APIView):
    def post(self, request):
        print("####################")
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")
        print("$$$$$$$-username-----",username)
        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(username=username).first()
        print("&&&&&&&&&&&&&&&-userinlogintable-------", t_user)
        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # Check password using check_password
        else:
        # Successful login response
            response_dict["message"] = "success"
            response_dict["login_id"] = t_user.id

            return Response(response_dict, status=HTTP_200_OK)


class userviewDoc(APIView):
    def get(self, request):
        doc_obj = DoctorTable.objects.all()
        viewDoc_serial = viewDocSerializer(doc_obj, many = True)
        print("------------>", viewDoc_serial.data)
        return Response(viewDoc_serial.data)
    
class userViewPrescription(APIView):
    def get(self, request, lid):
        lid_list =[]
        prescription_obj = bookinginfoTable.objects.filter(USERID__LOGINID_id=lid).order_by('-APPOINTMENTDATE')
        for i in prescription_obj:
            lid_list.append(i.USERID__LOGINID_id)
        obj = prescriptionTable.objects.filter(APPOINTMENTID__USERID__LOGINID__in=lid_list)
        viewPrescription_serial = viewPrescriptionSerializer(prescription_obj, many = True)
        print("------------>", viewPrescription_serial.data)
        return Response(viewPrescription_serial.data)


class userViewpost(APIView):
    def get(self, request):
        post_obj = postsTable.objects.all().order_by('-createdat')
        viewPost_serial = viewPostSerializer(post_obj, many = True)
        print("------------>", viewPost_serial.data)
        
        return Response(viewPost_serial.data)


class userViewnotification(APIView):
    def get(self, request):
        notification_obj = NotificationTable.objects.all().order_by('-createdat')
        viewNotification_serial = viewNotificationSerializer(notification_obj, many = True)
        return Response(viewNotification_serial.data)


class userViewappointment(APIView):
    def get(self, request):
        print("###################", request.data)
        appointment_obj = bookinginfoTable.objects.filter(USERID__LOGINID_id=request.data['USERID']).order_by('-APPOINTMENTDATE')
        viewAppointment_serial = viewAppointmentSerializer(appointment_obj, many = True)
        print("------------>", viewAppointment_serial.data)

        return Response(viewAppointment_serial.data)


class userViewSlot(APIView):
    def get(self, request):
        slot_obj = SlotTable.objects.all()
        viewslot_serial = viewSlotSerializer(slot_obj, many = True)
        print("------------>", viewslot_serial.data)
        
        return Response(viewslot_serial.data)


    

import google.generativeai as genai
genai.configure(api_key="AIzaSyBfA-PALoDy3VxF5rIHJ03Uz0eYLzDcmZM")
class chatbotapi(APIView):
    def post(self, request, lid):
        # Get query from the user input
        user_query = request.data.get('query', '')

        # Default response if no input
        response_data = {
            'chatbot_response': "",
            "chat_history": [],   # This will store the chatbot-like response
        }


        # Construct the prompt using the filtered data (ensure it's only from the models)
        print(user_query)
        prompt = (
            f"User Query: {user_query}. "
            f"Provide the response based on above data"
        )

        try:
            # Call Gemini API to generate the response
            gemini_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            gemini_chatbot_response = gemini_response.text.strip()
            print(user_query)
            ChatHistory.objects.create(
                user_query=user_query,
                chatbot_response=gemini_chatbot_response,
                USERID=userTable.objects.get(LOGINID_id=lid)
            )

            # Update response data with the chatbot response
            response_data['chatbot_response'] = gemini_chatbot_response
                        # Retrieve the chat history
            chat_history = ChatHistory.objects.order_by("-timestamp").values(
                "user_query", "chatbot_response", "timestamp"
            )
            response_data.update(
                {

                    "chatbot_response": gemini_chatbot_response,
                    "chat_history": list(chat_history),
                }
            )
            print(response_data)

            # f = ChatHistory(USERID=userTable.objects.get(LOGINID_id=lid))
            # f.save()
            # Return the chatbot-like response with the itinerary data
            return Response(response_data, status=201)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class bookslot(APIView):
    def post(self, request):
        print("###################",request.data)
        data={}
        data=request.data
        patient=userTable.objects.get(LOGINID__id=request.data['loginid'])
        data['PATIENTID']=patient.id
        user_serial=viewSlotSerializer(data=data)

        if user_serial.is_valid():
            user_serial.save()
            return Response(user_serial.data, status=status.HTTP_201_CREATED)
        return Response({'login_error':user_serial.errors}, status=status.HTTP_400__BAD_REQUEST)
    

class AppointmentCreateView(APIView):
    def post(self, request, LID):
        serializer = AppointmentSerializer(data=request.data)
        user_obj = userTable.objects.get(LOGINID_id=LID)
        doctor_obj = DoctorTable.objects.get(id=request.data.get('DOCTORID'))
        print('------------->', doctor_obj)
        print("######################",request.data)
        if serializer.is_valid():
            serializer.save(USERID=user_obj, DOCTORID=doctor_obj, status='pending')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import string
from .models import PasswordResetToken

# Generate a random password reset token
class ForgotPasswordView(APIView):

    @staticmethod
    def generate_reset_token():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def post(self, request):
        email = request.data.get('email')

        if email:
            try:
                user = userTable.objects.get(email=email)
                passw=LoginTable.objects.get(id=user.LOGINID.id)
                send_mail(
                'Password Reset Request',
                f'Your password {passw.password}',
                'predictivehealthcare3@gmail.com',  # Update with your email
                [email],
                fail_silently=False,
            )

                return JsonResponse({'message': 'Password reset email sent! Check your inbox.'}, status=200)
            except userTable.DoesNotExist:
                return JsonResponse({'message': 'Email not found in our system.'}, status=400)
            
        else:
            return JsonResponse({'message': 'Email is required.'}, status=400)




class UserProfileView(APIView):
    def get(self, request, lid):
        """Retrieve user profile details"""
        try:
            user_p = LoginTable.objects.get(id=lid)
            #print("***************************--->",user_p.username)
            user = userTable.objects.get(email=user_p.username)
            print("***************************--->",user.firstname)

            return Response(
                {
                    "username": f"{user.firstname} {user.lastname}".strip(),
                    "email": user.email,
                    
                },
                status=status.HTTP_200_OK,
            )
        except userTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ReviewView(APIView):
    def post(self, request, lid):
        serializer = ReviewSerializer(data=request.data)
        user_obj = userTable.objects.get(LOGINID_id=lid)
        doctor_obj = DoctorTable.objects.get(id=request.data.get('doctor_id'))
        print('------------->', doctor_obj)
        print("######################",request.data)
        if serializer.is_valid():
            serializer.save(USERID=user_obj, DOCTORID=doctor_obj, reviewcomment=request.data.get('review'))
            self.update_doctor_rating(doctor_obj)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update_doctor_rating(self, doctor_obj):
        """Calculate the new average rating and update the DoctorTable"""
        reviews = reviewTable.objects.filter(DOCTORID=doctor_obj)
        average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$----Average rating:', average_rating)
        
        # Update doctor's rating
        doctor_obj.avg_rating = round(average_rating, 2)
        doctor_obj.save()
    
class UserViewreview(APIView):
    def get(self, request, doc_id):
        """
        Fetch all reviews for a specific doctor.
        """
        try:
            reviews = reviewTable.objects.filter(DOCTORID_id=doc_id).order_by('-reviewtime')  # Newest first
            
            serializer = ReviewSerializer(reviews, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)