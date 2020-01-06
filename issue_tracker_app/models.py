from django.db import models
from django.utils import timezone

# Create your models here.

class Ticket(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    TICKET_TYPES = [
        ('B', 'bug'),
        ('F', 'feature')
    ]
    TICKET_STATUSES = [
        ('T', 'to do'),
        ('D', 'doing'),
        ('C', 'done')
    ]

    ticket_type = models.CharField(max_length=1, choices=TICKET_TYPES)
    ticket_status = models.CharField(max_length=1, choices=TICKET_STATUSES, default='T')
    upvotes = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    
    def __str__(self):
        return self.title
