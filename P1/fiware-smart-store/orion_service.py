import os
import requests
import uuid

ORION_HOST = os.environ.get('ORION_HOST', 'localhost')
ORION_PORT = os.environ.get('ORION_PORT', '1026')
ORION_URL = f"http://{ORION_HOST}:{ORION_PORT}/v2"

class EntityWrapper:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        return None

def generate_urn(entity_type):
    return f"urn:ngsi-ld:{entity_type}:{uuid.uuid4()}"

def check_connection():
    try:
        response = requests.get(f"http://{ORION_HOST}:{ORION_PORT}/version", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

import urllib.parse

def _parse_entity(entity_json):
    parsed = {'id': entity_json.get('id'), 'type': entity_json.get('type')}
    for key, value_dict in entity_json.items():
        if key not in ['id', 'type'] and isinstance(value_dict, dict) and 'value' in value_dict:
            val = value_dict['value']
            if key == 'image' and isinstance(val, str):
                val = urllib.parse.unquote(val)
            parsed[key] = val
    return EntityWrapper(**parsed)

def get_entities(entity_type):
    try:
        response = requests.get(f"{ORION_URL}/entities?type={entity_type}&limit=1000")
        if response.status_code == 200:
            return [_parse_entity(e) for e in response.json()]
    except requests.exceptions.RequestException:
        pass
    return []

def get_entity(entity_id):
    try:
        response = requests.get(f"{ORION_URL}/entities/{entity_id}")
        if response.status_code == 200:
            return _parse_entity(response.json())
    except requests.exceptions.RequestException:
        pass
    return None

def create_entity(entity_id, entity_type, attributes):
    payload = {"id": entity_id, "type": entity_type}
    for key, value in attributes.items():
        attr_type = "Text"
        if isinstance(value, int):
            attr_type = "Integer"
        elif isinstance(value, float):
            attr_type = "Float"
        elif key in ["refStore", "refProduct"]:
            attr_type = "Relationship"
        payload[key] = {"type": attr_type, "value": value}
    try:
        response = requests.post(f"{ORION_URL}/entities", json=payload)
        return response.status_code == 201
    except requests.exceptions.RequestException:
        return False

def update_entity(entity_id, attributes):
    payload = {}
    for key, value in attributes.items():
        attr_type = "Text"
        if isinstance(value, int):
            attr_type = "Integer"
        elif isinstance(value, float):
            attr_type = "Float"
        elif key in ["refStore", "refProduct"]:
            attr_type = "Relationship"
        payload[key] = {"type": attr_type, "value": value}
    try:
        response = requests.patch(f"{ORION_URL}/entities/{entity_id}/attrs", json=payload)
        return response.status_code == 204
    except requests.exceptions.RequestException:
        return False

def delete_entity(entity_id):
    try:
        response = requests.delete(f"{ORION_URL}/entities/{entity_id}")
        return response.status_code == 204
    except requests.exceptions.RequestException:
        return False

def get_stores(): return get_entities("Store")
def get_store(store_id): return get_entity(store_id)
def create_store(name, address, image=None):
    return create_entity(generate_urn("Store"), "Store", {"name": name, "address": address, "image": image or ""})

def get_products(): return get_entities("Product")
def get_product(product_id): return get_entity(product_id)
def create_product(name, price, size=None, image=None, originCountry=None):
    return create_entity(generate_urn("Product"), "Product", {"name": name, "price": float(price), "size": size or "", "image": image or "", "originCountry": originCountry or ""})

def get_employees(): return get_entities("Employee")
def get_employee(employee_id): return get_entity(employee_id)
def create_employee(name, salary, role, refStore, image=None):
    return create_entity(generate_urn("Employee"), "Employee", {"name": name, "salary": float(salary), "role": role, "refStore": refStore, "image": image or ""})

def get_shelves(): return get_entities("Shelf")
def get_shelf(shelf_id): return get_entity(shelf_id)
def create_shelf(name, location, refStore):
    return create_entity(generate_urn("Shelf"), "Shelf", {"name": name, "location": location or "", "refStore": refStore})
def update_shelf(shelf_id, name, location):
    return update_entity(shelf_id, {"name": name, "location": location or ""})

def get_inventories(): return get_entities("InventoryItem")
def get_inventory(inventory_id): return get_entity(inventory_id)
def create_inventory(refStore, refProduct, stockCount):
    return create_entity(generate_urn("InventoryItem"), "InventoryItem", {"refStore": refStore, "refProduct": refProduct, "stockCount": int(stockCount)})
def update_inventory_stock(inventory_id, stockCount):
    return update_entity(inventory_id, {"stockCount": int(stockCount)})

def find_inventory(refStore, refProduct):
    try:
        query = f"refStore=={refStore};refProduct=={refProduct}"
        response = requests.get(f"{ORION_URL}/entities?type=InventoryItem&q={query}")
        if response.status_code == 200 and len(response.json()) > 0:
            return _parse_entity(response.json()[0])
    except requests.exceptions.RequestException:
        pass
    return None

# Composite methods to fetch relationships like SQLAlchemy does
def get_store_with_relations(store_id):
    store = get_entity(store_id)
    if not store: return None
    
    # inventories
    store.inventories = []
    all_invs = get_inventories()
    for inv in all_invs:
        if inv.refStore == store_id:
            inv.product = get_product(inv.refProduct)
            store.inventories.append(inv)
            
    # employees
    all_emps = get_employees()
    store.employees = [e for e in all_emps if e.refStore == store_id]
    
    # shelves
    all_shelves = get_shelves()
    store.shelves = [s for s in all_shelves if s.refStore == store_id]
    
    return store

def get_product_with_relations(product_id):
    product = get_entity(product_id)
    if not product: return None
    
    product.inventories = []
    all_invs = get_inventories()
    for inv in all_invs:
        if inv.refProduct == product_id:
            inv.store = get_store(inv.refStore)
            product.inventories.append(inv)
            
    return product

def get_all_inventories_with_relations():
    invs = get_inventories()
    for inv in invs:
        inv.store = get_store(inv.refStore)
        inv.product = get_product(inv.refProduct)
    return invs
