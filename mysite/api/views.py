from django.shortcuts import render
from django.utils.timezone import make_aware
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import *
from .serializers import *

import logging
from datetime import datetime
import csv
from django.http import HttpResponse

# Authentication Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# ---------------------------------------------------------------------------- #
#            VIEWS TO LIST OUT ALL THE OBJECTS OF A PARTICULAR CLASS           #
# ---------------------------------------------------------------------------- #
class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    # permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Events to be viewed or edited.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Events to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# ---------------------------------------------------------------------------- #
#                             VIEWS FOR DATA INPUT                             #
# ---------------------------------------------------------------------------- #

class GetSurvey(APIView):
    serializer_class = SurveySerializer
    lookup_url_kwarg = 'id'

    def get(self, request, format=None):
        survey_id = request.GET.get(self.lookup_url_kwarg)
        if survey_id != None:
            try:
                survey = Survey.objects.get(id=survey_id)
                data = SurveySerializer(survey).data
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response({'Survey Not Found': 'Invalid Survey ID.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Survey ID paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class SubmitSurvey(APIView):
    def post(self, request, format=None):
        # Check the db to see that the requested survey exists
        survey_id = request.data.get("surveyId")
        if survey_id != None:
            survey_instances = Survey.objects.filter(id=survey_id)
            if len(survey_instances) > 0:
                survey_instance = survey_instances[0]

                sub_time = make_aware(datetime.now())
                logging.debug(sub_time)

                for question in request.data.get("questions"):
                    question_instance = Question.objects.filter(id=question["id"])[0]
                    selected_choice_instance = Choice.objects.filter(id=question["selectedChoiceId"])[0]

                    # Save the survey results to the database
                    result = Result(question_id=question_instance, choice_id=selected_choice_instance, survey_id=survey_instance, sub_time=sub_time)
                    
                    logging.debug(result)
                    logging.debug(result.sub_time)
                    result.save()

                return Response({'message': 'Survey Submitted!'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Survey ID'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Invalid post data, did not find a survey ID'}, status=status.HTTP_400_BAD_REQUEST)

class SubmitAttendance(APIView):
    def post(self, request, format=None):
        user_instance = User.objects.filter(id=request.data.get("user"))[0]
        event_instance = Event.objects.filter(id=request.data.get("event"))[0]

        attendance_check = Attendance.objects.filter(user=request.data.get("user"), event=request.data.get("event"))

        if len(attendance_check) > 0:
            return Response({'message': 'Already going'}, status=status.HTTP_400_BAD_REQUEST)

        result = Attendance(user = user_instance, event = event_instance)
        result.save()

        return Response({'message': 'Survey Submitted!'}, status=status.HTTP_200_OK)


class CheckAttendance(APIView):
    def post(self, request, format=None):
        user_instance = User.objects.filter(id=request.data.get("user"))[0]
        event_instance = Event.objects.filter(id=request.data.get("event"))[0]

        attendance_check = Attendance.objects.filter(user=request.data.get("user"), event=request.data.get("event"))

        if len(attendance_check) > 0:
            return Response({'message': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 0}, status=status.HTTP_200_OK)


class RemoveAttendance(APIView):
    def post(self, request, format=None):

        user_instance = User.objects.filter(id=request.data.get("user"))[0]
        event_instance = Event.objects.filter(id=request.data.get("event"))[0]

        Attendance.objects.filter(user=request.data.get("user"), event=request.data.get("event")).delete()

        return Response({'message': 'removed'}, status=status.HTTP_200_OK)


class GetBillboard(APIView):
    lookup_url_kwarg = 'id'

    def get(self, request, format=None):
        billboard_id = int(request.GET.get(self.lookup_url_kwarg))

        if billboard_id != None:
            if billboard_id == 1:   
                # Do billboard 1 logic...             
                logging.debug(Result.objects.filter(question_id=1))
                logging.debug(Result.objects.filter(question_id=1))

                num_red = len(Result.objects.filter(question_id=1).filter(choice_id=Choice.objects.filter(question_id=1).filter(option="4: Above Average")[0].id))
                num_blue = len(Result.objects.filter(question_id=1).filter(choice_id=Choice.objects.filter(question_id=1).filter(option="2: Below Average")[0].id))
                if num_red + num_blue == 0:
                    percentage_red = 0
                else:
                    percentage_red = num_red / (num_red + num_blue)

                # Package the data into the required json string format and send
                return Response({'text': percentage_red}, status=status.HTTP_200_OK)

            elif billboard_id == 2:
                # Do billboard 2 logic...
                num_red = len(Result.objects.filter(question_id=1).filter(choice_id=Choice.objects.filter(question_id=1).filter(option="Red")[0].id))
                num_blue = len(Result.objects.filter(question_id=1).filter(choice_id=Choice.objects.filter(question_id=1).filter(option="Blue")[0].id))
                if num_red + num_blue == 0:
                    percentage_red = 0
                else:
                    percentage_blue = num_blue / (num_red + num_blue)
                    
                # Package the data into the required json string format and send
                return Response({'text': percentage_blue}, status=status.HTTP_200_OK)

            else:
                return Response({'Billboard Not Found': 'Invalid Billboard ID.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Billboard ID paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ExportCSVSurvey(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="responsedataexport.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'QuestionID', 'ChoiceID', 'SurveyID', 'Submission Time'])
        Results = Result.objects.all()
        results_list = Results.values_list("id", "question_id", "choice_id", "survey_id", "sub_time")
        for result in results_list:
            writer.writerow(result)

        return response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


