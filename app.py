from flask import Flask, render_template, abort, request
import os
from storage.manager import FileStorageManager

app = Flask(__name__)

# Configuration
FILES_FOLDER = 'files'
file_manager = FileStorageManager(FILES_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
@app.route('/items/folder/<item_id>')
def items(item_id=None):
    structure = file_manager.get_structure()
    items_list = structure['items']
    
    # Get current folder and build breadcrumb path
    current_folder = None
    breadcrumbs = []
    
    if item_id:
        current_folder = next((item for item in items_list if item.id == item_id), None)
        if not current_folder or current_folder.type != 'folder':
            abort(404)
            
        # Build breadcrumbs
        temp_folder = current_folder
        while hasattr(temp_folder, 'parent'):
            parent = next((item for item in items_list if item.id == temp_folder.parent), None)
            if parent:
                breadcrumbs.insert(0, parent)
                temp_folder = parent
            else:
                break
        breadcrumbs.append(current_folder)
    
    # Filter items for current folder
    filtered_items = [
        item for item in items_list 
        if (not item_id and not hasattr(item, 'parent')) or
           (hasattr(item, 'parent') and item.parent == item_id)
    ]
    
    return render_template('items.html', 
                         items=filtered_items, 
                         current_folder=current_folder,
                         breadcrumbs=breadcrumbs)

@app.route('/items/file/<item_id>')
def item_detail(item_id):
    structure = file_manager.get_structure()
    item = next((item for item in structure['items'] if item.id == item_id), None)
    
    if not item or item.type != 'file':
        abort(404)
    
    # Generate breadcrumbs by traversing up through parent folders
    breadcrumbs = []
    if not hasattr(item, 'parent'):
        # If item has no parent, it's in the root folder
        breadcrumbs = [{'id': None, 'name': 'root', 'type': 'folder'}]
    else:
        current = next((i for i in structure['items'] if i.id == item.parent), None)
        while current:
            breadcrumbs.insert(0, current)
            current = next((i for i in structure['items'] if i.id == current.parent), None) if hasattr(current, 'parent') else None

    try:
        full_path = os.path.join(FILES_FOLDER, item.file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('item_detail.html', item=item, content=content, breadcrumbs=breadcrumbs)
    except Exception as e:
        abort(500)

if __name__ == '__main__':
    os.makedirs(FILES_FOLDER, exist_ok=True)
    app.run(debug=True, port=5003)
