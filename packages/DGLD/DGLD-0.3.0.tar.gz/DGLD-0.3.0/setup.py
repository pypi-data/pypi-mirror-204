from setuptools import setup, find_packages
setup(name='DGLD', #注意一定不要和pypi官网上之前出现过的模块名重复，不然报错
      version='0.3.0',
      description='A Deep Graph Anomaly Detection Library based on DGL',
      author='miziha-zp;zhoushengisnoob;GavinYGM;fmc123653;cfuser;Xinstein-rx',
      author_email='arlenjing@gmail.com', #这里务必填写正确的email格式
      packages=find_packages(),  # 表示你要封装的包，find_packages用于系统自动从当前目录开始找包
      license="apache 3.0"
      )