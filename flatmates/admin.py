from django.contrib import admin

from .models import userProfile, Expenses

@admin.register(userProfile)
class userProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name","email","joining_date","company")

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ("full_name","expense","spent_amount","spent_date","description")



