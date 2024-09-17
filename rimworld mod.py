import os
import xml.etree.ElementTree as ET
import re

def sanitize_filename(name):
    # Remove invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', name)

def rename_folders_with_xml_info(base_dir):
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        
        if not folder_name.isdigit():
            continue
        
        if not os.path.isdir(folder_path):
            continue

        about_path = os.path.join(folder_path, 'About', 'About.xml')
        
        if not os.path.exists(about_path):
            continue

        tree = ET.parse(about_path)
        root = tree.getroot()
        
        # Extract <name> and latest <supportedVersion>
        name = root.find('name').text
        supported_versions = root.find('supportedVersions')
        latest_version = max(
            version.text for version in supported_versions.findall('li')
        )
        
        # Create new folder name
        sanitized_name = sanitize_filename(name)
        new_folder_name = f"{sanitized_name} - {latest_version}"
        new_folder_path = os.path.join(base_dir, new_folder_name)
        
        # Rename the folder
        os.rename(folder_path, new_folder_path)
        print(f"Renamed '{folder_name}' to '{new_folder_name}'")

if __name__ == "__main__":
    # Specify the base directory containing your folders
    base_directory = 'TO\\Mods'
    rename_folders_with_xml_info(base_directory)