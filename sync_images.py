import os
import re
import shutil

# --- CONFIGURATION (Change these to match your setup!) ---
obsidian_vault = r"C:\Users\Lenovo\Documents\Obsidian Vault"  # YOUR Obsidian vault path
hugo_site = r"C:\Users\Lenovo\Documents\omarblog"
posts_dir_en = os.path.join(hugo_site, "content", "en", "posts")
posts_dir_ar = os.path.join(hugo_site, "content", "ar", "posts")
attachments_dir = os.path.join(obsidian_vault, "Attachments")
static_images_dir = os.path.join(hugo_site, "static", "images")

# --- Function to process a single Markdown file ---
def process_markdown_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Find all image links in the format ![Alt Text](image.jpg)
        images = re.findall(r'!\[([^\]]*)\]\(([^\)]*)\)', content)
        print(f"Images found in file {filepath}: {images}") # Debug print

        for alt_text, image_filename in images:
            # Remove any leading /images/ from the filename
            image_filename = image_filename.replace('/images/', '') # Crucial fix
            print(f"  Processing image: filename={image_filename}, alt_text={alt_text}") # Debug print
            image_source = os.path.join(attachments_dir, image_filename.replace('%20',' '))
            image_destination = os.path.join(static_images_dir, image_filename.replace('%20', ' '))
            markdown_image = f"![{alt_text}](/images/{image_filename.replace(' ', '%20')})"

            print(f"    image_source: {image_source}")  # VERY IMPORTANT DEBUG PRINT
            print(f"    image_destination: {image_destination}") # Debug print

            # Copy image if it exists
            if os.path.exists(image_source):
                print(f"DEBUG:     Image exists at source: {image_source}")
                try:
                    shutil.copy2(image_source, image_destination) # copy2 preserves metadata
                    print(f"DEBUG:     Copied: {image_filename}")
                    # Replace the link in the markdown content
                    content = content.replace(f"![{alt_text}]({image_filename})", markdown_image)

                except Exception as e:
                    print(f"DEBUG:     Error copying {image_filename}: {e}")
            else:
                print(f"DEBUG:     Image not found: {image_source}") # Print full path

        # Write the updated content back to the Markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

    except FileNotFoundError:
        print(f"DEBUG: Error: File not found: {filepath}")
    except Exception as e:
        print(f"DEBUG: An error occurred processing {filepath}: {e}")


# --- Create the static/images directory if it doesn't exist ---
os.makedirs(static_images_dir, exist_ok=True)

# --- Process English posts ---
print("DEBUG: Processing English posts...")
for filename in os.listdir(posts_dir_en):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir_en, filename)
        process_markdown_file(filepath)

# --- Process Arabic posts ---
print("DEBUG: Processing Arabic posts...")
for filename in os.listdir(posts_dir_ar):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir_ar, filename)
        process_markdown_file(filepath)

print("DEBUG: Image processing and copying complete.")