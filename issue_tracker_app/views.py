from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Ticket, Comment, Vote
from .forms import TicketForm, UserLoginForm, UserRegistrationForm, CommentForm
from django.db import IntegrityError
from crispy_forms.helper import FormHelper
import stripe
from .payment import create

# Create your views here.
def ticket_list(request):
    """
    Create a view that will return a list of Tickets
    """
    tickets = Ticket.objects.filter(published_date__lte=timezone.now())
    bugs = []
    features = []
    for ticket in tickets:
        if ticket.ticket_type == 'B':
            bugs.append(ticket)
        else:
            features.append(ticket)

    def bugs_srt(bug):
        return bug.upvotes.count()
    bugs.sort(reverse=True, key=bugs_srt)
    return render(request, 'issue_tracker_app/ticket_list.html', {'bugs': bugs, 'features': features})


def ticket_detail(request, pk):
    print(request.user.is_authenticated)
    user = None
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'issue_tracker_app/ticket_detail.html', {'ticket': ticket, 'user': user})


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
    return render(request, 'issue_tracker_app/ticket_new.html', {'form': form})


@login_required(login_url='/accounts/login')
def ticket_edit(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    user = request.user
    form = TicketForm(request.POST or None, instance = ticket)
    if ticket.author == user:
        if form.is_valid():
            ticket.save()
            return redirect(reverse('ticket_list'))
        else:
            return render(request, 'issue_tracker_app/ticket_edit.html', {'ticket': ticket, 'form': form})
    else:
        messages.error(request, 'You are not authorized to edit this post')
    return redirect(ticket_detail, pk=ticket_id)

@login_required(login_url='/accounts/login')
def checkout(request):
    session_id = create()
    print(session_id)
    return render(request, 'issue_tracker_app/checkout.html', {'session_id': session_id})

@login_required(login_url='/accounts/login')
def success(request):
    session_id = request.GET.get('session_id')
    line_items = stripe.checkout.Session.list_line_items(session_id, limit=5)
    print(line_items.data)
    return render(request, 'issue_tracker_app/success.html', {'session_id': session_id, 'line_items': line_items})


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

@login_required(login_url='/accounts/login')
def ticket_vote(request, ticket_id, user_id):
    user = User.objects.get(id=user_id)
    ticket = Ticket.objects.get(id=ticket_id)
    try:
        vote = Vote(user=user, ticket=ticket, date=timezone.now())
        vote.save()
        messages.success(request, 'Your vote has been added.')
    except IntegrityError as e:
        messages.error(request, 'You can\'t vote twice')
    except:
        messages.error(request, 'Something went wrong')
    return redirect('ticket_detail', pk=ticket.pk)
    
