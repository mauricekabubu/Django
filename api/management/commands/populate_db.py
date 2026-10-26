from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import Order, OrderItem, Product, User


class Command(BaseCommand):
    help = "Populate the database with sample products and orders for an existing superuser."

    PRODUCTS = [
        ("A Scanner Darkly", "A science fiction novel by Philip K. Dick.", "12.99", 4),
        ("Coffee Machine", "A compact automatic coffee machine.", "70.99", 6),
        ("Velvet Underground & Nico", "The classic debut album by The Velvet Underground.", "15.99", 11),
        ("Enter the Wu-Tang (36 Chambers)", "A landmark hip-hop album.", "17.99", 2),
        ("Digital Camera", "A lightweight digital camera for everyday photography.", "350.99", 4),
        ("Watch", "A stainless steel wristwatch.", "500.05", 0),
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True).order_by("id").first()
        if user is None:
            raise CommandError(
                "No superuser exists. Create one with 'python manage.py createsuperuser' and run this command again."
            )

        products = []
        for name, description, price, stock in self.PRODUCTS:
            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": Decimal(price),
                    "stock": stock,
                },
            )
            products.append(product)

        # Keep the seed repeatable: create the sample orders once for this user.
        if not Order.objects.filter(user=user).exists():
            order_specs = [
                (Order.StatusChoices.PENDING, [(products[0], 1), (products[1], 2)]),
                (Order.StatusChoices.CONFIRMED, [(products[2], 1), (products[3], 1)]),
                (Order.StatusChoices.CANCELLED, [(products[4], 1), (products[5], 1)]),
            ]
            for status, items in order_specs:
                order = Order.objects.create(user=user, status=status)
                OrderItem.objects.bulk_create(
                    [
                        OrderItem(order=order, product=product, quantity=quantity)
                        for product, quantity in items
                    ]
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Database populated: {len(products)} sample products; orders are linked to superuser '{user.username}'."
            )
        )
