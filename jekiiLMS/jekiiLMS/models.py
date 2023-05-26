from django.db import models

class RecentActivity(models.Model):
    EVENT_CHOICES = (
        ('loan_approval', 'Loan Approval'),
        ('loan_rejection', 'Loan Rejection'),
        ('loan_clearance', 'Loan Clearance'),
        ('loan_write_off', 'Loan Write-off'),
        ('loan_roll_over', 'Loan Roll-over'),
        ('loan_product_addition', 'Loan Product Addition'),
        ('branch_opened', 'Branch Opened'),
    )

    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=200)


    def __str__(self):
        return self.event_type
