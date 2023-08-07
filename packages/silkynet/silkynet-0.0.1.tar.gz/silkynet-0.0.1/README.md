

python setup.py sdist bdist_wheel
twine check dist/*



# 打包到私有云

- pip install devpi-client # 安装客服端
- devpi use https://matrix.amh-group.com/devpi/root/dev
- devpi use dev
- 进入待构建的项目setup.py目录,构建和上传你的包到 root/dev 索引
- devpi login root #登录密码 matrix
- devpi upload

# 本地环境打包

#### 先清除build,egg.info

```shell
pip install --upgrade setuptools wheel twine #安装打包工具
python setup.py bdist_wheel  
python setup.py sdist  
python setup.py sdist bdist_wheel
pip uninstall kflearn -y
pip install .\dist\kflearn-2.0.1-py3-none-any.whl
```

* dist/ 目录中生成两个文件
    * example_pkg_your_username-0.0.1-py3-none-any.whl
    * example_pkg_your_username-0.0.1.tar.gz

# pypi源操作

```shell
cat ~/.pip/pip.conf #查看pypi
pip config set global.index-url https://matrix.amh-group.com/devpi/root/dev #本地设置pipy源
python setup.py install #安装  
twine check dist/*
twine upload dist/*
pip install -U example_pkg -i https://pypi.org/simple # 安装最新的版本测试
```

# `kfl`命令行工具：

* 上传文件（直传,文件小于300Mi）  
  ```kfl put2 requirements.txt -env prd```
* 上传文件（通过token上传,文件可大于300Mi，但需访问外网）  
  ```kfl put requirements.txt horn/requirements.txt -env dev -biz predict-transfer```
* 上传文件为模型  
  ```kfl put requirements.txt horn/requirements.txt -env dev -biz predict-transfer -model modelname v1.0 horn```
* 下载文件  
  `kfl get ymmfile/predict-transfer/horn/requirements.txt aaa.txt -env dev -biz 'predict-transfer'`