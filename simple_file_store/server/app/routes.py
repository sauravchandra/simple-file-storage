from flask import Blueprint, request, jsonify
import os
from collections import Counter

from ...utils.common import calculate_file_hash

api = Blueprint('api', __name__, url_prefix='/api')

file_storage_path = '/tmp/store_location'

if not os.path.exists(file_storage_path):
    os.makedirs(file_storage_path)


def get_storage_file_path(file_name):
    return os.path.join(file_storage_path, file_name)


@api.route('/check', methods=['GET'])
def check_file():
    try:
        file_hash = request.args.get('hash')

        for file_name in os.listdir(file_storage_path):
            file_path = get_storage_file_path(file_name)

            if os.path.isfile(file_path) and not os.path.islink(file_path):
                file_content_hash = calculate_file_hash(file_path)
                if file_content_hash == file_hash:
                    return jsonify({'data': {file_hash: file_name}}), 200

        return jsonify({'message': f'File with hash {file_hash} not found.'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@api.route('/add', methods=['POST'])
def add_file():
    try:
        if request.files:
            file_name = request.files['file'].filename
            file_path = get_storage_file_path(file_name)
            request.files['file'].save(file_path)
            return jsonify({'message': f'File {file_name} added successfully.'}), 200

        elif request.json:
            existing_file = request.json.get('existing_file')
            uploaded_file = request.json.get('uploaded_file')

            reference_path = get_storage_file_path(uploaded_file)

            if not os.path.exists(reference_path):
                os.link(get_storage_file_path(existing_file), reference_path)
            return jsonify({'message': f'File {uploaded_file} added successfully.'}), 200

        else:
            return jsonify({'message': 'File data missing from request.'}), 400

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@api.route('/list', methods=['GET'])
def list_files():
    try:
        files = [f for f in os.listdir(file_storage_path) if os.path.isfile(
            os.path.join(file_storage_path, f))]
        return jsonify({'data': files}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@api.route('/remove', methods=['DELETE'])
def remove_file():
    try:
        file_name = request.args.get('file')
        file_path = get_storage_file_path(file_name)

        if os.path.exists(file_path):
            if os.path.islink(file_path):
                os.unlink(file_path)
            else:
                os.remove(file_path)
            return jsonify({'message': f'File {file_name} removed successfully.'}), 200
        return jsonify({'message': f'File {file_name} not found.'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@api.route('/update', methods=['PUT'])
def update_file():
    try:
        if request.files:
            file_name = request.files['file'].filename
            file_path = get_storage_file_path(file_name)
            request.files['file'].save(file_path)
            return jsonify({'message': f'File {file_name} updated successfully.'}), 200
        
        elif request.json:
            existing_file = request.json.get('existing_file')
            uploaded_file = request.json.get('uploaded_file')

            reference_path = get_storage_file_path(uploaded_file)

            if not os.path.exists(reference_path):
                os.link(get_storage_file_path(existing_file), reference_path)
            return jsonify({'message': f'File {uploaded_file} updated successfully.'}), 200

        else:
            return jsonify({'message': 'File data missing from request.'}), 400
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@api.route('/wordcount', methods=['GET'])
def word_count():
    try:
        total_words = sum(len(open(get_storage_file_path(file_name)).read(
        ).split()) for file_name in os.listdir(file_storage_path))
        return jsonify({'data': {'word_count': total_words}}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@api.route('/freq-words', methods=['GET'])
def frequent_words():
    try:
        limit = int(request.args.get('limit', 10))
        order = request.args.get('order', 'dsc')

        words = []
        for file_name in os.listdir(file_storage_path):
            with open(get_storage_file_path(file_name), 'r') as file:
                words.extend(file.read().split())

        word_counts = Counter(words)
        sorted_words = sorted(word_counts.items(),
                              key=lambda x: x[1], reverse=(order == 'dsc'))

        return jsonify({'data': {'words': sorted_words[:limit], 'limit': limit, 'frequency_type': order}}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
