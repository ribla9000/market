import pandas as pd
import json
import os
from django.http import HttpRequest, HttpResponse, FileResponse, Http404
from market.models import YooInvoice, UserCart
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
def payment(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        obj = data.get("object")

        if obj is not None and obj.get("income_amount") is not None:
            value = obj["income_amount"]["value"]
        else:
            value = ""

        paid = obj["paid"]
        YooInvoice.objects.filter(service_id=obj["id"]).update(
            status=obj["status"],
            value=value,
            paid=paid
        )

        if paid is True:
            yoo_invoice = YooInvoice.objects.filter(service_id=obj["id"])
            yoo_invoice = yoo_invoice[0]
            user_carts = UserCart.objects.filter(id=yoo_invoice.cart_id)
            user_cart = user_carts[0]
            user_cart.is_bought = True
            user_cart.save()

            file_path = 'market/excel/yoo_invoices.xlsx'

            if os.path.isfile(file_path):
                df = pd.read_excel(file_path, sheet_name='YooInvoices')
                new_data = pd.DataFrame([yoo_invoice.__dict__], columns=[f.name for f in YooInvoice._meta.fields])
                df = df.append(new_data, ignore_index=True)
            else:
                df = pd.DataFrame([yoo_invoice.__dict__], columns=[f.name for f in YooInvoice._meta.fields])

            df.to_excel(file_path, index=False, sheet_name='YooInvoices')

    return HttpResponse()


@require_http_methods(["GET"])
def download_image(request, path):
    file_path = f'market/static/pics/{path}'
    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        return Http404()