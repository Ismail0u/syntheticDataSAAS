from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from datetime import date
import os

from .models import Schema, GeneratedDataset
from .serializers import SchemaSerializer, GenerateDataSerializer, GeneratedDatasetSerializer
from .services.data_generator import DataGenerator
from .services.file_exporter import FileExporter


# --- DATA GENERATION ENDPOINT ---
class GenerateDataView(APIView):
    """
    Main view for generating synthetic data.
    Endpoint: POST /api/generate/
    
    This view handles input validation, quota checks, data generation, 
    file export, schema saving, and history logging.
    """
    # Requires the user to be authenticated via JWT (or session)
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Initialize serializer with request data for validation
        serializer = GenerateDataSerializer(data=request.data)
        
        # Validate the incoming data against defined constraints (e.g., max rows, format choices)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract validated data
        schema = serializer.validated_data['schema']
        rows = serializer.validated_data['rows']
        file_format = serializer.validated_data['format']
        save_schema = serializer.validated_data.get('save_schema', False)
        schema_name = serializer.validated_data.get('schema_name', '')
        
        user = request.user
        
        # Define quota limits based on the user's subscription plan
        quota_limits = {
            'free': 500,
            'pro': 50000,
            'enterprise': 999999999  # unlimited
        }
        
        # Reset the daily quota if the last reset date is before today
        if user.last_quota_reset != date.today():
            user.daily_quota_used = 0
            user.last_quota_reset = date.today()
            user.save()
        
        # Check if the requested number of rows exceeds the user's available quota
        max_quota = quota_limits.get(user.plan, 500)
        if user.daily_quota_used + rows > max_quota:
            return Response({
                'error': f'Quota journalier dépassé. Plan {user.plan}: {max_quota} lignes/jour. Utilisé: {user.daily_quota_used}'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        
        # --- DATA GENERATION ---
        try:
            # Instantiate the generator service (using 'fr_FR' locale as chosen)
            generator = DataGenerator(locale='fr_FR')
            data = generator.generate_dataset(schema, rows)
        except Exception as e:
            return Response({'error': f'Erreur lors de la génération: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        # --- DATA EXPORT ---
        exporter = FileExporter()
        file_content = None
        content_type = 'application/json'
        file_extension = file_format
        
        try:
            # Calls the appropriate export method based on the requested format
            if file_format == 'json':
                file_content = exporter.to_json(data)
                content_type = 'application/json'
            elif file_format == 'csv':
                file_content = exporter.to_csv(data)
                content_type = 'text/csv'
            elif file_format == 'xlsx':
                file_content = exporter.to_excel(data)
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif file_format == 'sql':
                file_content = exporter.to_sql(data)
                content_type = 'text/plain'
            elif file_format == 'xml':
                file_content = exporter.to_xml(data)
                content_type = 'application/xml'
        except Exception as e:
            return Response({'error': f'Erreur lors de l\'export: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        # --- SAVE & HISTORY LOGGING ---
        
        # Save the schema if the 'save_schema' flag is true and a name is provided
        if save_schema and schema_name:
            Schema.objects.create(
                user=user,
                name=schema_name,
                schema_json=schema
            )
        
        # Record the generation event in the user's history
        dataset = GeneratedDataset.objects.create(
            user=user,
            schema_json=schema,
            nb_rows=rows,
            file_format=file_format,
            file_path=''  # Placeholder: actual file storage logic would go here
        )
        
        # Update the user's daily quota usage
        user.daily_quota_used += rows
        user.save()
        
        
        # --- RETURN RESPONSE (FILE DOWNLOAD) ---
        
        # Create an HTTP response with the generated file content
        response = HttpResponse(file_content, content_type=content_type)
        # Set the Content-Disposition header to prompt a file download
        response['Content-Disposition'] = f'attachment; filename="synthetic_data_{dataset.id}.{file_extension}"'
        
        return response


# --- SCHEMA MANAGEMENT ENDPOINTS ---
class SchemaListCreateView(generics.ListCreateAPIView):
    """
    View to list all saved schemas for the authenticated user and create new ones.
    Endpoint: GET/POST /api/schemas/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SchemaSerializer
    
    def get_queryset(self):
        # Ensures only schemas owned by the currently logged-in user are returned
        return Schema.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically associates the newly created schema with the current user
        serializer.save(user=self.request.user)


class SchemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific user schema by ID.
    Endpoint: GET/PUT/DELETE /api/schemas/<id>/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SchemaSerializer
    
    def get_queryset(self):
        # Ensures users can only access their own schemas
        return Schema.objects.filter(user=self.request.user)


# --- DATASET HISTORY ENDPOINTS ---
class DatasetHistoryView(generics.ListAPIView):
    """
    View to retrieve the history of all generated datasets for the user.
    Endpoint: GET /api/history/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratedDatasetSerializer
    
    def get_queryset(self):
        # Returns all generated datasets records belonging to the current user
        return GeneratedDataset.objects.filter(user=self.request.user)


class DatasetDeleteView(generics.DestroyAPIView):
    """
    View to delete a specific generated dataset record from the history.
    Endpoint: DELETE /api/history/<id>/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratedDatasetSerializer
    
    def get_queryset(self):
        # Ensures users can only delete their own dataset history records
        return GeneratedDataset.objects.filter(user=self.request.user)