import os

def generate_tree(startpath, output_file=None):
    """
    Generates a directory tree structure and optionally saves it to a file.
    """
    output_lines = []
    
    # Prefix components:
    space = '    '
    branch = '│   '
    tee = '├── '
    last = '└── '

    def inner(dir_path, prefix=''):
        """ A recursive function to build the tree structure. """
        # List all items in the directory and filter out some common ones.
        files = [f for f in os.listdir(dir_path) if f not in ['.git', '__pycache__', '.venv', 'venv']]
        # Sort the files for consistent output
        files.sort()
        
        pointers = [tee] * (len(files) - 1) + [last]
        for pointer, path in zip(pointers, files):
            full_path = os.path.join(dir_path, path)
            output_lines.append(prefix + pointer + path)
            
            if os.path.isdir(full_path):
                # Decide the extension for the prefix
                extension = branch if pointer == tee else space
                # Recurse into the directory
                inner(full_path, prefix + extension)

    # Start the generation from the root of the specified path
    output_lines.append(f"{os.path.basename(os.path.abspath(startpath))}/")
    inner(startpath)
    
    tree_string = "\n".join(output_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_string)
        print(f"Struktur direktori telah disimpan ke '{output_file}'")
    else:
        print(tree_string)


if __name__ == "__main__":
    # The path to the directory you want to scan.
    # We assume this script is in the project root, and we want to scan 'app/'.
    path_to_scan = './app'

    if not os.path.isdir(path_to_scan):
        print(f"Error: Direktori '{path_to_scan}' tidak ditemukan.")
        print("Pastikan skrip ini dijalankan dari root direktori proyek Anda.")
    else:
        # You can specify an output file name here, or leave it as None to print to console.
        output_filename = 'project_tree.txt'
        generate_tree(path_to_scan, output_filename)
