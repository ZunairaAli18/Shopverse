from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display  = ('name', 'vendor', 'is_approved', 'created_at')
    list_filter   = ('is_approved',)
    list_editable = ('is_approved',)     # ← approve stores directly from list view
    search_fields = ('name', 'vendor__username')

    actions = ['approve_stores', 'reject_stores']

    def approve_stores(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} store(s) approved.')
    approve_stores.short_description = 'Approve selected stores'

    def reject_stores(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} store(s) rejected.')
    reject_stores.short_description = 'Reject selected stores'