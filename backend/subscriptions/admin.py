from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les Abonnements"""
    
    # Colonnes affichées
    list_display = ['id', 'user', 'status', 'start_date', 'end_date']
    
    # Filtres
    list_filter = ['status', 'start_date', 'end_date']
    
    # Recherche
    search_fields = ['user__email', 'user__username', 'stripe_customer_id', 'stripe_subscription_id']
    
    # Organisation du formulaire
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Stripe', {
            'fields': ('stripe_customer_id', 'stripe_subscription_id')
        }),
        ('Statut et Dates', {
            'fields': ('status', 'start_date', 'end_date')
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ['start_date']
    
    # Ordre par défaut
    ordering = ['-start_date']