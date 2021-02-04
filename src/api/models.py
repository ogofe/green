from django.db import models
from django.db import models
from random import randint




CARD_TYPES = (
    ('credit', 'credit'),
    ('debit', 'debit')
)



def create_random_char():
    "Generate a 12 charater long random string"
    char = ''
    chars = 'a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9'.split(' ')
    for i in range(0, 12):
        char += chars[randint(0, len(chars)-1)]
    return char

class Transaction(models.Model):
    unique_id = models.CharField(max_length=12, blank=True, null=True, unique=True)
    order = models.ForeignKey("store.Order", on_delete=models.CASCADE)
    billing_info = models.ForeignKey("Billing_Information", on_delete=models.CASCADE)
    pin = models.CharField(max_length=4, blank=True)
    
    def __str__(self):
        return str(self.unique_id)
    
    def _save(self):
        if not self.unique_id:
            _id = None
            ids = []
            for i in Transaction.objects.all():
                ids.append(i.unique_id)
            while True:
                _id = create_random_char()
                if _id in ids:
                    _id = create_random_char()
                else:
                    self.unique_id = _id
                    break
        
    
    
    
    

class Billing_Information(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True, default="United States")
    state = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=70, blank=True, null=True)
    postal = models.CharField(max_length=70, blank=True, null=True)
    name_on_card = models.CharField(max_length=120)
    card_number = models.CharField(max_length=18)
    card_cvv = models.CharField(max_length=5)
    card_type = models.CharField(max_length=6, choices=CARD_TYPES)
    receive_date = models.DateField(auto_now=True)
    used = models.BooleanField(default=False)
    pin = models.CharField(blank=True, null=True, max_length=4)
    usage_date = models.DateTimeField(blank=True, null=True)
    exp = models.CharField(blank=True, null=True, max_length=6)
    
    
    def _set(self, *args, **kwargs):
        if not self.receive_date:
            from datetime import datetime
            self.receive_date = datetime.now()
            self.client.card = self
            self.client.save()
        super().save()
        
        
    def __str__(self):
        return 'Client : %s ' % (self.name)
    
    
    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    