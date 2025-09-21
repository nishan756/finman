from .models import Member,PaymentContext,MemberTransactionDetail,Session,Department,MemberTransactionDetail,Transaction
from django import forms 




class MemberForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['shift'].required = True

    new_department = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(
            attrs = {
                'type':'text',
                'class':'form-control',
                'placeholder':'Department',
            }
        )
    )

    new_session = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(
            attrs = {
                'type':'text',
                'class':'form-control',
                'placeholder':'Session (Ex: 23 - 24)',
            }
        )
    )

    class Meta:
        model = Member
        fields = "__all__"
        widgets = {
            'name':forms.TextInput(attrs = {'type':'text','class':'form-control','placeholder':'Name'}),
            'roll':forms.NumberInput(attrs = {'type':'number','class':'form-control','placeholder':'Roll'}),
            'department':forms.Select(attrs = {'type':'select','class':'form-control'}),
            'semester':forms.Select(attrs = {'type':'select','class':'form-control'}),
            'contact':forms.TextInput(attrs = {'type':'text','class':'form-control','placeholder':'Contact'}),
            'email':forms.EmailInput(attrs = {'type':'email','class':'form-control'}),
            'joined_at':forms.DateInput(attrs = {'type':'date','class':'form-control'}),
            'session':forms.Select(attrs = {'type':'select','class':'form-control'}),
            'shift':forms.Select(attrs = {'type':'select','class':'form-control'}),
        }
        help_texts = {
            'contact':'*Provide an unique contact number',
            'joined_at':'*The date when the member join in the club',
            'roll':'*Board roll of the member',
            'email':'*Provide an unique email',
            'name':'*Full name of the member',
        }

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department',None)
        new_department = cleaned_data.get('new_department',None)
        session = cleaned_data.get('session',None)
        new_session = cleaned_data.get('new_session',None)
        check_session = Session.objects.filter(session = session).exists()
        check_department = Department.objects.filter(name = new_department).exists()

        if department is None and new_department is None:
            self.add_error('department','You must provide a department.')

        if department and new_department:
            self.add_error('department', 'Fill only one: existing or new department.')
            self.add_error('new_department', 'Fill only one: existing or new department.')

        if session is None and new_session is None:
            self.add_error('session','You must provide a session.')

        if session and new_session:
            self.add_error('session', 'Fill only one: existing or new session.')
            self.add_error('new_session', 'Fill only one: existing or new session.')

        if new_session:
            if new_session == check_session:
                self.add_error('new_session','This session already exists ')

        if new_department:
            if new_department == check_department:
                self.add_error('new_department','This department already exists')
        
        return cleaned_data
        


class PaymentContextForm(forms.ModelForm):

    class Meta:
        model = PaymentContext
        fields = "__all__"
        widgets = {
            'title':forms.TextInput(attrs = {'type':'text','class':'form-control'}),
            'start_date':forms.DateInput(attrs = {'type':'datetime-local','class':'form-control'}),
            'end_date':forms.DateTimeInput(attrs = {'type':'datetime-local','class':'form-control'}),
            'posted_at':forms.DateTimeInput(attrs = {'type':'datetime-local','class':'form-control'}),
            'amount':forms.NumberInput(attrs = {'type':'number','class':'form-control'}),
            'is_active':forms.CheckboxInput(attrs = {'type':'checkbox','class':'form-check-control'}),
            
        }



class MemberTransactionForm(forms.ModelForm):

    class Meta:
        model = MemberTransactionDetail
        exclude = ['amount',]
        widgets = {
            'context':forms.Select(attrs = {'type':'select','class':'form-control'}),

            'member':forms.Select(attrs = {'type':'text','class':'form-control'}),

            'account_no':forms.TextInput(attrs = {'type':'text','class':'form-control'}),

            'transaction_id':forms.TextInput(attrs = {'type':'text',
            'class':'form-control'}),

            'is_paid':forms.CheckboxInput(attrs = {'type':'checkbox','class':'form-check-input'}),

            'took_loan':forms.CheckboxInput(attrs = {'type':'checkbox','class':'form-check-input'}),

            'due':forms.NumberInput(attrs = {'type':'number','class':'form-control'}),

            'date':forms.DateTimeInput(attrs = {'type':'datetime-local','class':'form-control'}),

        }
        help_texts = {
            'account_no':'The account from which the money was sent',
        }

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data.get('transaction_id')
        if MemberTransactionDetail.objects.filter(transaction_id = transaction_id).exists():
            self.add_error('transaction_id','This id already exists')
        return transaction_id
    


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id','member_transaction']
        widgets = {
            
            'transaction_type':forms.Select(attrs = {'type':'select','class':'form-control'}),

            'title':forms.TextInput(attrs = {'type':'text','class':'form-control','placeholder':'Enter Transaction Title'}),

            'amount':forms.NumberInput(attrs = {'type':'number','class':'form-control','placeholder':'Enter Amount'}),

            'date':forms.DateInput(attrs = {'type':'date','class':'form-control'}),

        }

