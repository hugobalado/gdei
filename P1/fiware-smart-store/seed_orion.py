#!/usr/bin/env python3
import os
import requests
import uuid
import time
import sys

ORION_HOST = os.environ.get('ORION_HOST', 'localhost')
ORION_PORT = os.environ.get('ORION_PORT', '1026')
ORION_URL = f"http://{ORION_HOST}:{ORION_PORT}/v2"

def generate_urn(entity_type):
    return f"urn:ngsi-ld:{entity_type}:{uuid.uuid4()}"

def check_connection():
    try:
        response = requests.get(f"{ORION_URL.replace('/v2', '')}/version", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def create_entity(entity_id, entity_type, attributes):
    payload = {
        "id": entity_id,
        "type": entity_type
    }
    
    for key, value in attributes.items():
        attr_type = "Text"
        if isinstance(value, int):
            attr_type = "Integer"
        elif isinstance(value, float):
            attr_type = "Float"
        elif key in ["refStore", "refProduct"]:
            attr_type = "Relationship"
            
        if key == "image" and value:
            import urllib.parse
            value = urllib.parse.quote(value, safe=":/")
            
        payload[key] = {"type": attr_type, "value": value}
        
    try:
        response = requests.post(f"{ORION_URL}/entities", json=payload)
        if response.status_code != 201:
            print(f"Error creating {entity_id}: {response.text}")
            return False
        return True
    except requests.exceptions.RequestException as e:
        print(f"Exception creating {entity_id}: {e}")
        return False

def main():
    print(f"[*] Checking connection to Orion Context Broker at {ORION_URL}...")
    if not check_connection():
        print("[!] ERROR: Cannot connect to Orion Context Broker. Is it running?")
        sys.exit(1)
        
    print("[*] Connected! Seeding data...")

    # ==========================
    # 1. STORES
    # ==========================
    store_data = [
        {"name": "Supermercado Centro", "address": "Calle Mayor, 1", "image": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80"},
        {"name": "Supermercado Norte", "address": "Av. de la Libertad, 45", "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=800&q=80"},
        {"name": "Supermercado Sur", "address": "Plaza del Sol, 12", "image": "https://images.unsplash.com/photo-1534723452862-4c874018d66d?auto=format&fit=crop&w=800&q=80"},
        {"name": "Supermercado Este", "address": "Calle del Mar, 8", "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?auto=format&fit=crop&w=800&q=80"}
    ]
    
    stores = []
    for data in store_data:
        store_id = generate_urn("Store")
        stores.append(store_id)
        if create_entity(store_id, "Store", data):
            print(f" [+] Created Store: {data['name']} ({store_id})")
        else:
            print(f" [-] Failed to create Store: {data['name']}")

    # ==========================
    # 2. PRODUCTS
    # ==========================
    product_data = [
        {"name": "Leche Entera", "size": "1 Litro", "price": 0.90, "originCountry": "España", "image": "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=800&q=80"},
        {"name": "Pan de Molde", "size": "Integrales", "price": 1.50, "originCountry": "Francia", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80"},
        {"name": "Huevos", "size": "Docena", "price": 2.20, "originCountry": "España", "image": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?auto=format&fit=crop&w=800&q=80"},
        {"name": "Aceite de Oliva", "size": "1 Litro, Virgen Extra", "price": 8.50, "originCountry": "Italia", "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=800&q=80"},
        {"name": "Arroz", "size": "1 Kg", "price": 1.10, "originCountry": "España", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80"},
        {"name": "Pasta", "size": "Macarrones, 500g", "price": 0.85, "originCountry": "Italia", "image": "https://images.unsplash.com/photo-1551462147-ff29053bfc14?auto=format&fit=crop&w=800&q=80"},
        {"name": "Manzanas", "size": "1 Kg", "price": 1.99, "originCountry": "España", "image": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?auto=format&fit=crop&w=800&q=80"},
        {"name": "Pollo", "size": "Pechuga, 1 Kg", "price": 6.50, "originCountry": "Brasil", "image": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=800&q=80"},
        {"name": "Café", "size": "Natural, 250g", "price": 2.80, "originCountry": "Colombia", "image": "https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=800&q=80"},
        {"name": "Azúcar", "size": "Blanco, 1 Kg", "price": 1.00, "originCountry": "Brasil", "image": "https://images.unsplash.com/photo-1709651808265-977ed7ef78c6?w=400"}
    ]
    
    products = []
    for data in product_data:
        product_id = generate_urn("Product")
        products.append(product_id)
        if create_entity(product_id, "Product", data):
            print(f" [+] Created Product: {data['name']} ({product_id})")
        else:
            print(f" [-] Failed to create Product: {data['name']}")

    # ==========================
    # 3. INVENTORY ITEMS (Stock)
    # ==========================
    inventory_data = [
        {"refStore": stores[0], "refProduct": products[0], "stockCount": 50},
        {"refStore": stores[0], "refProduct": products[1], " stockCount": 30},
        {"refStore": stores[1], "refProduct": products[2], "stockCount": 40},
        {"refStore": stores[1], "refProduct": products[3], "stockCount": 15},
        {"refStore": stores[2], "refProduct": products[4], "stockCount": 60},
        {"refStore": stores[2], "refProduct": products[5], "stockCount": 45},
        {"refStore": stores[3], "refProduct": products[6], "stockCount": 25},
        {"refStore": stores[3], "refProduct": products[7], "stockCount": 20},
        {"refStore": stores[0], "refProduct": products[8], "stockCount": 100},
        {"refStore": stores[2], "refProduct": products[9], "stockCount": 80}
    ]
    
    for data in inventory_data:
        # Quick fix for dict typo in dict initialization
        if " stockCount" in data:
            data["stockCount"] = data.pop(" stockCount")
            
        inv_id = generate_urn("InventoryItem")
        if create_entity(inv_id, "InventoryItem", data):
            print(f" [+] Created InventoryItem ({inv_id}) in Store {data['refStore']} for Product {data['refProduct']}")
        else:
            print(f" [-] Failed to create InventoryItem.")

    # ==========================
    # 4. EMPLOYEES
    # ==========================
    employee_data = [
        {"name": "Juan Pérez", "role": "Cajero", "salary": 1200.0, "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400", "refStore": stores[0]},
        {"name": "María Gómez", "role": "Reponedor", "salary": 1150.0, "image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400", "refStore": stores[0]},
        {"name": "Carlos López", "role": "Gerente", "salary": 1800.0, "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400", "refStore": stores[0]},
        
        {"name": "Ana Martínez", "role": "Cajero", "salary": 1200.0, "image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400", "refStore": stores[1]},
        {"name": "Pedro Sánchez", "role": "Reponedor", "salary": 1150.0, "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400", "refStore": stores[1]},
        
        {"name": "Lucía Fernández", "role": "Gerente", "salary": 1800.0, "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400", "refStore": stores[2]},
        {"name": "Miguel Torres", "role": "Cajero", "salary": 1200.0, "image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400", "refStore": stores[2]},
        
        {"name": "Sofía Ruiz", "role": "Reponedor", "salary": 1150.0, "image": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400", "refStore": stores[3]},
        {"name": "David Jiménez", "role": "Cajero", "salary": 1200.0, "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400", "refStore": stores[3]},
        {"name": "Elena Navarro", "role": "Reponedor", "salary": 1150.0, "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400", "refStore": stores[3]},
    ]
    
    for data in employee_data:
        emp_id = generate_urn("Employee")
        if create_entity(emp_id, "Employee", data):
            print(f" [+] Created Employee: {data['name']} ({emp_id})")
        else:
            print(f" [-] Failed to create Employee: {data['name']}")

    # ==========================
    # 5. SHELVES
    # ==========================
    # Adding a couple of conceptual shelves per store
    shelf_data = [
        {"name": "Lácteos A1", "location": "Pasillo 1, Derecha", "refStore": stores[0]},
        {"name": "Panadería Frontal", "location": "Entrada principal", "refStore": stores[0]},
        {"name": "Carnicería Trasera", "location": "Fondo del local", "refStore": stores[1]},
        {"name": "Frutería Isla", "location": "Centro de la tienda", "refStore": stores[2]},
        {"name": "Góndola Central", "location": "Pasillo 3, Izquierda", "refStore": stores[3]}
    ]

    for data in shelf_data:
        shelf_id = generate_urn("Shelf")
        if create_entity(shelf_id, "Shelf", data):
            print(f" [+] Created Shelf: {data['name']} ({shelf_id})")
        else:
            print(f" [-] Failed to create Shelf: {data['name']}")

    print("\n[*] Initialization completed! Test data has been injected into Orion.")

if __name__ == "__main__":
    main()
