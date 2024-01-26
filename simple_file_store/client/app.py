#!/usr/bin/env python3

import argparse
import requests
import os

from ..utils.common import calculate_file_hash

API_BASE_URL = 'http://localhost:8080/api'


def add_files(files):
    for file_name in files:
        file_path = os.path.abspath(file_name)
        file_hash = calculate_file_hash(file_path)

        file_check_response = requests.get(
            f'{API_BASE_URL}/check?hash={file_hash}').json()

        if file_check_response.get('data'):
            if file_check_response.get('data').get(file_hash) == file_name:
                print(f"Error: File {file_name} already exists.")
                continue

            reference_name = file_check_response.get('data').get(file_hash)
            reference_data = {'existing_file': reference_name,
                              'uploaded_file': file_name}
            response = requests.post(
                f'{API_BASE_URL}/add', json=reference_data)

        else:
            with open(file_path, 'r') as file_content:
                file_data = {'file': file_content}
                response = requests.post(
                    f'{API_BASE_URL}/add', files=file_data)

        if response.status_code == 200:
            print(response.json().get('message'))
        else:
            print(
                f"Error: {response.status_code} - {response.json().get('message')}")


def list_files():
    response = requests.get(f'{API_BASE_URL}/list')

    if response.status_code == 200:
        files = response.json().get('data')
        if files:
            print("\n".join(files))
        else:
            print("No files available.")
    else:
        print(response)
        print(
            f"Error: {response.status_code} - {response.json().get('message')}")


def remove_files(files):
    for file in files:
        response = requests.delete(f'{API_BASE_URL}/remove?file={file}')
        print(response.json().get('message'))


def update_file(file_name):
    file_path = os.path.abspath(file_name)
    file_hash = calculate_file_hash(file_path)

    file_check_response = requests.get(
        f'{API_BASE_URL}/check?hash={file_hash}').json()

    if file_check_response.get('data'):
        if file_check_response.get('data').get(file_hash) == file_name:
            print(f'File {file_name} updated successfully.')
            return
        else:
            reference_name = file_check_response.get('data').get(file_hash)
            reference_data = {'existing_file': reference_name,
                              'uploaded_file': file_name}
            response = requests.put(
                f'{API_BASE_URL}/update', json=reference_data)
    else:
        with open(file_path, 'rb') as file_content:
            file_data = {'file': file_content}
            response = requests.put(
                f'{API_BASE_URL}/update', files=file_data)

    if response.status_code == 200:
        print(response.json().get('message'))
    else:
        print(
            f"Error: {response.status_code} - {response.json().get('message')}")


def word_count():
    response = requests.get(f'{API_BASE_URL}/wordcount')

    if response.status_code == 200:
        word_count_data = response.json().get('data')
        print(f"Total word count is {word_count_data.get('word_count')}")
    else:
        print(
            f"Error: {response.status_code} - {response.json().get('message')}")


def frequent_words(limit=10, order='asc'):
    response = requests.get(
        f'{API_BASE_URL}/freq-words?limit={limit}&order={order}')

    if response.status_code == 200:
        frequent_words_data = response.json().get('data')
        words = frequent_words_data.get('words')
        frequency_type = frequent_words_data.get('frequency_type')

        print(
            f"Top {limit} {'most' if frequency_type == 'dsc' else 'least'} frequent words are:")
        for word, frequency in words:
            print(f"{word}: {frequency}")
    else:
        print(
            f"Error: {response.status_code} - {response.json().get('message')}")


def main():
    parser = argparse.ArgumentParser(description='File Store Client')
    subparsers = parser.add_subparsers(
        dest='operation', help='Operation to perform')

    add_parser = subparsers.add_parser('add', help='Add files')
    add_parser.add_argument(
        'files', nargs='+', help='Paths of the files to be added')

    subparsers.add_parser('ls', help='List files')

    remove_parser = subparsers.add_parser('rm', help='Remove files')
    remove_parser.add_argument(
        'files', nargs='+', help='Paths of the files to be removed')

    update_parser = subparsers.add_parser('update', help='Update file')
    update_parser.add_argument(
        'file', help='Name of the file to be updated')

    subparsers.add_parser('wc', help='Get word count')

    freq_words_parser = subparsers.add_parser(
        'freq-words', help='Get frequent words')
    freq_words_parser.add_argument(
        '--limit', '-n', type=int, default=10, help='Limit for frequent words operation')
    freq_words_parser.add_argument(
        '--order', choices=['asc', 'dsc'], default='dsc', help='Order for frequent words operation')

    args = parser.parse_args()

    if args.operation is None:
        parser.print_help()
    else:
        if args.operation == 'add':
            add_files(args.files)
        elif args.operation == 'ls':
            list_files()
        elif args.operation == 'rm':
            remove_files(args.files)
        elif args.operation == 'update':
            update_file(args.file)
        elif args.operation == 'wc':
            word_count()
        elif args.operation == 'freq-words':
            frequent_words(args.limit, args.order)


if __name__ == '__main__':
    main()
