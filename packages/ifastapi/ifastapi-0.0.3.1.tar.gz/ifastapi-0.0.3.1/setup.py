import setuptools

setuptools.setup(name='ifastapi',
                 version='0.0.3.1',
                 description='基于fastapi二次优化 旨在更便捷、快速的搭建API',
                 url='https://github.com/ifczt/iFastApi',
                 author='IFCZT',
                 author_email='ifczt@qq.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 password='aa83896389',
                 install_requires=["fastapi","sqlalchemy","uvicorn","pymysql"],
                 zip_safe=False)
