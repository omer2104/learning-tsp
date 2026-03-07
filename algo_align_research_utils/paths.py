import os
import sys
from pathlib import Path


def get_project_root() -> Path:
    """
    Find the project root folder by scanning for requirements.txt and justfile.
    Returns the Path object of the project root.
    
    Returns:
        Path: The project root directory path
        
    Raises:
        FileNotFoundError: If the project root cannot be found
    """
    current_path = Path.cwd()
    
    # Define the files that indicate we're in the project root
    project_files = ['requirements.txt', 'justfile']
    
    # OS-specific root directories to stop at
    if sys.platform == 'win32':
        # On Windows, stop at drive root (e.g., C:\)
        root_dirs = {Path(drive + '\\') for drive in os.listdir('\\') if os.path.isdir(drive + ':\\')}
    elif sys.platform == 'darwin':
        # On macOS, stop at filesystem root (/)
        root_dirs = {Path('/')}
    else:
        # On Linux/Unix, stop at filesystem root (/)
        root_dirs = {Path('/')}
    
    # Walk up the directory tree
    while current_path not in root_dirs:
        # Check if current directory contains both project files
        if all((current_path / file).exists() for file in project_files):
            return current_path
        
        # Move up one directory
        current_path = current_path.parent
    
    # If we reach here, we couldn't find the project root
    raise FileNotFoundError(
        f"Could not find project root (directory containing both 'requirements.txt' and 'justfile'). "
        f"Reached root directory: {current_path}"
    )


def get_project_root_str() -> str:
    """
    Convenience function that returns the project root as a string.
    
    Returns:
        str: The project root directory path as a string
    """
    return str(get_project_root()).replace('\\', '/')
