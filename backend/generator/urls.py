from django.urls import path
from .views import (
    GenerateDataView,      # Handles POST request for synthetic data generation
    SchemaListCreateView,  # Handles GET (list) and POST (create) for schemas
    SchemaDetailView,      # Handles GET, PUT, DELETE for a specific schema
    DatasetHistoryView,    # Handles GET for the user's generation history
    DatasetDeleteView      # Handles DELETE for a specific history record
)

# Defines all API endpoints under the '/api/' root (assuming they are included 
# in the main project urls.py with 'api/')
urlpatterns = [
    # --- Data Generation Endpoint ---
    
    # POST /api/generate/
    # Main endpoint used to trigger the data generation process, performs validation and quota checks.
    path('generate/', GenerateDataView.as_view(), name='generate-data'),
    
    # --- Schema Management Endpoints ---
    
    # GET /api/schemas/ -> List all saved schemas for the user
    # POST /api/schemas/ -> Create a new schema
    path('schemas/', SchemaListCreateView.as_view(), name='schema-list'),
    
    # GET/PUT/DELETE /api/schemas/42/
    # Retrieve, update, or delete a specific schema by its primary key (pk).
    path('schemas/<int:pk>/', SchemaDetailView.as_view(), name='schema-detail'),
    
    # --- Dataset History Endpoints ---
    
    # GET /api/history/
    # Lists the historical records of all generated datasets by the user.
    path('history/', DatasetHistoryView.as_view(), name='dataset-history'),
    
    # DELETE /api/history/99/
    # Deletes a specific historical dataset record by its primary key (pk).
    path('history/<int:pk>/', DatasetDeleteView.as_view(), name='dataset-delete'),
]