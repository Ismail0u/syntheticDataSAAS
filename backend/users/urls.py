from django.urls import path
# Import views from the Simple JWT package
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from .views import RegisterView, ProfileView

# Defines all authentication endpoints under the '/api/auth/' root (assuming inclusion in project urls.py)
urlpatterns = [
    # --- Authentication Endpoints (JWT Flow) ---
    
    # POST /api/auth/register/
    # Handles new user sign-up and returns JWT tokens upon success.
    path('register/', RegisterView.as_view(), name='register'),
    
    # POST /api/auth/login/ (or token/)
    # Uses Django Rest Framework Simple JWT's built-in view to handle email/password login, 
    # generating the initial access and refresh tokens.
    path('login/', TokenObtainPairView.as_view(), name='login'),
    
    # POST /api/auth/token/refresh/
    # Uses the Refresh Token to securely obtain a new Access Token without re-logging in.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- User Profile Endpoint ---
    
    # GET/PUT /api/auth/profile/
    # Allows the authenticated user to view or update their profile details.
    path('profile/', ProfileView.as_view(), name='profile'),
]