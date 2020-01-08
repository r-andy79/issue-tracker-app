from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm, UserLoginForm, UserRegistrationForm

# Create your views here.
def ticket_list(request):
    tickets = Ticket.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'issue_tracker_app/ticket_list.html', {'tickets': tickets})


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'issue_tracker_app/ticket_detail.html', {'ticket': ticket})

@login_required(login_url='/accounts/login')
def ticket_new(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.published_date = timezone.now()
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'issue_tracker_app/ticket_edit.html', {'form': form})


@login_required(login_url='/accounts/login')
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out')
    return redirect(reverse('ticket_list'))


def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('ticket_list'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, 'You have successfully logged in')
                return redirect(reverse('ticket_list'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'issue_tracker_app/login.html', {'login_form': login_form})


def registration(request):
    registration_form = UserRegistrationForm()
    return render(request, 'issue_tracker_app/registration.html', {'registration_form': registration_form})
