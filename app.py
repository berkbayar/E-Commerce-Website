from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xcdb-.919adur@localhost/my_ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json.get('description', '')
    category = request.json.get('category', '')
    price = request.json['price']
    image_url = request.json['image_url']

    new_product = Product(name=name, description=description, category=category, price=price , image_url=image_url)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully!'}), 201

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {'id': product.id, 'name': product.name, 'description': product.description, 'category': product.category, 'price': product.price, 'image_url':product.image_url}
        output.append(product_data)

    return jsonify({'products': output})

@app.route('/api/products/<category_name>')
def products_by_category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    product_list = [{'name': product.name, 'id' : product.id , 'price': product.price, 'image_url': product.image_url} for product in products]
    return jsonify(product_list)


@app.route('/api/categories')
def get_categories():
    unique_categories = db.session.query(Product.category).distinct().all()
    category_list = [category[0] for category in unique_categories] 
    return jsonify(category_list)

@app.route('/api/search')
def search():
    query = request.args.get('query', '')
    sort_order = request.args.get('sort', 'asc')

    if sort_order == 'asc':
        order = Product.price.asc()
    else:
        order = Product.price.desc()

    search_results = Product.query.filter(Product.name.ilike(f'%{query}%')).order_by(order)
    products = [{'id': product.id, 'name': product.name, 'description': product.description,
                 'category': product.category, 'price': product.price, 'image_url': product.image_url}
                for product in search_results]

    
    category_counts = db.session.query(Product.category, db.func.count(Product.category).label('count')) \
        .group_by(Product.category).all()

    category_counts_list = [{'category': category, 'count': count} for category, count in category_counts]

    return jsonify({'products': products, 'categories': category_counts_list})





@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    product.name = request.json.get('name', product.name)
    product.description = request.json.get('description', product.description)
    product.category = request.json.get('category', product.category)
    product.price = request.json.get('price', product.price)
    product.image_url = request.json.get('image_url', product.image_url)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully!'})


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully!'})


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))  

    def __repr__(self):
        return f'<Product {self.name}>'


@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    