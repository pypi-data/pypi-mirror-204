from setuptools import setup


setup(
    name="clean_folder_homework_by_egor",
    version="1.0.0",
    description="homework",
    packages=['clean_folder_homework_by_egor'],
    entry_points=dict(console_scripts=[
        'clean_folder = clean_folder_homework_by_egor.clean:main'
    ])
    )