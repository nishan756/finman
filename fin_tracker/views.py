from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.decorators import login_required
from .models import Department,Session , Member , MemberTransactionDetail , PaymentContext , SEMESTER_LIST , SHIFT_LIST , Transaction , TRAN_TYPE
from .forms import MemberForm,PaymentContextForm,MemberTransactionForm,MemberTransactionForm,TransactionForm
from django.contrib import messages
from django.utils.timezone import datetime
from session.models import CustomUser
from functools import wraps
from django.core.paginator import Paginator
# Create your views here.

# -----------------------Essential Decorators are here--------------------------------


def member_required(func):
    @wraps(func)
    def wrapper(request,id,*args,**kwargs):
        try:
            member = Member.objects.get(id = id , club = request.user)
        except Member.DoesNotExist:
            return HttpResponse("<h1>Member not found</h1>")
        return func(request,id,member,*args,**kwargs)
    return wrapper

def payment_context_required(func):
    @wraps(func)
    def wrapper(request,id,*args,**kwargs):
        try:
            context = PaymentContext.objects.get(id = id)
        except PaymentContext.DoesNotExist:
            return HttpResponse('<h1>Payment Context not found</h1>')
        return func(request,id,context,*args,**kwargs)
    return wrapper

    
def member_transaction_required(func):
    @wraps(func)
    def wrapper(request,id,*args,**kwargs):
        try:
            member_transaction = MemberTransactionDetail.objects.get(id = id)
        except MemberTransactionDetail.DoesNotExist:
            return HttpResponse('<h1>Member transaction not found</h1>')
        return func(request,id,member_transaction,*args,**kwargs)
    return wrapper

def transaction_required(func):
    @wraps(func)
    def wrapper(request,id,*args,**kwargs):
        try:
            transaction = Transaction.objects.get(id = id)
        except Transaction.DoesNotExist:
            return HttpResponse('<h1>Transaction not found</h1>')
        return func(request,id,transaction,*args,**kwargs)
    return wrapper

def club_required(func):
    @wraps(func)
    def wrapper(request,id,*args,**kwargs):
        try:
            club = CustomUser.objects.get(id = id)
        except CustomUser.DoesNotExist:
            return HttpResponse('<h1>Club not found</h1>')
        return func(request,id,club,*args,**kwargs)
    return wrapper

# -------------------- End essential decorators section----------------------------

def Home(request):
    return render(request,'index.html')

def ClubList(request):
    clubs = CustomUser.objects.all()
    name = request.GET.get('name')
    if name:
        clubs = clubs.filter(club_name__icontains = name)
    paginatore = Paginator(clubs,20)
    page = request.GET.get('page')
    clubs = paginatore.get_page(page)
    return render(request,'club-list.html',{'clubs':clubs})

@club_required
def ClubProfile(request,id,club):
    notices = PaymentContext.objects.filter(club_id = id , is_active = True)
    title = request.GET.get('title')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if title:
        notices = notices.filter(title__icontains = title)
    if from_date:
        notices = notices.filter(posted_at__gte = from_date)
    if to_date:
        notices = notices.filter(posted_at__lte = to_date)
    return render(request,'club-profile.html',{"club":club,'notices':notices})


# Member is ok
@login_required(login_url = 'login')
def member_list(request):

    # Objects
    members = Member.objects.filter(club = request.user)
    departments = Department.objects.filter(club = request.user)
    sessions = Session.objects.filter(club = request.user).order_by('session')

    # Query param value
    name = request.GET.get('name')
    roll = request.GET.get('roll')
    department = request.GET.get('department')
    semester = request.GET.get('semester')
    joined_at = request.GET.get('joined_at')
    shift = request.GET.get('shift')

    # Filtering logics 
    if name:
        members = members.filter(name__icontains = name)
    if roll:
        members = members.filter(roll = roll)
    if department:
        members = members.filter(department_id = department)
    if semester:
        members = members.filter(semester = semester)
    if joined_at:
        members = members.filter(joined_at = joined_at)
    if shift:
        members = members.filter(shift = shift)
    
    return render(request,'member-list.html',{'members':members,'departments':departments,'semesters':SEMESTER_LIST,'sessions':sessions,'shift_list':SHIFT_LIST})


# Ok
@login_required(login_url = 'login')
@member_required
def member_detail(request,id,member):
    return render(request,'member-detail.html',{'member':member})

# Ok
@login_required(login_url = 'login')
def create_member(request):
    instance = False
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            get_session = data.get('new_session')
            get_department = data.get('new_department')

            member = form.save(commit=False)
            member.club = request.user
            member.posted_at = datetime.now()

            if get_department:
                dept_obj = Department.objects.create(name=get_department)
                member.department = dept_obj

            if get_session:
                sess_obj = Session.objects.create(session=get_session)
                member.session = sess_obj

            member.save()
            messages.success(request, f'Successfully added {data["name"]}')
            return redirect('member-detail', id=member.id)
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = MemberForm()

    return render(request, 'member-form.html', {'form': form,'instance':instance})

# Ok
@login_required(login_url = 'login')
@member_required
def edit_member(request,id,member):
    instance = True
    member = member
    if member.club == request.user:
        if request.method == 'POST':
            form = MemberForm(data = request.POST , instance = member)
            if form.is_valid():
                member = form.save(commit = False)
                member.club = request.user
                member.save()
                messages.success(request,f'Successfully added {form.cleaned_data["name"]}')
                return redirect('member-detail',id = member.id)
            else:
                messages.error(request,'Please correct the error belows')
        else:
            form = MemberForm(instance = member)
    else:
        messages.warning('You can\'t edit this instance')
        return redirect('home')
    return render(request,'member-form.html',{'form':form,'instance':instance})

# Ok
@login_required(login_url = 'login')
@member_required
def delete_member(request,id,member):
    member = member
    if member.club == request.user:
        member.delete()
        messages.success(request,'Successfully deleted a member')
    else:
        messages.warning(request,'You can\'t delete this instance')
        return redirect('home')
    return redirect('member-list')



# Start payment context related functions

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


# Ok
def all_payment_context(request):

    contexts = PaymentContext.objects.filter(club_id = request.user.id)
    
    # Query param value
    title = request.GET.get('title')
    from_date = parse_date(request.GET.get('from_date'))
    to_date = parse_date(request.GET.get('to_date'))

    # Date swapping if start_date < end_date
    if from_date and to_date:
        if from_date > to_date:
            from_date,to_date = to_date,from_date

    # Filtering logics  
    if title:
        contexts = contexts.filter(title__icontains = title)
    if from_date and to_date:
        contexts = contexts.filter(posted_at__date__gte =  from_date ,posted_at__date__lte =  to_date)
    elif from_date:
        contexts = contexts.filter(posted_at__gte = from_date)
    elif to_date:
        contexts = contexts.filter(posted_at__lte = to_date)

    return render(request,'payment-contexts.html',{'contexts':contexts})

# Ok
@payment_context_required
def payment_context_detail(request,id,context):
    return render(request,'payment-context-detail.html',{'context':context})

# Ok
@login_required(login_url = 'login')
def create_payment_context(request):
    if request.method == 'POST':
        form = PaymentContextForm(data = request.POST)
        if form.is_valid():
            context = form.save(commit = False)
            context.club = request.user
            context.save()
            messages.success(request,f'Successfully created {form.cleaned_data["title"]}')
            return redirect('payment-context-detail',id = context.id)
        else:
            messages.error(request,'Please correct the error below')
    else:
        form = PaymentContextForm()
    return render(request,'payment-context-form.html',{'form':form})

# Ok
@login_required(login_url = 'login')
@payment_context_required
def edit_payment_context(request,id,context):
    if context.club == request.user:
        if request.method == 'POST':
            form = PaymentContextForm(data = request.POST , instance = context)
            if form.is_valid():
                context = form.save(commit = False)
                context.club = request.user
                context.save()
                messages.success(request,f'Successfully updated {form.cleaned_data["title"]}')
                return redirect('payment-context-detail',id = id)
            else:
                messages.error(request,'Please correct the error belows')
        else:
            instance = True
            form = PaymentContextForm(instance = context)
    else:
        messages.warning('You can\'t edit this instance')
        return redirect('home')
    return render(request,'payment-context-form.html',{'form':form,'instance':instance})


@login_required(login_url = 'login')
@payment_context_required
def delete_payment_context(request,id,context):
    if context.club == request.user:
        messages.success(request,f'Successfully deleted {context.title}')
        context.delete()
    else:
        messages.warning('You can\'t delete this instance')
        return redirect('home')
    return redirect('payment-context-list')


# Start member transaction related functions
@login_required(login_url = 'login')
def create_member_transaction(request):
    instance = False
    if request.method == 'POST':
        form = MemberTransactionForm(data = request.POST)
        if form.is_valid():
            new_tran = form.save(commit = False)
            new_tran.amount = new_tran.context.amount
            new_tran.club = request.user
            new_tran.save()
            transaction = Transaction(amount = new_tran.amount,member_transaction = new_tran,title = new_tran.context.title,transaction_type = 'Income')
            transaction.save()
            messages.success(request,'Succesfully created new transaction')
            return redirect('member-transaction-detail',new_tran.id)
        else:
            messages.error(request,'Please correct the errors below')
    else:
        form = MemberTransactionForm()
    return render(request,'member-transaction-form.html',{"form":form,'instance':instance})

@login_required(login_url = 'login')
@member_transaction_required
def edit_member_transaction(request,id,member_transaction):
    if member_transaction.club == request.user:
        if request.method == 'POST':
            form = MemberTransactionForm(data = request.POST,instance = member_transaction)
            if form.is_valid():
                editted_tran = form.save(commit = False)
                editted_tran.club = request.user
                editted_tran.save()
                return redirect('member-transaction-detail',member_transaction.id)
            else:
                messages.error(request,'Please correct the errors below')
        else:
            form = MemberTransactionForm(instance = member_transaction)
    else:
        messages.warning('You can\'t edit this instance')
        return redirect('home')
    return render(request,'member-transaction-form.html',{"form":form})


@login_required(login_url = 'login')
@member_transaction_required
def delete_member_transaction(request,id,member_transaction):
    if member_transaction.club == request.user:
        messages.success(request,f'Successfully deleted [{member_transaction.member} transaction]')
        member_transaction.delete()
    else:
        messages.warning('You can\'t delete this instance')
        return redirect('home')
    return redirect('member-transaction-list')

    

def all_member_transaction(request):
    transactions = MemberTransactionDetail.objects.filter(club = request.user)
    departments = Department.objects.filter(club = request.user)
    sessions = Session.objects.filter(club = request.user).order_by('session')
    contexts = PaymentContext.objects.filter(club = request.user)

    # Query logics
    member = request.GET.get('member')
    context = request.GET.get('context')
    semester = request.GET.get('semester')
    session = request.GET.get('session')
    department = request.GET.get('department')
    transaction_id = request.GET.get('transaction_id')

    if transaction_id:
        try:
            transaction = transactions.get(transaction_id = transaction_id)
        except MemberTransactionDetail.DoesNotExist:
            transaction = None
    else:
        transaction = None
    if member:
        transactions = transactions.filter(member__name__icontains = member)
    if context:
        transactions = transactions.filter(context__id = context)
    if session:
        transactions = transactions.filter(member__session__id = session)
    if semester:
        transactions = transactions.filter(member__semester = semester)
    if department:
        transactions = transactions.filter(member__department__id = department)
    if transaction_id is not None:
        transactions = transactions.exclude(transaction_id = transaction_id)

    return render(request,'member-transactions.html',{'transactions':transactions,'departments':departments,'sessions':sessions,'SHIFT_LIST':SHIFT_LIST,'contexts':contexts,'semesters':SEMESTER_LIST,'transaction':transaction})

@member_transaction_required
def member_transaction_detail(request,id,member_transaction):
    return render(request,'member-transaction-detail.html',{'transaction':member_transaction})


# Start transaction related logics

@login_required(login_url = 'login')
def create_transaction(request):
    instance = False
    if request.method == 'POST':
        form = TransactionForm(data = request.POST)
        if form.is_valid():
            new_transaction = form.save()
            new_transaction.club = request.user
            new_transaction.save()
            messages.success(request,'Transaction Successfull')
            return redirect('transaction-detail',new_transaction.id)
        else:
            messages.error(request,'Please correct the error belows')
            print(form.errors)
    form = TransactionForm()
    return render(request,'transaction-form.html',{'form':form,'instance':instance})


@login_required(login_url = 'login')
@transaction_required
def edit_transaction(request,id,transaction):
    if transaction.club == request.user:
        instance = False
        if request.method == 'POST':
            form = TransactionForm(data = request.POST,instance = transaction)
            if form.is_valid():
                new_transaction = form.save()
                new_transaction.save()
                messages.success(request,'Successfully updated this trasaction')
                return redirect('transaction-detail',new_transaction.id)
            else:
                messages.error(request,'Please correct the error belows')
        form = TransactionForm(instance = transaction)
    else:
        messages.warning('You can\'t edit this instance')
        return redirect('home')
    return render(request,'transaction-form.html',{'form':form,'instance':instance})


@login_required(login_url = 'login')
@transaction_required
def delete_transaction(request,id,transaction):
    if transaction.club == request.user:
        transaction.delete()
        messages.success(request,'Successfully deleted a transacrtion')
    else:
        messages.warning('You can\'t delete this instance')
        return redirect('home')
    return redirect('transaction-list')

@login_required(login_url = 'login')
def transaction_list(request):
    transactions = Transaction.objects.filter(club = request.user)
    # Query logic
    title = request.GET.get('title')
    from_date = request.GET.get('from')
    to_date = request.GET.get('to_date')
    tran_type = request.GET.get('tran_type')
    if title:
        transactions = transactions.filter(title__icontains = title)
    if from_date and to_date:
        transactions = transactions.filter(date__gte = from_date,date__lte = to_date)
    elif from_date:
        transactions = transactions.filter(date__gte = from_date)
    elif to_date:
        transactions = transactions.filter(date__lte = to_date)
    if tran_type:
        transactions = transactions.filter(transaction_type = tran_type)

    return render(request,'transaction-list.html',{'transactions':transactions})

@login_required(login_url = 'login')
@transaction_required
def transaction_detail(request,id,transaction):
    return render(request,'transaction-detail.html',{'transaction':transaction})

