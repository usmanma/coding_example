from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from model_utils.models import TimeStampedModel

class Category(TimeStampedModel):
    category = models.CharField(max_length=50)
    published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.category


class Expense(TimeStampedModel):
    item = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        limit_choices_to={'published': True}
    )
    expense_date = models.DateField(verbose_name="date")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    employee = models.ForeignKey(
        User,
        default=User,
        limit_choices_to={'is_active': True}
    )
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        return "%s (%s)" % (self.item, self.expense_date)
    
    class Meta:
        ordering = ['category', 'expense_date']


class Report(TimeStampedModel):
    start = models.DateField()
    end = models.DateField()
    include_summary = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    expenses = models.ManyToManyField(Expense)
    
    def generate_report(self):
        self.draft = False
        self.save()
    
    def get_expenses(self):
        return self.expenses.all()
    
    def _category_total(self):
        return self.objects.extra(
            select={"cat_total": "category"}
        ).aggregate(cat_total=Sum("amount"))["cat_total"]
    
    def __unicode__(self):
        return "%s - %s" % (
            self.start.strftime("%d %b %Y"),
            self.end.strftime("%d %b %Y")
        )
    
    class Meta:
        ordering = ['-created']

def add_entry_to_report(sender, **kwargs):
    expense = kwargs['instance']
    
    # Only go on if the expense was saved successfully
    if kwargs['created']:
        # Try to find a report in db that is in draft mode
        try:
            report = Report.objects.get(draft=True)
        except Report.DoesNotExist:
            report = Report()
            report.draft = True
            report.start = expense.expense_date
            report.end = expense.expense_date
        
        # Set report dates to include the expense
        if expense.expense_date < report.start:
            report.start = expense.expense_date
        
        if expense.expense_date > report.end:
            report.end = expense.expense_date
        
        report.save()
        report.expenses.add(expense)
        report.save()

# Signals
post_save.connect(add_entry_to_report, sender=Expense)
