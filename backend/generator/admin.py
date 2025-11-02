from django.contrib import admin
from .models import Schema, GeneratedDataset

@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les Schémas"""
    
    # Colonnes affichées dans la liste
    list_display = ['id', 'name', 'user', 'date_created']
    
    # Filtres
    list_filter = ['date_created', 'user']
    
    # Recherche
    search_fields = ['name', 'user__email', 'user__username']
    
    # Organisation du formulaire
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'name')
        }),
        ('Schéma JSON', {
            'fields': ('schema_json',),
            'description': 'Définition du schéma au format JSON'
        }),
        ('Métadonnées', {
            'fields': ('date_created',)
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ['date_created']
    
    # Ordre par défaut
    ordering = ['-date_created']


@admin.register(GeneratedDataset)
class GeneratedDatasetAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les Datasets générés"""
    
    # Colonnes affichées
    list_display = ['id', 'user', 'nb_rows', 'file_format', 'created_at']
    
    # Filtres
    list_filter = ['file_format', 'created_at', 'user']
    
    # Recherche
    search_fields = ['user__email', 'user__username']
    
    # Organisation du formulaire
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Configuration', {
            'fields': ('schema', 'schema_json', 'nb_rows', 'file_format')
        }),
        ('Fichier', {
            'fields': ('file_path',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',)
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ['created_at']
    
    # Ordre par défaut
    ordering = ['-created_at']