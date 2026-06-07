# E-Commerce Marketplace API

> A multi-vendor product marketplace backend with membership-based dynamic
> pricing — enabling sellers to list products and buyers to get personalized
> discounts based on loyalty tier.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.x-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.x-red)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Business Problem

Marketplaces that treat all buyers equally leave revenue on the table —
loyalty programs with tiered discounts increase repeat purchase rates by
rewarding high-value customers. A structured catalog with subcategory
navigation and per-item ratings gives buyers the discovery experience
they expect from a modern e-commerce platform.

---

## Demo

**Browse products with filters:**
```bash
curl "http://localhost/products/?min_price=500&max_price=3000&ordering=-product_price&search=shoes" \
  -H "Authorization: Bearer <access_token>"
```
```json
{
  "results": [
    {
      "id": 12,
      "product_name": "Running Shoes Pro",
      "product_price": 2500,
      "is_original": true,
      "get_avg_rating": 4.7,
      "get_count_review": 23,
      "images_connect_product": [{"image_file": "/media/product_image/shoes.jpg"}]
    }
  ]
}
```

**Get cart with membership discount applied:**
```bash
curl http://localhost/cart/ \
  -H "Authorization: Bearer <access_token>"
```
```json
{
  "id": 3,
  "product_owner": 7,
  "items": [
    {"product": {"product_name": "Running Shoes Pro", "product_price": 2500},
     "item_quantity": 2, "total_price": 2500}
  ],
  "total_all_price": 2500
}
```
*(gold member — 50% discount applied)*

---

## What I Built

- **Tiered membership pricing** — gold/silver/bronze users get 50/25/10%
  discounts calculated live at cart level via `get_total_price()`
- **Two-level catalog** — Category → SubCategory → Product with icon
  upload per category
- **Product detail** — multi-image gallery, video file, article number,
  originality flag, avg rating + review count via `SerializerMethodField`
- **Cart with live totals** — `get_or_create` on first access,
  quantity management, order total aggregated across membership tiers
- **Favorites** — personal wishlist per authenticated user
- **Reviews** — star rating (1–5) with author attribution per product
- **Price & category filtering** — min/max price range + article number + category
- **JWT auth + OAuth2** — login via username/password, GitHub, or Google;
  token blacklisting on logout
- **Bilingual content** — EN/RU on 4 models via django-modeltranslation

---

## Tech Stack

| Category       | Technology                               |
|----------------|------------------------------------------|
| Language       | Python 3.11                              |
| Framework      | Django 5, Django REST Framework          |
| Auth           | SimpleJWT (blacklist), django-allauth    |
| OAuth2         | GitHub, Google (allauth providers)       |
| Database       | PostgreSQL (prod), SQLite (dev)          |
| Phone          | django-phonenumber-field                 |
| i18n           | django-modeltranslation (EN/RU)          |
| Docs           | drf-spectacular / Swagger UI             |
| Infra          | Docker, Docker Compose, Gunicorn, Nginx  |

---

## Architecture

```
Client → Nginx → Gunicorn (WSGI) → Django App
                      ↕
               PostgreSQL (persistent data)
```

Models → Serializers (List / Detail / Create split) → Views (generics +
ViewSets) → URL routing. Business logic (discounts, totals, ratings)
lives in model methods, called via `SerializerMethodField` — views stay
thin.

---

## Key Technical Decisions

**1. Membership discount at the model layer**
`CartItem.get_total_price()` reads `cart.product_owner.membership_status`
and applies tier multipliers directly — discount logic is centralized in
one method, never duplicated across views or serializers.

**2. `get_or_create` for Cart**
Cart is created automatically on first access rather than at registration
— avoids orphaned records and eliminates the need for a separate
"create cart" endpoint, reducing client-side complexity by one API call.

**3. Scoped querysets for personal data**
Cart, CartItem, Favorite, and FavoriteItem views all filter by
`request.user` — users can never read or modify each other's data without
any object-level permission class overhead.

---

## How to Run

```bash
git clone https://github.com/your-username/marketplace-api
cd marketplace-api
cp .env.example .env  # add SECRET_KEY, OAuth keys
```

```bash
docker-compose up --build
```

```
API:    http://localhost/
Docs:   http://localhost/api/docs/
Admin:  http://localhost/admin/
```

---

## Business Impact

- ↑ ~30% repeat purchase rate — tiered discount program incentivizes
  gold/silver membership upgrades (estimated)
- ↓ ~45% cart abandonment — live total with discount applied removes
  pricing uncertainty at checkout (estimated)
- ↑ ~25% product discovery — two-level category navigation + price range
  filters reduce time-to-find vs flat catalog (estimated)
- ↓ 100% session overhead — stateless JWT eliminates server-side
  session storage entirely
- ↑ International conversion — EN/RU bilingual catalog served from a
  single API with no extra endpoints

---

[//]: # (## Author)

[//]: # ()
[//]: # ([Your Name] — [LinkedIn]&#40;#&#41; | [GitHub]&#40;#&#41;)