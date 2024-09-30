from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomerProfile(models.Model):
    COMPANY_CHOICES = (
        ('sole_proprietorships', 'Sole Proprietorships'),
        ('partnerships ', 'Partnerships '),
        ('limited_company', 'Limited Company'),
    )
    ref_no = models.CharField("Refenence number", max_length=50,)
    chinese_name = models.CharField("Chinese name", max_length=50,blank=True, null=True)
    english_name = models.CharField("English name", max_length=50,blank=True, null=True)
    revenue_sharing = models.IntegerField("Revenue sharing")
    br_no = models.CharField("BR no.", max_length=50,blank=True, null=True)
    br_expiry_date = models.DateField("BR Expiry Date", blank=True, null=True)
    company_type = models.CharField("Company Type", max_length=50, choices=COMPANY_CHOICES, blank=True, null=True)
    company_address = models.CharField("Company Address", max_length=100,blank=True, null=True)
    category = models.CharField("Category", max_length=50,blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="Phone number must be 8 digits.")
    tvp_contact_no = models.CharField("TVP contact phone number", validators=[phone_regex], max_length=8,blank=True, null=True)
    company_email = models.EmailField("Company Email", blank=True, null=True)
    company_email_password = models.CharField("Company Email Password", max_length=50,blank=True, null=True)
    tvp_registerd_email = models.EmailField("TVP Registered Email",blank=True, null=True)
    tvp_registerd_email_password = models.CharField("TVP Registerd Email Password", max_length=50,blank=True, null=True)
    referrer = models.ForeignKey('data.RefererProfile', on_delete=models.PROTECT, related_name='referrer_set', blank=True, null=True)
    mpf_pending_no = models.CharField("MPF Pending Number", max_length=50,blank=True, null=True)
    mpf_account = models.CharField("MPF Account", max_length=50,blank=True, null=True)
    mpf_password = models.CharField("MPF Password", max_length=50,blank=True, null=True)
    closed =  models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.closed:
            return f'{self.ref_no} closed'
        return self.ref_no

class OwnerProfile(models.Model):
    ref_no = models.ForeignKey('data.CustomerProfile', on_delete=models.CASCADE, verbose_name = 'Owners', related_name='owner_set')
    owner_chinese_name = models.CharField("Owner Chinese name", max_length=50,blank=True, null=True)
    owner_english_name = models.CharField("Owner English name", max_length=50)
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="Phone number must be 8 digits.")
    phone = models.CharField(validators=[phone_regex], max_length=8,blank=True, null=True)
    shares = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-shares']

    def __str__(self):
        return f'{self.owner_english_name}'

class RefererProfile(models.Model):
    ref_no = models.CharField("Refenence number", max_length=50,)
    referrer_name = models.CharField("Referrer name", max_length=50, blank=True, null=True)
    referral_times = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.ref_no}' + ' - ' + f'{self.referrer_name}' + ' : $' + f'{self.balance}'

class CustomerLedger(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
    customer_bank_ac = models.CharField("Customer Bank Account", max_length=50,blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_changes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.ref_no} - Balance: {self.balance}"

class BalanceChange(models.Model):
    receiver = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='balance_receiver_set')
    transaction_date = models.DateTimeField(null=True, blank=True)
    transaction_type = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.receiver} - Balance Change: {self.amount}"


@receiver(post_save, sender=OwnerProfile)
def createuser(sender, instance, created,**kwargs):
    if created:
        RefererProfile.objects.create(ref_no = instance.ref_no ,referrer_name = instance.owner_english_name,)

@receiver(post_save, sender=CustomerProfile)
def createreferrer(sender, instance, created,**kwargs):
    if created:
        CustomerLedger.objects.create(customer = instance)
        if instance.referrer:
            referrer = RefererProfile.objects.get(referrer_name = instance.referrer)
            referrer.referral_times += 1
            referrer.balance += 3000
            referrer.save()

@receiver(post_save, sender=BalanceChange)
def createreferrer(sender, instance, created,**kwargs):
    if created:
        receiver = CustomerLedger.objects.get(customer = instance.receiver)
        if instance.amount > 0:
            receiver.balance += instance.amount
            change = f"{instance.transaction_type}: +{instance.amount}"
            if instance.transaction_date:
                change += f" ({instance.transaction_date.strftime('%Y-%m-%d %H:%M:%S')})"
            receiver.balance_changes += change + "\n"
            receiver.save()
        elif instance.amount < 0:
            receiver.balance += instance.amount
            change = f"{instance.transaction_type}: -{instance.amount}"
            if instance.transaction_date:
                change += f" ({instance.transaction_date.strftime('%Y-%m-%d %H:%M:%S')})"
            receiver.balance_changes += change + "\n"
            receiver.save()