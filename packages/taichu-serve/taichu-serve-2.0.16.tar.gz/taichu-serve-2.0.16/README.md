## 介绍

taichu-serve 是一个基于python的服务端模型部署框架，旨在提供一个简单易用的模型部署方案，让开发者可以专注于模型的开发和优化，而不用关心模型的部署和运维。

## 特性

-   **简单易用**：极简情况下，只需编写一个customize_service.py文件，即可完成模型的部署。
-   **免写WebServer**：开发者无需编写Web服务，只需编写模型前后处理逻辑。
-   **多协议支持**：支持http、grpc、流式grpc三种协议。
-   **服务治理**：支持链路追踪、限流、探活等服务治理功能。
-   **性能指标**：内置了核心指标埋点，如QPS、延迟、吞吐量等。


## Quick Start

### 环境要求
-   Python 3.6+
-   Docker


### 1. 安装

```bash
pip3 install taichu-serve -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 初始化模型包
提供一个脚手架工具，可以帮助开发者快速初始化一个模型包。开发者需要修改模型包内的`customize_service.py`文件，实现模型的前后处理逻辑，以及模型的加载、预热等接口。
```bash
taichu_serve init
```
执行后会在当前目录下生成一个名为`project`的文件夹，参考[模型包目录结构说明](#模型包目录结构说明)。

### 3. 启动模型服务
开发者能够在本地启动模型服务，方便调试。
```bash
cd project
taichu_serve run
```
模型会在本地启动启动http服务和grpc服务，端口分别为`8080`和`8081`，可以通过[标准预测协议](https://github.com/kserve/kserve/tree/master/docs/predict-api/v2)进行预测请求。

### 4. 测试预测请求
脚手架预置了http、grpc、流式grpc三种测试脚本，开发者可以根据自己的需求修改测试脚本
```bash
# 测试http请求
python3 test/http_client.py
# 测试grpc请求
python3 test/grpc_client.py
# 测试流式请求
python3 test/stream_grpc_client.py
```

### [可选] 构建的运行环境镜像
如果平台提供的基础镜像不能满足你的需求，你可以自己构建一个镜像，然后将镜像上传到平台swr仓库，再在平台上部署。
```bash
taichu_serve build --from_image {你的基础镜像} 
# 例如 taichu_serve build --from_image python:3.7
```
命令成功后会在本地生成一个可在平台部署的新镜像,镜像名关注命令行输出的`Successfully built`后的镜像名

`taichu_serve build`能改造你的基础镜像，使其能够用于在平台上部署。注：镜像只含有模型服务的运行环境，内不包含模型文件。

#### 上传镜像到平台
本地测试完毕后，将镜像上传到平台swr仓库
```bash
docker tag {镜像名} {平台仓库地址}/{镜像名}
docker push {平台仓库地址}/{镜像名}
```

## 模型包目录结构说明
执行`taichu_serve init`后，会在当前目录下生成一个名为`project`的文件夹，目录结构如下：
```bash
project
├── test                            # 可选，测试脚本文件夹
│       ├── grpc_client.py          # 可选，grpc测试客户端
│       ├── http_client.py          # 可选，http测试客户端
│       └── stream_grpc_client.py   # 可选，流式grpc测试客户端
├── customize_service.py            # 必填，模型服务自定义逻辑
├── models                          # 可选，模型文件夹
├── config.ini                      # 可选，项目配置文件
├── requirements.txt                # 可选，项目pip依赖
├── dependencies.txt                # 可选，项目apt依赖
├── launch.sh                       # 可选，镜像启动脚本。如果执行了taichu_serve build，会生成该文件，除非有特殊需求，否则不需要修改该文件
└── Dockerfile                      # 可选，镜像dockerfile。如果执行了taichu_serve build，会生成该文件，如有特殊需求，请基于该文件自行构建部署镜像
```

## 模型服务代码说明 
模型包内只有一个必填文件`customize_service.py`，该文件内包含了模型服务的自定义逻辑，开发者需要在该文件内实现模型的前后处理逻辑，以及模型的加载、预热等逻辑。

### customize_service.py
```python
import logging

from taichu_serve import Service

logger = logging.getLogger(__name__)


class ModelService(Service):
    def __init__(self, model_path):
        """
        Args:
            model_path: 模型文件夹路径
        """
        super(ModelService, self).__init__(model_path)
        logger.info("self.model_path: %s",
                    model_path)

    def _preprocess(self, input_data, context):
        """
        Args:
            input_data: 输入数据
            context: 请求上下文,一般用于流式请求
        """   
        logger.info('enter _preprocess')
        return input_data

    def _inference(self, preprocessed_result, context):
        logger.info('enter _inference')        
        return preprocessed_result

    def _postprocess(self, inference_result, context):
        logger.info('enter _postprocess')

        return inference_result
    
    # 可选，模型预热逻辑
    def _warmup(self):
        logger.info('warmup finished')
```


