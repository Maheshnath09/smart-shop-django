# My Store - E-commerce Platform

A modern, full-featured e-commerce platform built with Django 5.2, featuring AI-powered product recommendations, user authentication, wishlist management, and a responsive mobile-first design.

![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🛒 Core E-commerce
- **Product Catalog** - Browse products by categories with search functionality
- **Shopping Cart** - Session-based cart with quantity management
- **Order Management** - Complete checkout flow with order history
- **User Profiles** - Extended user profiles with personal information

### 🤖 AI Recommendations
- **Personalized Suggestions** - ML-powered recommendations based on user behavior
- **"Recommended for You"** - Homepage section with personalized picks
- **"You May Also Like"** - Related products on product detail pages
- **Works for Guests** - Session-based tracking for non-logged users

### ❤️ Wishlist
- **Save Favorites** - Add/remove products to personal wishlist
- **Quick Access** - Heart icon on all product cards ♥

### 📱 Mobile-First Design
- **Responsive UI** - Optimized for all screen sizes
- **Dark Theme** - Modern dark mode interface
- **Touch-Friendly** - Large tap targets for mobile users

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Templates  │  │   Static    │  │    Responsive CSS       │  │
│  │   (HTML)    │  │  (CSS/JS)   │  │   (Mobile-First)        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                         │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────────────┐  │
│  │ Products  │ │   Cart    │ │  Orders   │ │ Recommendations │  │
│  │   App     │ │   App     │ │   App     │ │      App        │  │
│  └───────────┘ └───────────┘ └───────────┘ └─────────────────┘  │
│  ┌───────────┐ ┌───────────┐                                    │
│  │ Accounts  │ │ Wishlist  │     ┌──────────────────────────┐   │
│  │   App     │ │   App     │     │   ML Recommendation      │   │
│  └───────────┘ └───────────┘     │      Engine              │   │
│                                  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    SQLite Database                          ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐   ││
│  │  │Products │ │ Orders  │ │Wishlist │ │  ProductViews   │   ││
│  │  │Category │ │OrderItem│ │         │ │ (ML Tracking)   │   ││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘   ││
│  │  ┌─────────┐ ┌─────────┐                                   ││
│  │  │  User   │ │ Profile │                                   ││
│  │  └─────────┘ └─────────┘                                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
my_store/
├── accounts/              # User authentication & profiles
│   ├── models.py          # Profile model
│   ├── views.py           # Login, signup, profile views
│   └── templates/         # Auth templates
├── products/              # Product catalog
│   ├── models.py          # Product, Category models
│   ├── views.py           # List, detail, search views
│   └── templates/         # Product templates
├── cart/                  # Shopping cart
│   ├── cart.py            # Cart session management
│   ├── views.py           # Add, remove, update cart
│   └── context_processors.py
├── orders/                # Order processing
│   ├── models.py          # Order, OrderItem models
│   └── views.py           # Checkout, order history
├── wishlist/              # Wishlist functionality
│   ├── models.py          # Wishlist model
│   └── views.py           # Add/remove wishlist items
├── recommendations/       # AI recommendation engine
│   ├── models.py          # ProductView tracking
│   ├── engine.py          # ML recommendation logic
│   ├── utils.py           # Helper functions
│   └── middleware.py      # Session tracking
├── static/css/            # Custom CSS styles
├── templates/             # Base templates
└── config/                # Django settings
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/my_store.git
cd my_store

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with:
# SECRET_KEY=your-secret-key
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the app!

---

## 🔧 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django 5.2** | Web framework |
| **SQLite** | Database (dev) |
| **Pillow** | Image processing |
| **django-crispy-forms** | Form rendering |
| **crispy-bootstrap5** | Bootstrap 5 forms |
| **python-decouple** | Environment variables |

---

## 📱 Screenshots

### Homepage with Recommendations
The homepage displays personalized product recommendations based on user browsing history.

### Product Categories
Browse products organized by categories: Electronics, Clothing, Books, Beauty, Home & Kitchen.

### Shopping Cart
Add products to cart, update quantities, and proceed to checkout.

---

## 🤖 Recommendation System

The app features a hybrid ML recommendation engine:

1. **Content-Based Filtering** - Suggests products from similar categories
2. **Collaborative Filtering** - "Users who viewed X also viewed Y"
3. **Behavioral Signals**:
   - Purchase history
   - Wishlist items
   - Product views
   - Category preferences

### How It Works
```python
# Tracks every product view
track_product_view(request, product)

# Gets personalized recommendations
recommendations = get_recommendations(request, limit=8)
```

---

## 🛠️ Configuration

### Environment Variables (.env)
```
SECRET_KEY=your-super-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECURE_SSL_REDIRECT=False
```

### Production Settings
For production deployment, update the following in `.env`:
```
DEBUG=False
SECURE_SSL_REDIRECT=True
ALLOWED_HOSTS=yourdomain.com
```

---

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Product listing |
| `/category/<slug>/` | GET | Products by category |
| `/product/<category>/<slug>/` | GET | Product detail |
| `/search/` | GET | Search products |
| `/cart/` | GET | View cart |
| `/cart/add/<id>/` | POST | Add to cart |
| `/cart/remove/<id>/` | POST | Remove from cart |
| `/orders/create/` | POST | Create order |
| `/wishlist/` | GET | View wishlist |
| `/wishlist/add/<id>/` | GET | Add to wishlist |
| `/accounts/login/` | GET/POST | User login |
| `/accounts/signup/` | GET/POST | User registration |
| `/accounts/profile/` | GET/POST | User profile |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Built with ❤️ using Django

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap 5
- Crispy Forms
