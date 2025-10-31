from django.db import models
# Assuming 'users' app is where the custom User model is defined
from users.models import User

## Schema Model
class Schema(models.Model):
    """
    Represents a user-defined blueprint (schema) for synthetic data generation.
    This model stores the structure and the Faker types requested by the user.
    """
    # Links the schema to a specific authenticated user.
    # If the user is deleted, all their schemas are deleted (CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schemas')

    # Human-readable name given to the schema by the user (e.g., "Customer Data").
    name = models.CharField(max_length=255)

    # Stores the structure of the data: {field_name: faker_type}.
    # Example: {"first_name": "name", "customer_email": "email"}
    schema_json = models.JSONField()

    # Automatically records the date and time when the schema was first created.
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Orders query results by the most recently created schemas first.
        ordering = ['-date_created']
    
    def __str__(self):
        """String representation used in the Django admin site."""
        return f"{self.user.email} - {self.name}"


## GeneratedDataset Model
class GeneratedDataset(models.Model):
    """
    Represents a historical record of a generated dataset, primarily for download 
    history and tracking usage.
    """
    # Defines the possible output formats for the generated data file.
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('sql', 'SQL'),
        ('xml', 'XML'),
    ]
    
    # Links the dataset record to the user who generated it.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')

    # Optional link to the Schema model used. If the schema is deleted, 
    # the dataset record remains, but the foreign key is set to NULL.
    schema = models.ForeignKey(Schema, on_delete=models.SET_NULL, null=True, blank=True)

    # Stores a copy of the schema JSON at the time of generation for historical integrity.
    schema_json = models.JSONField()
    nb_rows = models.IntegerField() # The number of data rows generated in this dataset.

    # The format in which the file was saved (e.g., 'csv', 'json').
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='json')

    # Path or URL where the generated file is stored (e.g., S3 or local path).
    file_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.nb_rows} rows - {self.file_format}"