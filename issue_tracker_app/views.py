from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Ticket

# Create your views here.
def ticket_list(request):
    tickets = Ticket.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'issue_tracker_app/ticket_list.html', {'tickets': tickets})


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'issue_tracker_app/ticket_detail.html', {'ticket': ticket})