# Dasman Website - Location-Based Product Filtering

## Overview
This module extends Odoo's website shop functionality to filter products based on geographic location (Governorate/City and Area). Products are filtered based on their availability in warehouses linked to specific locations.

## Features

### 1. Location Management
- **Governorate (City)**: High-level geographic divisions
- **Area**: Subdivisions within governorates
- **Warehouse Integration**: Warehouses are linked to governorates

### 2. Product Filtering
- Products are filtered based on stock availability in warehouses
- Only products with stock > 0 in the selected location are shown
- Dynamic filtering based on governorate selection

### 3. User Interface
- Location selection popup on home page
- Shop page with location filter dropdowns
- Dynamic area filtering based on selected city

## Setup Instructions

### 1. Install Dependencies
Make sure the following modules are installed:
- `website_sale` (for shop functionality)
- `stock` (for warehouse management)

### 2. Configure Warehouses
1. Go to **Inventory > Configuration > Warehouses**
2. For each warehouse, set the **Governorate** field
3. Ensure products have stock in the appropriate warehouses

### 3. Configure Products
1. Make sure products are published and saleable
2. Add stock to products in the appropriate warehouse locations
3. Products will automatically appear in the shop based on location

## Usage

### For Customers
1. **Home Page**: Select city and area from the popup
2. **Shop Page**: Use the location filters to browse products
3. **Product Availability**: Only products available in selected location are shown

### For Administrators
1. **Manage Governorates**: Go to **Inventory > Configuration > Governments**
2. **Manage Areas**: Go to **Inventory > Configuration > Areas**
3. **Link Warehouses**: Set governorate for each warehouse

## Technical Details

### Data Models
- `gov`: Governorate/City model
- `area`: Area model (linked to governorate)
- `stock.warehouse`: Extended with governorate field

### Key Methods
- `WebsiteSale.get_location_filtered_products()`: Filters products by location
- `ProductTemplate.get_available_locations()`: Gets locations where product is available
- `ProductTemplate.get_warehouses_with_stock()`: Gets warehouses with product stock

### Routes
- `/`: Home page with location selection
- `/shop`: Shop page with location filtering

## Troubleshooting

### Products Not Showing
1. Check if products are published and saleable
2. Verify stock exists in warehouse locations
3. Ensure warehouse is linked to correct governorate

### Location Filter Not Working
1. Check if `website_sale` module is installed
2. Verify governorate and area data exists
3. Check browser console for JavaScript errors

## Sample Data
The module includes sample data for testing:
- Governorates: Cairo, Alexandria, Giza
- Areas: Maadi, Heliopolis, Montazah, Agami, 6th October, Sheikh Zayed

## Customization
- Modify `shop_template.xml` to change the filter UI
- Update `website_sale.py` to modify filtering logic
- Extend `main.py` controller for additional functionality 