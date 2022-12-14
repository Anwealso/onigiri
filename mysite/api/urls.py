# api/urls.py
from django.urls import include, path
from rest_framework import routers

from .views import *


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'events', EventViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'groups', GroupViewSet)

# Set up the url routing for the API
urlpatterns = [
    path('get-survey', GetSurvey.as_view()),
    path('submit-survey', SubmitSurvey.as_view()),
    path('submit-attendance', SubmitAttendance.as_view()),
    path('check-attendance', CheckAttendance.as_view()),
    path('remove-attendance', RemoveAttendance.as_view()),

    path('get-billboard', GetBillboard.as_view()),

    path('', include(router.urls)),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('test/', testEndPoint, name='test'),

    path('results/', ExportCSVSurvey.as_view())
]