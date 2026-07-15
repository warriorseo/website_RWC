import os
import shutil

base_dir = r"d:\AI-Cyborg-2558\_SEO_Clients\RWC"
scripts_dir = os.path.join(base_dir, "scripts")
data_dir = os.path.join(base_dir, "data")

if not os.path.exists(scripts_dir): os.makedirs(scripts_dir)
if not os.path.exists(data_dir): os.makedirs(data_dir)

keep_at_root = {
    'README.md',
    'TODO.md',
    'wp_credentials.env',
    'RWC.code-workspace',
    'RWC - Copy.code-workspace',
}

for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)
    if os.path.isfile(item_path):
        if item in keep_at_root:
            continue
            
        if item.endswith('.py'):
            shutil.move(item_path, os.path.join(scripts_dir, item))
            print(f"Moved script: {item}")
        elif item.endswith('.csv') or item.endswith('.txt'):
            shutil.move(item_path, os.path.join(data_dir, item))
            print(f"Moved data file: {item}")
        else:
            # Check if there are other extensions to keep or move
            print(f"Leaving file alone: {item}")
