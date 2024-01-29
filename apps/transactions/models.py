from django.db import models

from apps.users.models import User

class Transactions(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_completed:
            raise ValueError("Transaction is already completed.")
        
        if not self.is_completed:
            from_user_balance = self.from_user.balance
            to_user_wallet = self.to_user.wallet

            if from_user_balance >= self.amount:
                self.from_user.balance -= self.amount
                self.to_user.wallet += self.amount

                self.is_completed = True

                self.from_user.save()
                self.to_user.save()
                super(Transactions, self).save(*args, **kwargs)
            else:
                raise ValueError("Insufficient funds for the transaction.")
            
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
