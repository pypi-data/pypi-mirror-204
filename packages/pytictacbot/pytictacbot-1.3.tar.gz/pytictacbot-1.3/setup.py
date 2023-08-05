from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pytictacbot",
    version="1.3",
    packages=["tictacbot"],
    include_package_data=True,
    description="A program that makes you unbeatable at BombParty",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pynput",
        "pyperclip",
        "pyautogui",
        "art",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "tictacbot=tictacbot.listen:__main__"
        ]
    }
)