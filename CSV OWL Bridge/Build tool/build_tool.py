import subprocess
import sys
import os

def install(package):
    """
    Installs the given package using pip.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """
    Main function that reads the requirements from 'requirements.txt' and installs any missing packages.
    """
    if not os.path.exists('requirements.txt'):
        print("Error: 'requirements.txt' not found.")
        return

    with open('requirements.txt', 'r') as f:
        packages = f.readlines()

    for package in packages:
        package = package.strip()
        if not package:
            continue

        try:
            __import__(package)
            print(f"'{package}' is already installed.")
        except ImportError:
            print(f"Installing '{package}'...")
            install(package)

    print("All required packages are installed or updated.")

if __name__ == "__main__":
    main()
