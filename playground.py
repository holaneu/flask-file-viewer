import os
import json
from storage.manager import FileStorageManager

def pretty_print_structure(structure):
    """Print the file structure in a readable format"""
    print(json.dumps(structure, indent=2, default=vars))

def main():
    # Define the base directory for our files
    base_dir = os.path.join(os.path.dirname(__file__), 'files')
    
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created base directory: {base_dir}")
    
    try:
        # Initialize the file storage manager
        manager = FileStorageManager(base_dir)
        
        # Get and display the file structure
        structure = manager.get_structure()
        print("\nFile system structure:")
        pretty_print_structure(structure)
        
        print(f"\nTotal items found: {structure['total']}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
