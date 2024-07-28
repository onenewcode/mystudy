# 创建环境
conda create -n deep python=3.10


# 激活环境
activate your_env_name

# 删除虚拟环境
conda remove -n your_env_name --all
# 查看环境
conda info -e









conda install keras
conda create -n deep tensorflow-gpu
```py

    import os
    os.environ["CUDA_VISIBLE_DEVICES"]="0"
```    