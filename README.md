# Product Recommendation engine using Django

[Video Link for the tutorial](https://www.youtube.com/watch?v=eGHN3XvBBv8)

[![Watch the Video](https://img.youtube.com/vi/eGHN3XvBBv8/sddefault.jpg)](https://www.youtube.com/watch?v=eGHN3XvBBv8D)


# 🚀 Overview

A powerful Django-based recommendation engine that provides personalized suggestions by leveraging user interactions and preferences.

This project utilizes advanced machine learning algorithms, collaborative filtering, and content-based filtering to deliver highly accurate recommendations. It's designed to be scalable and adaptable, making it perfect for building personalized experiences in e-commerce, media streaming, and content platforms.


# 🎯 Features

User-Based Collaborative Filtering

Item-Based Collaborative Filtering

Content-Based Filtering

Hybrid Recommendation System

Real-time Suggestions

Scalable and Modular Design

Admin Panel for Managing Data

# 🏗️ Project Structure

```
recommendation_engine/
│
├── recommendation_engine/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── recommender/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── db.sqlite3
├── manage.py
└── requirements.txt

```

# 🛠️ Installation

Clone the Repository

```
git clone https://github.com/boxabhi/recommendation-engine
cd recommendation_engine

Create and Activate a Virtual Environment

python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`

Install Dependencies

pip install -r requirements.txt

Run Migrations

python manage.py migrate

Create a Superuser (Optional)

Start the Development Server

python manage.py runserver
```

# 📊 How It Works

Data Collection: User interaction data is collected and stored in the database.

Processing: The system analyzes user behavior, ratings, and preferences.

Model Training: Machine learning models are trained on collected data.

Recommendations: Users receive personalized suggestions based on predictions.

# 🔧 Configuration

Algorithm Choice: Easily switch between collaborative filtering, content-based, or hybrid approaches in the settings.

Thresholds: Customize thresholds for similarity and recommendation confidence.

# 📂 Models

```

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_image = models.URLField()
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('purchase', 'Purchase'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.product}"


```

# 🌐 API Endpoints

/recommendations/user/<int:id>/ – Get recommendations for a specific user.

/recommendations/item/<int:id>/ – Retrieve similar items.

# 🎨 Frontend Integration

Easily integrates with React, Vue, or any other frontend framework.

Provides API endpoints for dynamic fetching of recommendations.

# 🤝 Contribution Guidelines

We welcome contributions! Please follow these steps:

Fork the project.

Create a feature branch.

Commit changes and push.

Submit a pull request.

# 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

# 📩 Contact

For queries, reach out to:

Name: Abhijeet Gupta

Email: abhijeetg40@gmail.com

LinkedIn: Abhijeet Gupta

# ⭐ Support the Project

If you find this project useful, please consider giving it a star ⭐ on GitHub!

This project is part of a Django course on creating advanced web applications. Stay tuned for more tutorials!




