# images added manually

import os
import sys
import django
import csv
import logging

# Add project directory to Python path to ensure Django finds the app
sys.path.append(r"C:/Users/RUDHI PAREEK/Desktop/Store/sportstore")

# Ensure Django settings are configured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportstore.settings")
django.setup()

# Now import the Product model
from products.models import Product

# Logging Functionality
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def import_products_from_csv(csv_path):
    try:
        total_rows = 0
        processed_rows = 0
        
        # First, count total rows in the CSV for verification
        with open(csv_path, newline='', encoding='utf-8-sig') as file:
            total_rows = sum(1 for row in csv.reader(file)) - 1  # Subtract 1 for header
            logging.info(f"📊 Total products in CSV: {total_rows}")
        
        # Now process the rows
        with open(csv_path, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            products_to_create = []
            skipped_products = 0
            processed_products = 0
            error_products = 0
            
            # Print the header keys to verify CSV structure
            if reader.fieldnames:
                logging.info(f"🔍 CSV columns: {', '.join(reader.fieldnames)}")
            
            for idx, row in enumerate(reader, start=1):
                processed_rows += 1
                try:
                    # Check if all required keys exist
                    required_fields = ['name', 'description', 'price', 'category']
                    missing_fields = [field for field in required_fields if field not in row or not row[field]]
                    
                    if missing_fields:
                        logging.error(f"❌ Row {idx} missing required fields: {', '.join(missing_fields)}")
                        error_products += 1
                        continue
                    
                    name = row['name'].strip()
                    description = row['description'].strip()
                    
                    try:
                        price = float(row['price'])
                    except ValueError:
                        logging.error(f"❌ Row {idx} has invalid price format: '{row['price']}'")
                        error_products += 1
                        continue
                        
                    category = row['category'].strip()
                    
                    # Check if product already exists
                    if Product.objects.filter(name=name, category=category).exists():
                        logging.warning(f"⚠ Skipping existing product: {name}")
                        skipped_products += 1
                        continue
                    
                    # Create product instance (without saving)
                    product = Product(
                        name=name, 
                        description=description, 
                        price=price, 
                        category=category
                    )
                    
                    products_to_create.append(product)
                    processed_products += 1
                    logging.info(f"✔ Queued product for import: {name}")
                
                except Exception as e:
                    logging.error(f"❌ Error processing row {idx}: {str(e)}")
                    error_products += 1
            
            # Bulk insert products to speed up database writes
            if products_to_create:
                Product.objects.bulk_create(products_to_create)
                logging.info(f"✅ Successfully added {len(products_to_create)} products.")
            
            # Display summary statistics
            logging.info(f"📝 Summary:")
            logging.info(f"   - Total rows in CSV: {total_rows}")
            logging.info(f"   - Rows processed: {processed_rows}")
            logging.info(f"   - Products queued and added: {processed_products}")
            logging.info(f"   - Products skipped (duplicates): {skipped_products}")
            logging.info(f"   - Products with errors: {error_products}")
            
            # Check if all rows were processed
            if processed_rows < total_rows:
                logging.warning(f"⚠ Not all rows were processed! Expected {total_rows}, processed {processed_rows}")
            
    except Exception as e:
        logging.error(f"❌ Critical Error: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())

# Run the script
csv_path = r"C:\Users\RUDHI PAREEK\Desktop\Store\sportstore\products\products.csv"
import_products_from_csv(csv_path)
