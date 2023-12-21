import os
import json
import frontmatter
from datetime import datetime

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def extract_blog_data(markdown_path):
    with open(markdown_path, 'r', encoding='utf-8') as file:
        content = frontmatter.load(file)

    # Extract front matter keys and values
    front_matter = {key: content[key] for key in content.keys() if key != 'content'}

    return {
        'front_matter': front_matter,
        'content': content.content
    }

def extract_all_blogs(directory, output_directory):
    all_blogs = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                subdirectory_name = os.path.basename(root)
                markdown_path = os.path.join(root, filename)
                blog_data = extract_blog_data(markdown_path)

                if subdirectory_name not in all_blogs:
                    all_blogs[subdirectory_name] = []

                all_blogs[subdirectory_name].append(blog_data)

    for subdirectory, blog_data_list in all_blogs.items():
        output_json_path = os.path.join(output_directory, f'{subdirectory}.json')
        with open(output_json_path, 'w') as output_file:
            json.dump(blog_data_list, output_file, indent=2, default=datetime_serializer)

if __name__ == '__main__':
    hugo_content_directory = 'HugoProject/content'
    output_json_directory = 'HugoProject/static/json'

    extract_all_blogs(hugo_content_directory, output_json_directory)
