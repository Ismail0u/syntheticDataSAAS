from django.db import models
from users.models import User

class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schemas')
    name = models.CharField(max_length=255)
    schema_json = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"


class GeneratedDataset(models.Model):
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('sql', 'SQL'),
        ('xml', 'XML'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    schema = models.ForeignKey(Schema, on_delete=models.SET_NULL, null=True, blank=True)
    schema_json = models.JSONField()
    nb_rows = models.IntegerField()
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='json')
    file_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.nb_rows} rows - {self.file_format}"