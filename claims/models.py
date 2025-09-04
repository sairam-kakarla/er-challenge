from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse

class Claim(models.Model):
    class Status(models.TextChoices):
        PAID = 'Paid', 'Paid'
        DENIED = 'Denied', 'Denied'
        UNDER_REVIEW = 'Under Review', 'Under Review'
    # Core Fields from CSV/JSON
    id = models.IntegerField(primary_key=True)
    patient_name = models.CharField(max_length=255)
    billed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNDER_REVIEW)
    insurer_name = models.CharField(max_length=255)
    discharge_date = models.DateField()

    # User-Generated Fields
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Claim #{self.id} - {self.patient_name}"


class ClaimDetail(models.Model):
    # Core fields from detail.csv
    id = models.IntegerField(primary_key=True)
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE,related_name='details')
    cpt_codes = models.CharField(max_length=255, help_text="Comma-separated CPT codes")
    denial_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for Claim #{self.claim.id}"
    
class Note(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='notes')
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    text= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author_name = self.author.username if self.author else "Anonymous"
        return f"Note by {author_name} for Claim #{self.claim.id}"