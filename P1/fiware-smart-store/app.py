import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_babel import Babel, _
from models import db, Store, Product, InventoryItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es']

def get_locale():
    # Attempt to retrieve language from session
    return session.get('lang', app.config['BABEL_DEFAULT_LOCALE'])

babel = Babel(app, locale_selector=get_locale)

db.init_app(app)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


def seed_data():
    if Store.query.first() is None:
        # Create 4 stores
        stores = [
            Store(name="Supermercado Centro", address="Calle Mayor, 1", image="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80"),
            Store(name="Supermercado Norte", address="Av. de la Libertad, 45", image="https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=800&q=80"),
            Store(name="Supermercado Sur", address="Plaza del Sol, 12", image="https://images.unsplash.com/photo-1534723452862-4c874018d66d?auto=format&fit=crop&w=800&q=80"),
            Store(name="Supermercado Este", address="Calle del Mar, 8", image="https://images.unsplash.com/photo-1604719312566-8912e9227c6a?auto=format&fit=crop&w=800&q=80")
        ]
        db.session.add_all(stores)
        db.session.commit()

        # Create 10 products
        products = [
            Product(name="Leche Entera", size="1 Litro", price=0.90, originCountry="España", image="https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=800&q=80"),
            Product(name="Pan de Molde", size="Integrales", price=1.50, originCountry="Francia", image="https://images.unsplash.com/photo-1595185593881-306cd11bbd77?auto=format&fit=crop&w=800&q=80"),
            Product(name="Huevos", size="Docena", price=2.20, originCountry="España", image="https://images.unsplash.com/photo-1506976785307-8732e854ad03?auto=format&fit=crop&w=800&q=80"),
            Product(name="Aceite de Oliva", size="1 Litro, Virgen Extra", price=8.50, originCountry="Italia", image="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=800&q=80"),
            Product(name="Arroz", size="1 Kg", price=1.10, originCountry="España", image="https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80"),
            Product(name="Pasta", size="Macarrones, 500g", price=0.85, originCountry="Italia", image="https://images.unsplash.com/photo-1551462147-ff29053bfc14?auto=format&fit=crop&w=800&q=80"),
            Product(name="Manzanas", size="1 Kg", price=1.99, originCountry="España", image="https://images.unsplash.com/photo-1560806887-1e4cd0b6faa6?auto=format&fit=crop&w=800&q=80"),
            Product(name="Pollo", size="Pechuga, 1 Kg", price=6.50, originCountry="Brasil", image="https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=800&q=80"),
            Product(name="Café", size="Natural, 250g", price=2.80, originCountry="Colombia", image="https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=800&q=80"),
            Product(name="Azúcar", size="Blanco, 1 Kg", price=1.00, originCountry="Brasil", image="https://images.unsplash.com/photo-1581441363689-1f3c3c414635?auto=format&fit=crop&w=800&q=80")
        ]
        db.session.add_all(products)
        db.session.commit()

        # Create inventory (min 2 per store)
        inventories = [
            InventoryItem(refStore=stores[0].id, refProduct=products[0].id, stockCount=50),
            InventoryItem(refStore=stores[0].id, refProduct=products[1].id, stockCount=30),
            InventoryItem(refStore=stores[1].id, refProduct=products[2].id, stockCount=40),
            InventoryItem(refStore=stores[1].id, refProduct=products[3].id, stockCount=15),
            InventoryItem(refStore=stores[2].id, refProduct=products[4].id, stockCount=60),
            InventoryItem(refStore=stores[2].id, refProduct=products[5].id, stockCount=45),
            InventoryItem(refStore=stores[3].id, refProduct=products[6].id, stockCount=25),
            InventoryItem(refStore=stores[3].id, refProduct=products[7].id, stockCount=20),
            # Add a couple more randomly to ensure more variety
            InventoryItem(refStore=stores[0].id, refProduct=products[8].id, stockCount=100),
            InventoryItem(refStore=stores[2].id, refProduct=products[9].id, stockCount=80)
        ]
        db.session.add_all(inventories)
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

@app.route('/')
def index():
    stores_count = Store.query.count()
    products_count = Product.query.count()
    total_stock = db.session.query(db.func.sum(InventoryItem.stockCount)).scalar() or 0
    return render_template('index.html', stores_count=stores_count, products_count=products_count, total_stock=total_stock)

@app.route('/stores')
def view_stores():
    stores = Store.query.all()
    return render_template('stores.html', stores=stores)

@app.route('/store/<id>')
def store_detail(id):
    store = Store.query.get_or_404(id)
    return render_template('store_detail.html', store=store)

@app.route('/store/new', methods=['GET', 'POST'])
def store_create():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        image = request.form.get('image')
        if name and address:
            new_store = Store(name=name, address=address, image=image)
            db.session.add(new_store)
            db.session.commit()
            return redirect(url_for('view_stores'))
    return render_template('store_form.html')

@app.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/<id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/product/new', methods=['GET', 'POST'])
def product_create():
    if request.method == 'POST':
        name = request.form.get('name')
        size = request.form.get('size')
        price_str = request.form.get('price')
        image = request.form.get('image')
        originCountry = request.form.get('originCountry')
        if name and price_str:
            try:
                price = float(price_str)
                new_product = Product(name=name, size=size, price=price, image=image, originCountry=originCountry)
                db.session.add(new_product)
                db.session.commit()
            except ValueError:
                pass
            return redirect(url_for('view_products'))
    return render_template('product_form.html')

@app.route('/inventory', methods=['GET', 'POST'])
def view_inventory():
    if request.method == 'POST':
        refStore = request.form.get('refStore')
        refProduct = request.form.get('refProduct')
        stockCount_str = request.form.get('stockCount')
        
        if refStore and refProduct and stockCount_str:
            try:
                stockCount = int(stockCount_str)
                # Check if already exists
                inv = InventoryItem.query.filter_by(refStore=refStore, refProduct=refProduct).first()
                if inv:
                    inv.stockCount += stockCount
                else:
                    new_inv = InventoryItem(refStore=refStore, refProduct=refProduct, stockCount=stockCount)
                    db.session.add(new_inv)
                db.session.commit()
            except ValueError:
                pass
            return redirect(url_for('view_inventory'))
        
    inventories = InventoryItem.query.join(Store).join(Product).all()
    stores = Store.query.all()
    products = Product.query.all()
    return render_template('inventory.html', inventories=inventories, stores=stores, products=products)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
