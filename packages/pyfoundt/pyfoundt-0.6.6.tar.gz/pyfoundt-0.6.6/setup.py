from setuptools import setup, find_packages

setup(
    name='pyfoundt',
    packages=find_packages(),
    version='0.6.6',
    install_requires=[
        "requests"
    ],
    author="ZuoYihan",
    description="一个普通的模块",
    long_description="一个简洁且易于上手的一种包含了Python语言一些常用操作的模块.",
    platforms=["Windows", "Linux"],
    python_requires='>=3',
    classifiers=[  # 程序的所属分类列表
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ]
)
