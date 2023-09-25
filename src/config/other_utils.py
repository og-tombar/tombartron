import os


def update_dict_recursive(src_dict: dict, dest_dict: dict) -> None:
    for key in src_dict:
        if key in dest_dict and isinstance(dest_dict[key], dict) and isinstance(src_dict[key], dict):
            update_dict_recursive(dest_dict[key], src_dict[key])
        else:
            dest_dict[key] = src_dict[key]


def empty_dir(dir_path: str) -> None:
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
