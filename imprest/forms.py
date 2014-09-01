from django.core.urlresolvers import reverse
from django.forms import ModelForm

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit

from .models import Expense

class ExpenseForm(ModelForm):
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_action = ''
        # Changes submit button text and styling based on state.
        SUBMIT_PRE = 'Edit' if self.instance.id else 'Add'
        SUBMIT_CSS_EXTRAS = ' btn-warning' if self.instance.id else ''
        
        helper.layout = Layout(
            Field(
                'item',
                placeholder='Item',
                css_class='span12',
            ),
            Field(
                'category',
                css_class='span12',
            ),
            PrependedText(
                'amount',
                '&pound;',
                placeholder='Amount',
                css_class='span11',
            ),
            Field(
                'expense_date',
                placeholder='Expense Date',
                data_date_format='dd/mm/yyyy',
                css_class='span12 dateinput',
            ),
            Field(
                'employee',
                css_class='span12',
            ),
            Field(
                'notes',
                placeholder='Optional Notes',
                css_class='span12',
            ),
            ButtonHolder(
                Submit('submit', '%s Expense' % SUBMIT_PRE, css_class='btn-primary pull-right%s' % SUBMIT_CSS_EXTRAS)
            ),
        )
        return helper
    
    class Meta:
        model = Expense
