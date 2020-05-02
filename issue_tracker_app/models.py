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
    upvotes = models.ManyToManyField('auth.User', through='Vote', related_name='upvotes')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    
    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=140)


    def __str__(self):
        return self.comment_text


    def get_absolute_url(self):
        return reverse('ticket_list')


class Vote(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.user) + ":" + str(self.ticket) + str(self.date)


    class Meta:
        unique_together = ("user", "ticket")