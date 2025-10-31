from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(MONGO_URI)
db = client['crud_db']
collection = db['items']


# CREATE - Add a new item
@app.route('/api/items', methods=['POST'])
def create_item():
    try:
        data = request.json
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Name and price are required'}), 400

        item = {
            'name': data['name'],
            'price': data['price'],
            'quantity': data.get('quantity', 0),
            'category': data.get('category', ''),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = collection.insert_one(item)
        return jsonify({
            'id': str(result.inserted_id),
            'message': 'Item created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ - Get all items
@app.route('/api/items', methods=['GET'])
def get_all_items():
    try:
        items = []
        for item in collection.find():
            item['_id'] = str(item['_id'])
            items.append(item)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ - Get a single item by ID
@app.route('/api/items/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = collection.find_one({'_id': ObjectId(item_id)})
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        item['_id'] = str(item['_id'])
        return jsonify(item), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# UPDATE - Update an item
@app.route('/api/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.json
        update_data = {}

        if 'name' in data:
            update_data['name'] = data['name']
        if 'price' in data:
            update_data['price'] = data['price']
        if 'quantity' in data:
            update_data['quantity'] = data['quantity']
        if 'category' in data:
            update_data['category'] = data['category']

        update_data['updated_at'] = datetime.utcnow()

        result = collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_data}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Item not found'}), 404

        return jsonify({'message': 'Item updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE - Delete an item
@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        result = collection.delete_one({'_id': ObjectId(item_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)