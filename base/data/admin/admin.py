from django.contrib import admin

# Register your models here.
from data.models.models import CustomerProfile, OwnerProfile, RefererProfile, CustomerLedger,BalanceChange

class OwnerInline(admin.TabularInline):
    model = OwnerProfile
    fields = ('owner_english_name','owner_chinese_name','phone','shares')

class OwnerAdmin(admin.ModelAdmin):
    inlines = [OwnerInline, ]
    search_fields = ['ref_no','chinese_name','english_name']


admin.site.register(CustomerProfile,OwnerAdmin)        
admin.site.register(RefererProfile) 
admin.site.register(CustomerLedger)
admin.site.register(BalanceChange)