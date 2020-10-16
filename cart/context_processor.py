def cart_total_amount(request):
    total = 0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            total = total + (float(value['price'])*value['quantity'])
    return {'cart_total_amount': total}

# ESTA ES UNA VARIABLE GLOBAL Y FUNCIONA EN TODOS LOS TEMPLATES


def cart_total_products(request):
    cont = 0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            if(value['price'] == value['price']):
                cont = cont+value['quantity']
            else:
                cont = cont+1
    return {'cart_total_products': cont}
