from django.shortcuts import render

# Create your views here.
def ticket_list(request):
    return render(request, 'issue_tracker_app/ticket_list.html', {})