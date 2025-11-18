# 🍷 Wine Tracker – Django Candidate Exercise

## Overview

Welcome to the **Wine Tracker** coding exercise.

Your task is to complete a small Django application that tracks wines, the stores that sell them, and each store’s inventory.  
This exercise assesses your ability to use Django’s core features — **models, forms, validation, views, routing, and templates**.

---

## 🧩 Requirements Summary

### 1. Models

Create three models with migrations:

#### **Wine**

| Field          | Type                                           | Notes                                        |
| -------------- | ---------------------------------------------- | -------------------------------------------- |
| `id`           | `UUIDField`                                    | Primary key, auto-generated (`uuid4`)        |
| `name`         | `CharField(max_length=200)`                    | Required                                     |
| `manufacturer` | `CharField(max_length=200)`                    | Required                                     |
| `type`         | `CharField(choices=TYPE_CHOICES)`              | Choices: `red`, `white`, `rose`, `specialty` |
| `is_vintage`   | `BooleanField(default=False)`                  | Indicates vintage or non-vintage             |
| `sweetness`    | `CharField(choices=SWEETNESS_CHOICES)`         | `dry`, `off-dry`, `sweet`, `very-sweet`      |
| `price`        | `DecimalField(max_digits=8, decimal_places=2)` | Must be ≥ 0                                  |

**Validation Rule:**  
If `price > 30.00`, `is_vintage` **must** be `True`.  
This should be enforced in the Django Form’s `clean()` method.

---

#### **Store**

| Field     | Type                        | Notes       |
| --------- | --------------------------- | ----------- |
| `id`      | `AutoField`                 | Primary key |
| `name`    | `CharField(max_length=200)` | Required    |
| `address` | `CharField(max_length=300)` | Required    |

---

#### **StoreWine (Inventory)**

| Field      | Type                                          | Notes                       |
| ---------- | --------------------------------------------- | --------------------------- |
| `id`       | `AutoField`                                   | Primary key                 |
| `store`    | `ForeignKey(Store, on_delete=models.CASCADE)` | Related name: `inventories` |
| `wine`     | `ForeignKey(Wine, on_delete=models.CASCADE)`  | Related name: `inventories` |
| `quantity` | `PositiveIntegerField(default=0)`             | Inventory quantity          |

**Constraint:** Each `(store, wine)` pair must be unique.

---

### 2. Views & Routes

| Route                    | Description                                                     |
| ------------------------ | --------------------------------------------------------------- |
| `/wines/`                | Default page – create new wine and view paginated list of wines |
| `/wines/<uuid:wine_id>/` | Detail page for a wine with its store inventories               |
| `/stores/new/`           | Create new store form (redirects to `/wines/` on success)       |
| `/inventory/`            | Maintain wine inventories per store                             |

---

### 3. Forms

Use Django’s built-in **Form** and **ModelForm** classes.

#### **WineForm**

- Based on `Wine` model.
- Validate that if `price > 30.00`, then `is_vintage` is `True`.

#### **StoreForm**

- Based on `Store` model.

#### **Inventory Form**

- Allows selecting a Store and Wine, and setting quantity.
- If `(store, wine)` already exists, update it. Otherwise create a new record.

**All validation must occur before saving objects.**

---

### 4. Templates

Use Django templates (no external CSS frameworks required).

#### Required Templates

- `wines/list.html` – Form for new wine + paginated wine list
- `wines/detail.html` – Displays wine details and list of stores carrying it
- `stores/new.html` – New store creation form
- `inventory/maintain.html` – Maintain inventory entries

Use minimal structure (tables, forms, buttons, links).  
Add a “Create Store” button on the wine list page.

---

### 5. Pagination & Redirects

- Wine list must be paginated (e.g. 10–20 items per page).
- Use **POST-Redirect-GET (PRG)** pattern:
  - After saving a form, redirect to a clean page state.
- Redirects:
  - After creating a Store → `/wines/`
  - After creating a Wine → `/wines/`
  - After updating Inventory → `/inventory/`

---

### 6. URL Naming

Use namespaced URLs:

- `wines:list`
- `wines:detail`
- `stores:new`
- `inventory:maintain`

---

### 7. Messages (Optional)

Use Django’s `messages` framework for success/error notifications after form submissions.

---

### 8. Admin (Optional)

Register `Wine`, `Store`, and `StoreWine` in Django Admin to help inspection.

---

## ✅ Acceptance Criteria

You’ll be evaluated on:

1. **Model accuracy** (UUID PK, constraints, relationships).
2. **Form validation** (must prevent invalid submissions).
3. **Routing & redirects** working as specified.
4. **Pagination** on wine list.
5. **Template usage** (no DRF - Django Rest Framework, pure HTML rendering).
6. **Code clarity & organization** (readable, modular, committed logically).

---

## 🧠 Bonus (Optional)

- Add a search/filter on `/wines/`
- Add unit tests for form validation and model logic
- Add `__str__()` methods for all models
- Improve templates with light styling

---

## ⚙️ Setup Instructions

```bash

# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
# This step completed for initial db use the db.sqlite3
python manage.py migrate

# 5. Start the development server
python manage.py runserver
```
