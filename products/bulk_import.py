import os
import sys
import django
import csv
import requests
from django.core.files.base import ContentFile
from django.conf import settings

# Add project directory to Python path to ensure Django finds the app
sys.path.append(r"C:/Users/RUDHI PAREEK/Desktop/Store/sportstore")

# Ensure Django settings are configured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportstore.settings")
django.setup()

# Now import the Product model
from products.models import Product

# Logging and Image Download Functionality
import logging
from io import BytesIO

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def download_image(image_url):
    """Download image from URL and return a Django File object."""
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        file_name = image_url.split("/")[-1]  # Extract filename from URL
        return file_name, ContentFile(response.content)  # Convert to Django file
    except requests.exceptions.RequestException as e:
        logging.warning(f"⚠ Image download failed [{image_url}]: {e}")
        return None, None

def import_products_from_csv(csv_path):
    try:
        with open(csv_path, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            products_to_create = []
            skipped_products = 0

            for idx, row in enumerate(reader, start=1):
                try:
                    name = row['name'].strip()
                    description = row['description'].strip()
                    price = float(row['price'])
                    category = row['category'].strip()
                    image_url = row['image_url'].strip()

                    # Check if product already exists
                    if Product.objects.filter(name=name, category=category).exists():
                        logging.warning(f"⚠ Skipping existing product: {name}")
                        skipped_products += 1
                        continue

                    # Download and attach image
                    file_name, image_file = download_image(image_url)

                    # Create product instance (without saving)
                    product = Product(
                        name=name, description=description, price=price, category=category
                    )

                    # If image is valid, save it to ImageField
                    if image_file:
                        product.image.save(file_name, image_file, save=False)

                    products_to_create.append(product)
                    logging.info(f"✔ Queued product for import: {name}")

                except Exception as e:
                    logging.error(f"❌ Error processing row {idx}: {e}")

            # Bulk insert products to speed up database writes
            if products_to_create:
                Product.objects.bulk_create(products_to_create)
                logging.info(f"✅ Successfully added {len(products_to_create)} products.")
            
            logging.info(f"⚠ Skipped {skipped_products} duplicate/existing products.")

    except Exception as e:
        logging.error(f"❌ Critical Error: {e}")

# Run the script
csv_path = r"C:\Users\RUDHI PAREEK\OneDrive\Desktop\Store\sportstore\products\products.csv"
import_products_from_csv(csv_path)
