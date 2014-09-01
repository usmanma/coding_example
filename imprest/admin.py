from django.contrib import admin

from .models import Category, Expense, Report

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['item', 'id', 'category', 'expense_date', 'amount']
    fields = (('item', 'amount'), ('expense_date', 'category', 'employee'), 'notes')
    ordering = ['-expense_date']
    list_filter = ['expense_date', 'category', 'employee']
    date_hierarchy = 'expense_date'
    search_fields = ['item']
    
class ReportAdmin(admin.ModelAdmin):
    list_display = ('edit_report', 'start', 'end', 'draft', 'include_summary')
    fields = (('start', 'end'), 'include_summary', 'draft')
    date_hierarchy = 'start'

    def edit_report(self, obj):
        return 'IR-%s (%s)' % (obj.id, obj)


    edit_report.allow_tags = True

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'published')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Report, ReportAdmin)
