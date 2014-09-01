from django.conf.urls import patterns, include, url

urlpatterns = patterns('imprest.views',
    url(r'^$', 'expense', {}, 'imprest_expense_new'),
    url(r'^view/(?P<report_id>\d+)/$', 'view_report', name="imprest.report.view"),
    url(r'^generate/(?P<report_id>\d+)/$', 'generate_report', name='imprest.report.generate'),
    url(r'^expense/(?P<expense_id>\d+)/delete/$', 'delete_expense', name='imprest.expense.delete'),
    url(r'^expense/(?P<expense_id>\d+)/edit/$', 'expense', {}, 'imprest_expense_edit'),
)
