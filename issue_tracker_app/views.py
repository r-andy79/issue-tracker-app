from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import auth, messages
from .models import Ticket
from .forms import TicketForm

# Create your views here.
def ticket_list(request):
    tickets = Ticket.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'issue_tracker_app/ticket_list.html', {'tickets': tickets})


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'issue_tracker_app/ticket_detail.html', {'ticket': ticket})


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


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out')
    return redirect(reverse('ticket_list'))
