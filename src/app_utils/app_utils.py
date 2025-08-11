import os

def get_resource_path(module_file: str, *path_segments: str) -> str:
    """
    Get the absolute path to a resource file relative to the given module file.

    :param module_file: __file__ attribute of the module requesting the resource.
    :param path_segments: Relative path components under the module's directory.
    :return: Absolute path to the resource file.
    """
    module_path = os.path.abspath(module_file)
    base_dir = os.path.dirname(module_path)
    return os.path.join(base_dir, *path_segments)


if __name__ == "__main__":
    # Example usage of get_resource_path
    print(get_resource_path(__file__, "example_resource.txt"))
