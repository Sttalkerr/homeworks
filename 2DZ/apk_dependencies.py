import subprocess
import yaml
import sys
import re

def generate_mermaid_graph(dependencies):
    mermaid_str = "graph TD\n"
    for package, deps_list in dependencies.items():
        for deps_dict in deps_list: 
            for dep_package, dep_deps in deps_dict.items(): 

                mermaid_str += f"    {package} --> {dep_package}\n"
                
                if dep_deps: 
                    for sub_dep in dep_deps:
                        if isinstance(sub_dep, dict): 
                            for sub_dep_package, _ in sub_dep.items():
                                mermaid_str += f"    {dep_package} --> {sub_dep_package}\n"
                        else:
                            for sub_dep_package in sub_dep:
                                mermaid_str += f"    {dep_package} --> {sub_dep_package}\n"
    return mermaid_str

def get_dependencies(package_name, max_depth, current_depth):
    if current_depth > max_depth:
        return []
    
    try:
        result = subprocess.run(["apk", "info", "-R", package_name], capture_output=True, text=True)
        
        dependencies = result.stdout.splitlines()
        
        dependency_tree = {package_name: []}

        for dep in dependencies:
            dep = dep.split(" ")[0]
            if '=' in dep or '>' in dep:
                if '>' in dep:
                    dep=dep[:dep.find('>')]
                if '=' in dep:
                    dep=dep[:dep.find('=')]
            if dep and dep != package_name: 
                if dep not in dependency_tree:
                    sub_dependencies = get_dependencies(dep, max_depth,current_depth + 1)
                    dependency_tree[package_name].append(sub_dependencies)
        return dependency_tree
    except subprocess.CalledProcessError as e:
        print(f"Error fetching dependencies for {package_name}: {e}")
        return []

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл config.yaml не найден.", file=sys.stderr)
        return None
    except yaml.YAMLError as e:
        print(f"Ошибка парсинга config.yaml: {e}", file=sys.stderr)
        return None

def main():
    config = load_config('config.yaml')
    if config:
        dependencies = get_dependencies(config['package_name'], config['max_depth'],0)
        mermaid_str = generate_mermaid_graph(dependencies)
        print(mermaid_str)

if __name__ == "__main__":
    main()