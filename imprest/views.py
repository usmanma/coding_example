from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.http import base36_to_int, int_to_base36

from .forms import ExpenseForm
from .models import Expense, Report

def _get_drafts():
    try:
        draft_report = Report.objects.get(draft=True)
        new_expenses = draft_report.get_expenses()
    except Report.DoesNotExist:
        draft_report = None
        new_expenses = None
    reports = Report.objects.filter(draft=False)
    if reports:
        for r in reports:
            r.__setattr__('rid', int_to_base36(r.id))
    
    return (draft_report, new_expenses, reports)

@login_required
def expense(request, expense_id=None):
    if expense_id:
        expense = get_object_or_404(Expense, pk=expense_id)
    else:
        expense = Expense()
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('imprest.views.expense'))
    else:
        form = ExpenseForm(instance=expense)
    
    
    draft_report, new_expenses, reports = _get_drafts()
    
    c = {
        'expense_form': form,
        'new_expenses': new_expenses,
        'draft_report': draft_report,
        'reports': reports,
    }
    
    return render_to_response(
        'imprest/index.html',
        c,
        context_instance=RequestContext(request)
    )

@login_required
def view_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    report_id = int_to_base36(report.id)
    expenses = report.expenses.all()
    internal_expenses = expenses.order_by('expense_date')
    expenses_total = expenses.aggregate(Sum('amount'))
    employee_total = {}
    cat_total = {}
    
    for expense in expenses:
        try:
            employee_total[expense.employee] += expense.amount
        except:
            employee_total[expense.employee] = expense.amount
        try:
            cat_total[expense.category] += expense.amount
        except:
            cat_total[expense.category] = expense.amount

    ctx = {
        'report': report,
        'report_id': report_id,
        'expenses': expenses,
        'internal_expenses': internal_expenses,
        'employee_totals': employee_total,
        'total': expenses_total,
        'category_totals': cat_total,
    }
    return render_to_response('imprest/view_report.html', ctx)

@login_required
def generate_report(request, report_id):
    try:
        Report.objects.get(pk=report_id).generate_report()
    except Report.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('imprest.views.view_report', args=(report_id,)))

@login_required
def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(pk=expense_id)
        expense.delete()
    except:
        pass
    return HttpResponseRedirect(reverse('imprest.views.expense'))
