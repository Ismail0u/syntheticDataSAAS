from rest_framework import serializers
from .models import Schema, GeneratedDataset

class SchemaSerializer(serializers.ModelSerializer):
    """
    Serializer for the saved JSON Schemas (blueprints) defined by the user.
    Handles serialization/deserialization of the Schema model data.
    """
    class Meta:
        model = Schema
        # Fields exposed via the API. Note: 'user' is often handled automatically 
        # or set by the view to the current request user.
        fields = ['id', 'name', 'schema_json', 'date_created']
        # Fields that are automatically set by the database/backend and cannot be 
        # modified by the client during creation or update.
        read_only_fields = ['id', 'date_created']


class GenerateDataSerializer(serializers.Serializer):
    """
    Custom serializer used to validate incoming POST request data for the 
    /api/generate/ endpoint. It does not map directly to a model.
    """
    # The required JSON structure defining the fields and Faker types.
    schema = serializers.JSONField(help_text="JSON schema defining the fields to generate (e.g., {'name': 'name'}).")
    
    rows = serializers.IntegerField(min_value=1, max_value=50000, help_text="The number of data rows to generate")
    # The requested export format for the generated dataset file.
    format = serializers.ChoiceField(
        choices=['json', 'csv', 'xlsx', 'sql', 'xml'],
        default='json',
        help_text="The desired output format for the dataset."
    )
    save_schema = serializers.BooleanField(default=False, help_text="Set to true to save the schema blueprint to the user's account.")
    schema_name = serializers.CharField(required=False, allow_blank=True, help_text="Name for the schema (required if save_schema is True).")


class GeneratedDatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for the GeneratedDataset model, used to display the history 
    of generated files to the user.
    """
    # Custom read-only field to display the email of the generating user, 
    # fetched via the foreign key relationship.
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = GeneratedDataset
        # Fields exposed to the user in the history view.
        fields = ['id', 'user_email', 'schema_json', 'nb_rows', 'file_format', 'file_path', 'created_at']
        read_only_fields = ['id', 'user_email', 'created_at']