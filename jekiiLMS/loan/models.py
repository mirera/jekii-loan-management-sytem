from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.db.models import Sum
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db import transaction
from member.models import Member
from company.models import Organization
from user.models import CompanyStaff
from jekiiLMS.mpesa_statement import amount_based_cs, final_recommended_amount
from jekiiLMS.loan_math import total_payable_amount, installments, total_penalty

   

#Loan Prouct model starts here

REPAYMENT_FREQUENCY_CHOICES = (
    ('onetime','ONETIME'),
    ('daily', 'DAILY'),
    ('weekly','WEEKLY'),
    ('monthly','MONTHLY'),
)

INTEREST_TYPE_CHOICES = (
    ('flat rate','FLAT RATE'),
    ('reducing balance', 'REDUCING BALANCE'),
)

SERVICE_FEE_TYPE_CHOICES = (
    ('fixed value','FIXED VALUE'),
    ('percentage', 'PERCENTAGE'),
)

PENALTY_FEE_TYPE_CHOICES = (
    ('fixed_value','FIXED VALUE'),
    ('percentage of principal', 'p.c of Due Principal'),
    ('percentage of principal interest', 'p.c of Due P + I'),
)

PENALTY_FREQUENCY_TYPE_CHOICES = (
    ('onetime','ONETIME'),
    ('daily', 'DAILY'),
    ('weekly', 'WEEKLY'),
    ('monthly', 'MONTHLY'),
)



ACTIVE_CHOICES = (
    ('active','ACTIVE'),
    ('inactive','INACTIVE'),
)

TERM_PERIOD = (
    ('day','DAY'),
    ('week','WEEK'),
    ('month','MONTH'),
    ('year','YEAR'),
)

class LoanProduct(models.Model): 
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    loan_product_name = models.CharField(max_length=300)
    minimum_amount = models.IntegerField()
    maximum_amount = models.IntegerField()
    loan_product_term = models.IntegerField()
    loan_term_period= models.CharField(max_length=20, choices=TERM_PERIOD, default='month')
    repayment_frequency = models.CharField(max_length=8, choices=REPAYMENT_FREQUENCY_CHOICES, default='onetime')
    interest_type = models.CharField(max_length=30, choices=INTEREST_TYPE_CHOICES, default='flat_rate')
    interest_rate = models.FloatField()
    service_fee_type = models.CharField(max_length=300, choices=SERVICE_FEE_TYPE_CHOICES, default='fixed_value')
    service_fee_value = models.FloatField()
    penalty_type = models.CharField(max_length=300, choices=PENALTY_FEE_TYPE_CHOICES, default='fixed_value')
    penalty_value = models.FloatField()
    penalty_frequency = models.CharField(max_length=300, choices=PENALTY_FREQUENCY_TYPE_CHOICES, default='onetime')
    status = models.CharField(max_length=10, choices=ACTIVE_CHOICES, default='active')
    loan_product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.loan_product_name
#-- ends



#Loan  model starts here

LOAN_STATUS = (
    ('pending','PENDING'),
    ('approved','APPROVED'),
    ('rejected','REJECTED'),
    ('overdue','OVERDUE'),
    ('cleared','CLEARED'),
    ('written off','WRITTEN OFF'),
    ('rolled over', 'ROLLED OVER')
)
class Loan(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    loan_id =models.CharField(max_length=50, null=True, unique=True, blank=True)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_member')
    applied_amount = models.IntegerField()
    approved_amount = models.IntegerField(blank=True, null=True)
    disbursed_amount = models.IntegerField(blank=True, null=True)
    num_installments = models.IntegerField(blank=True, null=True)
    guarantor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_guarantor', blank=True)
    application_date = models.DateTimeField()
    approved_date = models.DateTimeField(blank=True, null=True)
    disbursed_date = models.DateTimeField(blank=True, null=True)
    due_amount = models.IntegerField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    final_due_date = models.DateTimeField(blank=True, null=True)
    interest_amount = models.IntegerField(blank=True, null=True)
    service_fee_amount = models.IntegerField(blank=True, null=True)
    cleared_date = models.DateTimeField(blank=True, null=True)
    loan_officer = models.ForeignKey(CompanyStaff,on_delete=models.SET_NULL, null=True, related_name='loans_as_officer')
    approved_by = models.ForeignKey(CompanyStaff,on_delete=models.SET_NULL, null=True, related_name='loans_as_manager')
    loan_purpose = models.TextField()
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    attachments = models.FileField(upload_to='loan_attachments/', null=True, blank=True) 
    # extras for written off loans 
    write_off_date = models.DateTimeField(blank=True, null=True)
    write_off_expense = models.IntegerField(blank=True, null=True)
    #parent loan
    parent_loan = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
   


    #Generating loan id based on date 
    def save(self, *args, **kwargs):
        if not self.loan_id:
            date_str = now().strftime('%Y%m%d')
            #averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_loan = Loan.objects.select_for_update().filter(loan_id__startswith=date_str).order_by('-loan_id').first()
                if last_loan:
                    last_id = last_loan.loan_id[-5:]
                    next_id = str(int(last_id)+1).zfill(5)
                    self.loan_id = date_str+next_id
                else:
                    self.loan_id = date_str+'00001'
        super(Loan, self).save(*args, **kwargs)

    #method to limit the application date input to be today or earlier date
    
    def clean(self):
        if self.application_date.date() > now().date():
            raise ValidationError('Application date cannot be in the future.')
            
    #method to calculate first_repayment_date
    def first_repayment_date(self):
        if self.loan_product.repayment_frequency == 'weekly':
            return self.application_date + timedelta(days=7)
        elif self.loan_product.repayment_frequency == 'monthly':
            return self.application_date + timedelta(days=30)
        elif self.loan_product.repayment_frequency == 'daily':
            self.application_date + timedelta(days=1)
        else:
            if self.loan_product.loan_term_period == 'day':
                return self.application_date + timedelta(days=self.loan_product.loan_product_term)
            elif self.loan_product.loan_term_period == 'week':
                return self.application_date + timedelta(days=self.loan_product.loan_product_term*7)
            elif self.loan_product.loan_term_period == 'month':
                return self.application_date + timedelta(days=self.loan_product.loan_product_term*30)
            else:
                return self.application_date + timedelta(days=self.loan_product.loan_product_term*365)
    
    
    #method to calculte the next payment date
    def next_payment_date(self):
        start_date = self.approved_date + timedelta(days=1) #consider adding grace period
        elapsed_days = (now().date() - start_date.date()).days 

        if self.loan_product.repayment_frequency == 'onetime':
            return self.due_date
        else:
            # Calculate the next payment date based on the loan's repayment frequency
            if self.loan_product.repayment_frequency == 'daily':
                interval_duration = 1
            elif self.loan_product.repayment_frequency == 'weekly':
                interval_duration = 7
            elif self.loan_product.repayment_frequency == 'monthly':
                interval_duration = 30

            # Calculate the number of intervals that have elapsed since the loan was disbursed
            intervals_elapsed = elapsed_days / interval_duration

            # Calculate the number of the next interval (e.g. the next month if the repayment frequency is monthly)
            next_interval = intervals_elapsed + 1

            # Calculate the date of the next payment by adding the duration of the next interval to the start date
            next_payment_date = start_date + timedelta(days=(next_interval * interval_duration)) 
            return next_payment_date

    #method to calculte the previous payment date
    def previous_payment_date(self):
        # Get the loan's payment frequency and number of installments
        payment_frequency = self.loan_product.repayment_frequency
        num_installments = self.num_installments
        
        # Calculate the interval duration based on the payment frequency
        if payment_frequency == 'daily':
            interval_duration = timedelta(days=1)
        elif payment_frequency == 'weekly':
            interval_duration = timedelta(days=7)
        elif payment_frequency == 'monthly':
            interval_duration = timedelta(days=30)

        
        # Get the current next payment date
        next_payment_date = self.next_payment_date()
        
        # Calculate the number of intervals that have elapsed since the start date
        intervals_elapsed = (next_payment_date - self.approved_date) // interval_duration
        
        if intervals_elapsed < 1:
            previous_payment_date = None

     
        # Calculate the number of the previous interval (e.g. the previous week if the repayment frequency is weekly)
        previous_interval = intervals_elapsed - num_installments + 1
        
        # Calculate the date of the previous payment by subtracting the duration of the previous interval from the next payment date
        previous_payment_date = next_payment_date - (previous_interval * interval_duration)
        
        return previous_payment_date

    #final payment date
    def final_payment_date(self):
        start_date = self.approved_date + timedelta(days=1) #1day grace period
        loan_term = self.loan_product.loan_product_term
        term_period = self.loan_product.loan_term_period
        if term_period == 'day':
            loan_term = timedelta(days=loan_term)
        elif term_period == 'week':
            loan_term = timedelta(days=loan_term * 7)
        elif term_period == 'month':
            loan_term = timedelta(days=loan_term * 30)
        elif term_period == 'year':
            loan_term = timedelta(days=loan_term * 365)

        final_date = start_date + loan_term 

        return final_date
    # method to calculate total_payable
    def total_payable(self):
        amount_payable = total_payable_amount(self)
        return amount_payable
    
    #method to find amount due per payment interval 
    def amount_due(self): #consider a scnerio where the borrower as defaulted more than once 
        payable = total_payable_amount(self)
        installment = installments(self)
        amount = payable / installment
        return amount     
    
    #penalty amount
    def late_penality(self):
        penality_amount = total_penalty(self)
        return penality_amount
    #method to calculte the loan balance
    def loan_balance(self):
        loan_object = Loan.objects.get(id=self.id)
        total_payable = loan_object.total_payable()

        # Get the sum of all loan repayments
        loan_repayments_sum = Repayment.objects.filter(loan_id=self).aggregate(Sum('amount'))['amount__sum']
        
        # If there are no loan repayments yet, set the sum to 0
        if loan_repayments_sum is None:
            loan_repayments_sum = 0

        loan_balance = total_payable - loan_repayments_sum
        
        if loan_balance < 0:
            loan_balance = 0
        
        return loan_balance
    
    #mehto to calculate amount based on borrower crdit score
    def amount_based_cs(self):
        amount = amount_based_cs(self)
        return amount
    
    #method to get final recomme principal amount
    def final_reco_amount(self): 
        amount = final_recommended_amount(self) 
        return amount

    #method to get final recomem amount times 3
    def final_amount_thrice(self): 
        amount = self.final_reco_amount() * 3
        return amount

    #method to check collateral value
    def collateral_value(self):
        # Loop through all collaterals of the loan object
        collaterals = Collateral.objects.filter(loan=self)
        value = 0
        if collaterals:
            for collateral in collaterals:
                value += collateral.estimated_value
            return value
        else:
            return value
    #method to get total credit score of guarantors
    def total_guarantor_score(self):
        score = 0
        guarantors = Guarantor.objects.filter(loan=self)
        for guarantor in guarantors:
            score += guarantor.name.credit_score
        return score

        
    class Meta:
        ordering = ['-application_date']
        permissions = [
            ('approve_loan', 'Can approve loan'),
            ('reject_loan', 'Can reject loan'),
            ('write_off_loan', 'Can write off loan'),
            ('rollover_loan', 'Can roll over loan'),
        ]


    def __str__(self):
        return self.member.first_name + ' ' + self.member.last_name



# Note models starts here   
class Note(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan =models.ForeignKey(Loan, on_delete=models.CASCADE, null=True)
    body= models.TextField()
    author= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add= True)
 

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]

#Note model ends

# Repayment models starts here   
class Repayment(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20)
    loan_id = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, related_name='repayments')
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    amount= models.IntegerField()
    date_paid = models.DateTimeField() 


    class Meta:
        ordering = ['-date_paid']

    def __str__(self):
        return self.member.first_name + ' ' + self.member.first_name
 

    

    def loanBalance(self):
        if self.loan_id:
            loan = Loan.objects.get(pk=self.loan_id.pk)
            loan_repayments = Repayment.objects.filter(loan_id=self.loan_id).aggregate(Sum('amount'))['amount__sum']
            total_payable = loan.total_payable()
            loan_balance = total_payable - loan_repayments
            return loan_balance

    #method to calculate next_repayment_date
    def next_repayment_date(self):
        start_date = self.loan_id.approved_date + timedelta(days=1)
        if self.loan_id:
            if self.loan_id.loan_product.repayment_frequency == 'weekly':
                return self.date_paid + timedelta(days=7)
            elif self.loan_id.loan_product.repayment_frequency == 'monthly':
                return self.date_paid + timedelta(days=30)
            elif self.loan_id.loan_product.repayment_frequency == 'daily':
                return self.date_paid + timedelta(days=1)
            else:
                if self.loan_id.loan_product.loan_term_period == 'day': 
                    return start_date + timedelta(days=self.loan_id.loan_product.loan_product_term)
                elif self.loan_id.loan_product.loan_term_period == 'week': 
                    return start_date + timedelta(days=self.loan_id.loan_product.loan_product_term * 7)
                elif self.loan_id.loan_product.loan_term_period == 'month': 
                    return start_date + timedelta(days=self.loan_id.loan_product.loan_product_term * 30)
                else:
                    return start_date + timedelta(days=self.loan_id.loan_product.loan_product_term * 365)
        
    

#Repayment model ends 

#Guarantor Model starts
class Guarantor(models.Model):
    company =models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan =models.ForeignKey(Loan, on_delete=models.CASCADE, related_name = 'loan_as_no')
    name= models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    amount= models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
 

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.name)

#Collateral Model starts
TYPE = (
    ('electronics','ELECTRONICS'),
    ('vehicle','VEHICLE'),
    ('land','LAND'),
    ('shares','SHARES'),
    ('cash deposit','CASH DEPOSIT'),
    ('others','OTHERS'),
)
class Collateral(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan = models.ForeignKey(Loan, on_delete= models.CASCADE, null=True)
    name =models.CharField(max_length=200)
    type= models.CharField(max_length=50, choices=TYPE, default='electronics')
    serial_number= models.CharField(max_length=200)
    estimated_value = models.IntegerField()
 

    def __str__(self):
        return self.name  

class MpesaStatement(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan = models.ForeignKey(Loan, on_delete= models.CASCADE, null=True, related_name='statements')
    owner = models.ForeignKey(Member, on_delete= models.CASCADE, null=True)
    code =models.CharField(max_length=20)
    statements = models.FileField(upload_to='mpesa-statements/', null=True, blank=True) 

    def __str__(self):
        return self.owner.first_name + ' ' + self.owner.last_name