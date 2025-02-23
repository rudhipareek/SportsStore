import os
import django

# Ensure Django settings are configured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportstore.settings")

django.setup()

import csv
import requests
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from products.models import Product
from io import BytesIO



def download_image(image_url):
    """Download image from URL and return a Django File object."""
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            file_name = image_url.split("/")[-1]  # Extract filename from URL
            return file_name, ContentFile(response.content)  # Convert to Django file
        else:
            print(f"⚠ Failed to download {image_url}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"⚠ Error downloading {image_url}: {e}")
        return None, None

def import_products_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            description = row['description']
            price = row['price']
            category = row['category']
            image_url = row['image_url']

            # Check if product already exists
            if Product.objects.filter(name=name, category=category).exists():
                print(f"⚠ Product already exists: {name}")
                continue

            # Download and attach image
            file_name, image_file = download_image(image_url)
            if image_file:
                product = Product(name=name, description=description, price=price, category=category)
                product.image.save(file_name, image_file)  # Save image to ImageField
                product.save()
                print(f"✔ Product added: {name}")
            else:
                print(f"❌ Failed to add product: {name}")

# Run the script
csv_path = r"C:\Users\RUDHI PAREEK\OneDrive\Desktop\Store\sportstore\products\products.csv"  # Change this to your actual CSV file path
import_products_from_csv(csv_path)
