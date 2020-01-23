from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Ticket, Comment
from .forms import TicketForm, UserLoginForm, UserRegistrationForm, CommentForm

# Create your views here.
def ticket_list(request):
    """
    Create a view that will return a list of Tickets
    """
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
    if request.user.is_authenticated:
        return redirect(reverse('ticket_list'))
    
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('ticket_list'))
            else:
                messages.error(request, 'Unable to register your account at this time')

    else:
        registration_form = UserRegistrationForm()
    return render(request, 'issue_tracker_app/registration.html', {'registration_form': registration_form})


def user_profile(request):
    """The user's profile"""
    user = User.objects.get(email=request.user.email)
    username = User.objects.get(username=request.user.username)
    tickets = Ticket.objects.filter(author=username)
    tickets_count = Ticket.objects.filter(author=username).count()
    bugs_count = Ticket.objects.filter(author=username, ticket_type='B').count()
    features_count = Ticket.objects.filter(author=username, ticket_type='F').count()
    to_do_count = Ticket.objects.filter(author=username, ticket_status ='T').count()
    doing_count = Ticket.objects.filter(author=username, ticket_status ='D').count()
    done_count = Ticket.objects.filter(author=username, ticket_status ='C').count()
    return render(request, 'issue_tracker_app/profile.html', {'profile': user, 
                                                              'tickets': tickets,
                                                              'tickets_count': tickets_count, 
                                                              'bugs_count': bugs_count, 
                                                              'features_count': features_count,
                                                              'to_do_count': to_do_count,
                                                              'doing_count': doing_count,
                                                              'done_count': done_count
                                                              })


@login_required(login_url='/accounts/login')
def add_comment_to_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.ticket = ticket
            comment.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()
    return render(request, 'issue_tracker_app/add_comment_to_ticket.html', {'form': form})
