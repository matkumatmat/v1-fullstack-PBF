import os
def generate_tree(startpath, output_file=None):
    output_lines = []
    space = '    '
    branch = '│   '
    tee = '├── '
    last = '└── '

    def inner(dir_path, prefix=''):
        files = [f for f in os.listdir(dir_path) if f not in ['.git', '__pycache__', '.venv', 'venv']]
        files.sort()
        
        pointers = [tee] * (len(files) - 1) + [last]
        for pointer, path in zip(pointers, files):
            full_path = os.path.join(dir_path, path)
            output_lines.append(prefix + pointer + path)
            
            if os.path.isdir(full_path):
                extension = branch if pointer == tee else space
                inner(full_path, prefix + extension)

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
    path_to_scan = './app'

    if not os.path.isdir(path_to_scan):
        print(f"Error: Direktori '{path_to_scan}' tidak ditemukan.")
        print("Pastikan skrip ini dijalankan dari root direktori proyek Anda.")
    else:
        output_filename = 'project_tree.txt'
        generate_tree(path_to_scan, output_filename)
