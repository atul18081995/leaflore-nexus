from django.db import models
from plants.models import Plant
from django.conf import settings

class NurseryProfile(models.Model):
    plant = models.OneToOneField(
        Plant,
        on_delete=models.CASCADE,
        related_name="nursery"
    )

    is_sellable = models.BooleanField(default=False)

    propagation_method = models.CharField(
        max_length=100,
        help_text="Seed / Cutting / Grafting / Tissue Culture"
    )

    grow_time_days = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("hard", "Hard"),
        ]
    )

    nursery_notes = models.TextField(blank=True)

    def __str__(self):
        return f"NurseryProfile: {self.plant.common_name}"

class StockNotification(models.Model):
    plant = models.ForeignKey(
        "plants.Plant",
        on_delete=models.CASCADE,
        related_name="stock_notifications"
    )
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ("plant", "email")

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    email = models.EmailField(null=True, blank=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "email", "plant")

    def __str__(self):
        return f"Wishlist: {self.plant.common_name}"