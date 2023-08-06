import os
import setuptools  # 没有的直接pip install一下就行了

setuptools.setup(
    name='qingxun-openapi-python-sdk',  # 这里的名字最好和代码的文件名一样
    version='1.0',
    description='qingxun-openapi-python-sdk',  # 一个简要的介绍
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    packages=setuptools.find_packages(),
    include_package_data = True,
)

