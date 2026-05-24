from django import forms


class OrderForm(forms.Form):

    orderId = forms.IntegerField()

    side = forms.ChoiceField(
        choices=[
            (0, "BUY"),
            (1, "SELL"),
        ]
    )

    price = forms.IntegerField()

    quantity = forms.IntegerField()