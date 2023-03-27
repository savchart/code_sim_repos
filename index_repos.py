import os
import time
import sys
import json
import tempfile
from collections import defaultdict
from github import Github
from pygments import lex
from pygments.lexers import get_lexer_for_filename
from typing import List, Tuple, Union
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def download_repository(repo_name_):
    access_token = os.getenv("GITHUB_TOKEN")
    if not access_token:
        print("Please set GITHUB_TOKEN in your environment")
        sys.exit(1)

    github = Github(access_token)
    repo = github.get_repo(repo_name_)
    contents = repo.get_contents("")

    temp_dir = tempfile.mkdtemp()
    download_contents(contents, temp_dir, repo)

    return temp_dir


def download_contents(contents, temp_dir_, repo):
    for content in contents:
        if content.type == "dir":
            new_contents = repo.get_contents(content.path)
            new_temp_dir = os.path.join(temp_dir_, content.name)
            try:
                os.makedirs(new_temp_dir)
            except FileExistsError:
                print(f"Directory {new_temp_dir} already exists. Skipping...")
            print(f"Creating directory {new_temp_dir}...")
            download_contents(new_contents, new_temp_dir, repo)
        else:
            download_file(content, temp_dir_)


def download_file(content, temp_dir_):
    time.sleep(1)
    file_path = os.path.join(temp_dir_, content.name)
    try:
        with open(file_path, "wb") as f:
            print(f"Downloading {file_path}...")
            f.write(content.decoded_content)
    except Exception as e:
        print(f"Error downloading {file_path}: {e}")


def index_repository(temp_dir_):
    inverted_index = defaultdict(set)
    for root, _, files in os.walk(temp_dir_):
        for file in files:
            file_path = os.path.join(root, file)
            index_file(file_path, inverted_index)

    return inverted_index


def index_file(file_path, inverted_index_):
    try:
        lexer = get_lexer_for_filename(file_path)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            tokens = lex(content, lexer)

        for token_type, token_value in tokens:
            if token_type.name.startswith("Token.Name"):
                inverted_index_[token_value].add(file_path)
    except Exception as e:
        pass


def save_inverted_index(inverted_index_, output_path_):
    with open(output_path_, "w") as f:
        json.dump({k: list(v) for k, v in inverted_index_.items()}, f)


def extract_token_names(file_path: str) -> List[str]:
    try:
        lexer = get_lexer_for_filename(file_path)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            tokens = lex(content, lexer)

        token_names = []
        for token_type, token_value in tokens:
            if str(token_type).startswith("Token.Name"):
                token_names.append(token_value)
        return token_names
    except Exception as e:
        print(f"Error extracting token names from {file_path}: {e}")
        return []


def check_similarity(file_path: str, inverted_index_: dict, similarity_threshold: float = 0.85) -> Union[str, None]:
    token_names = extract_token_names(file_path)
    token_names_set = set(token_names)
    token_count = len(token_names_set)

    max_similarity = 0
    max_similarity_file = None

    for token_name in token_names_set:
        for indexed_file in inverted_index_.get(token_name, []):
            indexed_tokens = set(extract_token_names(indexed_file))
            intersection_count = len(token_names_set.intersection(indexed_tokens))
            similarity = intersection_count / token_count

            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_file = indexed_file

            if max_similarity >= similarity_threshold:
                return max_similarity_file

    return None


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage:")
        print("  Indexing: python index_repos.py index repo_name output_path")
        print("  Checking: python index_repos.py check input_file_path output_path")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "index":
        repo_name = sys.argv[2]
        output_path = sys.argv[3]

        temp_dir = download_repository(repo_name)
        inverted_index = index_repository(temp_dir)
        save_inverted_index(inverted_index, output_path)

    elif operation == "check":
        input_file_path = sys.argv[2]
        output_path = sys.argv[3]

        with open(output_path, "r") as f:
            inverted_index = json.load(f)

        similar_file = check_similarity(input_file_path, inverted_index)

        if similar_file:
            print(f"Similar file found: {similar_file}")
        else:
            print("OK")

    else:
        print("Invalid operation. Use 'index' or 'check'.")
        sys.exit(1)
