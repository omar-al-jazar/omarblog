import os
import re
import shutil

def process_markdown_files(content_dir):
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                process_single_file(filepath)

def process_single_file(filepath):
    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        # Corrected regex to handle more cases
        updated_content = re.sub(r'!\[(.*?)\]\(((?!https?://)(.*?))\)', r'![\1]({\77< static "\2" >})', content)
        f.seek(0)
        f.write(updated_content)
        f.truncate()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(script_dir, "content")
    process_markdown_files(content_dir)