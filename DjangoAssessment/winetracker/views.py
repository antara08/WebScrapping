from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Wine, StoreWine
from .forms import WineForm, StoreForm, InventoryForm


# /wines/
def wine_list(request):
    if request.method == "POST":
        form = WineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Wine created successfully.")
            return redirect("wines:list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WineForm()

    wines_qs = Wine.objects.order_by("name")
    paginator = Paginator(wines_qs, 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,
    }
    return render(request, "wines/list.html", context)


# /wines/<uuid:wine_id>/  → wines:detail
def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    inventories = wine.inventories.select_related("store")
    context = {
        "wine": wine,
        "inventories": inventories,
    }
    return render(request, "wines/detail.html", context)


# /stores/new/  → stores:new
def store_new(request):
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Store created successfully.")
            return redirect("wines:list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StoreForm()

    return render(request, "stores/new.html", {"form": form})


# /inventory/  → inventory:maintain
def maintain_inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory updated successfully.")
            return redirect("inventory:maintain")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InventoryForm()

    inventories = (
        StoreWine.objects.select_related("store", "wine")
        .order_by("store__name", "wine__name")
    )

    context = {
        "form": form,
        "inventories": inventories,
    }
    return render(request, "inventory/maintain.html", context)
