import subprocess


def check_dependencies():
    dependencies = ['matplotlib', 'tkinter']

    missing_dependencies = []
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing_dependencies.append(dep)

    if missing_dependencies:
        print(f"Missing dependencies: {', '.join(missing_dependencies)}")
        print("Installing missing dependencies...")
        try:
            subprocess.check_call(["pip", "install", *missing_dependencies])
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
    else:
        print("All required dependencies are already installed.")


if __name__ == "__main__":
    check_dependencies()
