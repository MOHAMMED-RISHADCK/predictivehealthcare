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

class DoctorDetailsView(View):
    @method_decorator(csrf_exempt)  # Optional: If you want to disable CSRF protection for this view
    def get(self, request, lid):

        # Get the doctor associated with this user (assuming a relationship exists)
        # doctor = get_object_or_404(DoctorTable, LOGINID=user.LOGINID)

        # Get the related booking info for this user and doctor
        bookings = bookinginfoTable.objects.filter(USERID__LOGINID__id=lid)
        bookings1 = bookinginfoTable.objects.filter(USERID__LOGINID__id=lid).first()
        print(bookings)

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
        print("$$$$$$$$$$$$$$",username)
        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(username=username).first()
        print("%%%%%%%%%%%%%%%%%%%%", t_user)
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
        prescription_obj = bookinginfoTable.objects.filter(USERID__LOGINID_id=lid)
        for i in prescription_obj:
            lid_list.append(i.USERID__LOGINID_id)
        obj = prescriptionTable.objects.filter(APPOINTMENTID__USERID__LOGINID__in=lid_list)
        viewPrescription_serial = viewPrescriptionSerializer(prescription_obj, many = True)
        print("------------>", viewPrescription_serial.data)
        return Response(viewPrescription_serial.data)


class userViewpost(APIView):
    def get(self, request):
        post_obj = postsTable.objects.all()
        viewPost_serial = viewPostSerializer(post_obj, many = True)
        print("------------>", viewPost_serial.data)
        
        return Response(viewPost_serial.data)


class userViewnotification(APIView):
    def get(self, request):
        notification_obj = NotificationTable.objects.all()
        viewNotification_serial = viewNotificationSerializer(notification_obj, many = True)
        return Response(viewNotification_serial.data)


class userViewappointment(APIView):
    def get(self, request):
        appointment_obj = bookinginfoTable.objects.all()
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
    def post(self, request):
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
    def post(self, request, *args, **kwargs):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)