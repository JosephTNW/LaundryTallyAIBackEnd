from app import app, db
from app.models import User, Launderer, Laundry, Clothes, association_table
from flask import jsonify, request, url_for, send_from_directory
from app.utils import generate_token, verify_token, get_root_path, allowed_file
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.dict_mapper import launderer_to_dict, clothes_to_dict
import time 
from datetime import datetime
from sqlalchemy.orm import aliased
import os
import uuid
from PIL import Image
import numpy as np
import json
import requests

# USER RELATED (AUTH)
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token})

@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    user = User(name=name, email=email, password=password)
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already in use'}), 400
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})

@app.route('/clothes/<filename>')
def serve_clothes_image(filename):
    return send_from_directory(get_root_path() + app.config['CLOTHES_FOLDER'], filename)

@app.route('/launderer/<filename>')
def serve_launderer_image(filename):
    return send_from_directory(get_root_path() + app.config['LAUNDERER_FOLDER'], filename)

@app.route('/bill/<filename>')
def serve_bill_image(filename):
    return send_from_directory(get_root_path() + app.config['BILL_FOLDER'], filename)

@app.route("/", methods=['GET'])
def home():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    home_limit = 5
    
    clothes = Clothes.query \
        .filter_by(owner=user.id) \
        .order_by(Clothes.inputted_at.desc()) \
        .limit(5) \
        .all()
        
    clothes_list = [
        {
            "id": c.id,
            "type": c.c_type,
            "color": c.color,
            "cloth_pic": url_for('serve_clothes_image', filename=c.cloth_pic) if c.cloth_pic else None,
            "inputted_at": c.inputted_at
        } for c in clothes
    ]
    
    launderers = Launderer.query \
        .order_by(Launderer.inputted_at.desc()) \
        .limit(5) \
        .all()
    
    launderer_list = [
        {
            "id": l.id,
            "name": l.name,
            "address": l.address,
            "desc": l.desc,
            "phone_num": l.phone_num,
            "launderer_pic": url_for('serve_launderer_image', filename=l.l_pic) if l.l_pic else None,
            "has_whatsapp": l.has_whatsapp,
            "has_delivery": l.has_delivery,
            "inputted_at": l.inputted_at
        } for l in launderers
    ]
    
    laundries = Laundry.query \
        .filter_by(owner=user.id).order_by(Laundry.laundered_at.desc()) \
        .limit(5) \
        .all()
       
    laundry_list = [
        {
            "id": l.id,
            "launderer": launderer_to_dict(Launderer.query.get(l.launderer)),
            "bill_pic": url_for('serve_bill_image', filename=l.bill_pic),
            "laundered_at": l.laundered_at,
            "laundry_days": l.laundry_days,
            "status": l.status,
            "clothes": [clothes_to_dict(c) for c in Clothes.query.join(association_table).filter(association_table.c.laundry_id == l.id).all()]
        } for l in laundries
    ]
    
    return jsonify({'user': user.name, 'clothes': clothes_list, 'launderers': launderer_list, 'laundries': laundry_list}), 200

# CLOTHES LOGIC
@app.route("/clothes", methods=['GET'])
def get_clothes():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    clothes = Clothes.query \
        .filter_by(owner=user.id) \
        .order_by(Clothes.inputted_at.desc()) \
        .limit(10) \
        .all()
        
    clothes_list = [
        {
            "id": c.id,
            "type": c.c_type,
            "color": c.color,
            "desc": c.desc,
            "cloth_pic": url_for("serve_clothes_image", filename=c.cloth_pic) if c.cloth_pic else None,
            "inputted_at": c.inputted_at
        } for c in clothes
    ]
            
    return jsonify(clothes_list)

@app.route("/clothes", methods=['POST'])
def create_clothes():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    clothes_items = []
    index = 0
    
    while f'cType{index}' in request.form:
        clothes_type = request.form.get(f'cType{index}')
        color = request.form.get(f'color{index}')
        desc = request.form.get(f'desc{index}')
        
        file_key = f'file{index}'
        if file_key not in request.files:
            return jsonify({'message': f'No file part in the request for item {index}'}), 400
        
        file = request.files[file_key]
        
        if file.filename == '':
            return jsonify({'message': f'No selected file for item {index}'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            new_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(app.config['CLOTHES_FOLDER'], new_filename)
            file.save(file_path)
            
            new_clothes = Clothes(
                owner=user.id,
                c_type=clothes_type,
                color=color,
                desc=desc,
                cloth_pic=new_filename,
                inputted_at=datetime.fromtimestamp(time.time())
            )
            
            clothes_items.append(new_clothes)
        else:
            return jsonify({'message': f'File type not allowed for item {index}'}), 400
        
        index += 1
    
    if not clothes_items:
        return jsonify({'message': 'No valid clothes items provided'}), 400
    
    try:
        db.session.add_all(clothes_items)
        db.session.commit()
        return jsonify({'message': 'Clothes added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@app.route("/clothes", methods=['PUT'])
def edit_clothes():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    clothes_id = request.form.get('id')
    clothes_type = request.form.get('c_type')
    color = request.form.get('color')
    desc = request.form.get('desc')

    clothes = Clothes.query.filter_by(id=clothes_id).first()

    if not clothes:
        return jsonify({'message': 'Clothes not found'}), 404
    
    clothes.c_type = clothes_type
    clothes.color = color
    clothes.desc = desc

    if 'cloth_pic' in request.files:
        file = request.files['cloth_pic']
        if file and allowed_file(file.filename):
            file_extension = os.path.splitext(file.filename)[1]
            new_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(app.config['CLOTHES_FOLDER'], new_filename)
            file.save(file_path)
            
            # Delete the old file if it exists
            if clothes.cloth_pic:
                old_file_path = os.path.join(app.config['CLOTHES_FOLDER'], clothes.cloth_pic)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            clothes.cloth_pic = new_filename
    
    db.session.commit()
    
    return jsonify({'message': 'Clothes updated successfully'}), 200

@app.route("/clothes", methods=['DELETE'])
def delete_clothes():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    clothes_id = request.args.get("id")
    
    clothes = Clothes.query.filter_by(id=clothes_id).first()
    
    if clothes.cloth_pic:
        image_path = os.path.join(app.config['CLOTHES_FOLDER'], clothes.cloth_pic)
        if os.path.exists(image_path):
            os.remove(image_path)

    if not clothes:
        return jsonify({'message': 'Clothes not found'}), 404
    
    db.session.delete(clothes)    
    db.session.commit()
    
    return jsonify({'message': 'Clothes deleted successfully'}), 200

@app.route("/launderer", methods=['POST'])
def create_launderer():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    name = request.json.get('name')
    address = request.json.get('address')
    phone_num = request.json.get('phone_num')
    has_whatsapp = request.json.get('has_whatsapp')
    has_delivery = request.json.get('has_delivery')
    l_pic = request.json.get('l_pic')
    desc = request.json.get('desc')
    
    launderer = Launderer(
        name=name,
        address=address,
        phone_num=phone_num,
        has_whatsapp=has_whatsapp,
        has_delivery=has_delivery,
        l_pic=l_pic,
        desc=desc,
        inputted_at=datetime.fromtimestamp(time.time())
    )
    
    db.session.add(launderer)
    db.session.commit()
    
    return jsonify({'message': 'Launderer created successfully', 'id': launderer.id}), 200

@app.route("/launderer", methods=['GET'])
def view_launderer():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    launderers = Launderer.query \
        .order_by(Launderer.inputted_at.desc()) \
        .limit(10) \
        .all()
    
    launderer_list = [
        {
            "id": l.id,
            "name": l.name,
            "address": l.address,
            "phone_num": l.phone_num,
            "desc": l.desc,
            "has_whatsapp": l.has_whatsapp,
            "has_delivery": l.has_delivery,
            "launderer_pic": url_for('serve_launderer_image', filename=l.l_pic) if l.l_pic else None,
            "inputted_at": l.inputted_at
        } for l in launderers
    ]
    
    return jsonify(launderer_list), 200

@app.route("/launderer", methods=['PUT'])
def edit_launderer():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    launderer_id = request.json.get('id')
    name = request.json.get('name')
    address = request.json.get('address')
    has_delivery = request.json.get('has_delivery')
    phone_num = request.json.get('phone_num')
    has_whatsapp = request.json.get('has_whatsapp')

    launderer = Launderer.query.filter_by(id=launderer_id).first()

    if not launderer:
        return jsonify({'message': 'Launderer not found'}), 404
    
    launderer.name = name
    launderer.address = address
    launderer.has_delivery = has_delivery
    launderer.phone_num = phone_num
    launderer.has_whatsapp = has_whatsapp
    
    db.session.commit()
    
    return jsonify({'message': 'Launderer updated successfully'}), 200
    
@app.route("/launderer", methods=['DELETE'])
def delete_launderer():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    launderer_id = request.json.get('id')

    launderer = Launderer.query.filter_by(id=launderer_id).first()

    if not launderer:
        return jsonify({'message': 'Launderer not found'}), 404
    
    db.session.delete(launderer)    
    db.session.commit()
    
    return jsonify({'message': 'Launderer deleted successfully'}), 200

@app.route("/launderer/search", methods=['GET'])
def search_launderer():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401

    query = request.args.get("query")
    
    launderers = Launderer.query \
        .filter(Launderer.name.ilike(f"%{query}%") |
                Launderer.address.ilike(f"%{query}%") |
                Launderer.phone_num.ilike(f"%{query}%")) \
        .order_by(Launderer.inputted_at.desc()) \
        .limit(10) \
        .all()

    launderer_list = [
        {
            "id": l.id,
            "name": l.name,
            "address": l.address,
            "phone_num": l.phone_num,
            "desc": l.desc,
            "has_whatsapp": l.has_whatsapp,
            "launderer_pic": url_for('serve_launderer_image', filename=l.l_pic) if l.l_pic else None,
            "has_delivery": l.has_delivery,
            "inputted_at": l.inputted_at
        } for l in launderers
    ]

    return jsonify(launderer_list), 200
    
@app.route("/laundry", methods=['POST'])
def create_laundry():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    clothes_ids_str = request.form.get('clothes_ids')
    launderer_id = request.form.get('launderer_id')
    laundry_days = request.form.get('laundry_days')
    
    clothes_ids = [int(clothes_id) for clothes_id in clothes_ids_str.split(',')]
    
    if 'bill_pic' in request.files:
        file = request.files['bill_pic']
        if file and allowed_file(file.filename):
            file_extension = os.path.splitext(file.filename)[1]
            new_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(app.config['BILL_FOLDER'], new_filename)
            file.save(file_path)
            
            laundry = Laundry(
                launderer=launderer_id,
                bill_pic=new_filename,
                status='pending',
                laundry_days=laundry_days,
                laundered_at=datetime.fromtimestamp(time.time()),
                owner=user.id
            )
    
    db.session.add(laundry)
    db.session.commit()

    
    for clothes_id in clothes_ids:
        association = association_table.insert().values(
            clothes_id=clothes_id, 
            laundry_id=laundry.id
            )
        db.session.execute(association)
        db.session.commit()
    
    return jsonify({'message': 'Launderer created successfully', 'id': laundry.id}), 200
    
@app.route("/laundry", methods=['GET'])
def get_laundry():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    laundries = Laundry.query \
        .join(association_table, Laundry.id == association_table.c.laundry_id) \
        .join(Clothes, association_table.c.clothes_id == Clothes.id) \
        .filter(Laundry.owner == user.id) \
        .order_by(Laundry.laundered_at.desc()) \
        .all()
    
    laundry_list = [
        {
            "id": l.id,
            "launderer": launderer_to_dict(Launderer.query.get(l.launderer)),
            "bill_pic": url_for('serve_bill_image', filename=l.bill_pic),
            "laundered_at": l.laundered_at,
            "laundry_days": l.laundry_days,
            "status": l.status,
            "clothes": [clothes_to_dict(c) for c in Clothes.query.join(association_table).filter(association_table.c.laundry_id == l.id).all()]
        } for l in laundries
    ]
    
    return jsonify(laundry_list), 200    

@app.route("/validate", methods=['PUT'])
def validate_laundry():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    laundry_id = request.json.get('laundry_id')
    clothes_ids = request.json.get('clothes_ids')
    
    print(f"received laundry id: {laundry_id}")
    print(f"received clothes ids: {clothes_ids}")

    if (len(clothes_ids) == 0):
        return jsonify({'message': 'Invalid Clothes'}), 400
    
    laundry_clothes = db.session.query(association_table).filter_by(laundry_id=laundry_id).all()
    
    if (len(laundry_clothes) == 0):
        return jsonify({'message': 'Invalid Laundry'}), 400
    
    # status = "finish" if laundry_count == len(clothes_ids) else "missing"
    
    laundered_clothes = association_table.update().where(
        (association_table.c.laundry_id == laundry_id)
    ).values(
        returned=association_table.c.clothes_id.in_(clothes_ids)
    )
    db.session.execute(laundered_clothes)
    db.session.commit()
    
    revalidate_clothes = db.session.query(association_table).filter_by(laundry_id=laundry_id).all()
        
    all_returned = all(revalidate.returned for revalidate in revalidate_clothes)
    if all_returned:
        status = "finish"
    else:
        status = "missing"
        
    laundry = Laundry.query.filter_by(id=laundry_id).first()
    laundry.status = status
    db.session.commit()
    
    return jsonify({"message": f"laundry updated to status {status}"}), 200    

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

@app.route("/type", methods=['POST'])
def type_detect():
    token = request.headers.get('Authorization')
    
    user = verify_token(token)
    
    if isinstance(user, str):
        return jsonify({'message': user}), 401
    
    if 'cloth_pics' not in request.files:
        return jsonify({'message': 'No files part in the request'}), 400
    
    files = request.files.getlist('cloth_pics')
    if not files:
        return jsonify({'message': 'No selected files'}), 400
    
    try:
        images = []
        for file in files:
            # Open the image file
            image = Image.open(fp = file).convert('L')  # Convert image to grayscale
            image = image.resize((28, 28))  # Resize image to 28x28
            
            # Convert the image to a numpy array and normalize it
            image_array = (255.0 - np.array(image)) / 255.0
            images.append(image_array)
        
        # Convert the list of image arrays to a numpy array
        images = np.stack(images)
        
        # Prepare the data for the model
        json_data = json.dumps({"instances": images.tolist()})
        
        # Define the endpoint
        endpoint = "http://localhost:8080/v1/models/fashion-mnist:predict"
        
        # Send the request to the model
        response = requests.post(endpoint, data=json_data)
        predictions = response.json()["predictions"]
        
        # Get the class names for the predictions
        predicted_classes = [class_names[np.argmax(pred)] for pred in predictions]
        return jsonify({"data": predicted_classes}), 200
    
    except Exception as e:
        return jsonify({'message': f"error try catch:{str(e)}"}), 500
    
    
    