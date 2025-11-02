from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    View for registering a new user.
    Endpoint: POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Allow anyone (unauthenticated users) to access this view
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Custom creation method to generate and return JWT tokens upon successful registration.
        """
        # Validate data (passwords match, email unique, etc.)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # --- JWT Token Generation ---
        # Get the RefreshToken object for the newly created user
        refresh = RefreshToken.for_user(user)

        # Return the user data along with the access and refresh tokens
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    View for viewing and modifying the authenticated user's profile information.
    Endpoint: GET/PUT /api/auth/profile/
    """
    permission_classes = [IsAuthenticated] # Only authenticated users with a valid access token can access this view
    serializer_class = UserSerializer
    
    def get_object(self):
        """
        Ensures that the user can only retrieve/update their own profile data.
        """
        # Return the user object associated with the current request
        return self.request.user