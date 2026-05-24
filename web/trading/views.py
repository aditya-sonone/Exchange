from django.shortcuts import render

from .forms import OrderForm

from generated.python.order import Order
from generated.python.side import Side

from .client import send_packet


def order_view(request):

    msg = None

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            order = Order()

            order.orderId = form.cleaned_data["orderId"]

            order.side = Side(
                int(form.cleaned_data["side"])
            )

            order.price = form.cleaned_data["price"]

            order.quantity = form.cleaned_data["quantity"]

            packet = order.serialize()

            response = send_packet(packet)

            msg = (
                f"ACK Received | "
                f"OrderId={response.orderId} | "
                f"Filled={response.filledQty} | "
                f"Remaining={response.remainingQty}"
            )

    else:

        form = OrderForm()

    return render(
        request,
        "trading/order.html",
        {
            "form": form,
            "message": msg
        }
    )