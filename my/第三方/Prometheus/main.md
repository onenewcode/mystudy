# Prometheuss实战
## Prometheus监控Kubernetes
### 搭建本地Kubernetes集群
为了能够更直观的了解和使用Kubernetes，我们将在本地通过工具Minikube(https://github.com/kubernetes/minikube)搭建一个本地的Kubernetes测试环境。Minikube会在本地通过虚拟机运行一个单节点的Kubernetes集群，可以方便用户或者开发人员在本地进行与Kubernetes相关的开发和测试工作。
安装过程就不再赘述

**启动**
```shell
$ minikube start
Starting local Kubernetes v1.7.5 cluster...
Starting VM...
SSH-ing files into VM...
Setting up certs...
Starting cluster components...
Connecting to cluster...
Setting up kubeconfig...
Kubectl is now configured to use the cluster.
```
MiniKube会自动配置本机的kubelet命令行工具，用于与对集群资源进行管理。同时Kubernetes也提供了一个Dashboard管理界面，在MiniKube下可以通过以下命令打开：
```shell
$ minikube dashboard
Opening kubernetes dashboard in default browser...
```
Kubernetes中的Dashboard本身也是通过Deployment进行部署的，因此可以通过MiniKube找到当前集群虚拟机的IP地址：
```shell
$ minikube ip
192.168.49.2
```
通过kubectl命令行工具，找到Dashboard对应的Service对外暴露的端口，如下所示，kubernetes-dashboard是一个NodePort类型的Service，并对外暴露了30000端口：
```shell
$ kubectl get service --namespace=kube-system
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   12d
```
在Dashbord中，用户可以可视化的管理当前集群中运行的所有资源，以及监视其资源运行状态。


Kubernetes环境准备完成后，就可以开始尝试在Kubernetes下尝试部署一个应用程序。Kubernetes中管理的所有资源都可以通过YAML文件进行描述。如下所示，创建了一个名为nginx-deploymeht.yml文件：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.26.0
        ports:
        - containerPort: 80
```
在该YAML文件中，我们定义了需要创建的资源类型为Deployment，在metadata中声明了该Deployment的名称以及标签。spec中则定义了该Deployment的具体设置，通过replicas定义了该Deployment创建后将会自动创建3个Pod实例。运行的Pod以及进行则通过template进行定义。

在命令行中使用，如下命令：
```SHELL
$ kubectl create -f nginx-deploymeht.yml
deployment "nginx-deployment" created
```
在未指定命名空间的情况下，kubectl默认关联default命名空间。由于这里没有指定Namespace，该Deployment将会在默认的命令空间default中创建。 通过kubectl get命令查看当前Deployment的部署进度：


```SHELL
# 查看Deployment的运行状态
$ kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           8m39s


# 查看运行的Pod实例
$ kubectl get pods
NAME                                READY     STATUS    RESTARTS   AGE
nginx-deployment-6d8f46cfb7-5f9qm   1/1       Running   0          1m
nginx-deployment-6d8f46cfb7-9ppb8   1/1       Running   0          1m
nginx-deployment-6d8f46cfb7-nfmsw   1/1       Running   0          1m
```
为了能够让用户或者其它服务能够访问到Nginx实例，这里通过一个名为nginx-service.yml的文件定义Service资源：
```SHELL
apiVersion: v1
kind: Service
metadata:
  labels:
    app: web
  name: nginx-service
spec:
  type: NodePort # 服务类型
  ports:
  - port: 80 # Service端口
    protocol: TCP # 协议
    targetPort: 80 # 容器端口
    nodePort: 30001  # 对外暴露的端口，可以指定
  selector:
    app: nginx # 指定关联Pod的标签

```
默认情况下，Service资源只能通过集群网络进行访问(type=ClusterIP)。这里为了能够直接访问该Service，需要将容器端口映射到主机上，因此定义该Service类型为NodePort。

创建并查看Service资源：
```shell
$ kubectl create -f nginx-service.yml
service "nginx-service" created

$ kubectl get svc
NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP        131d
nginx-service   NodePort    10.104.103.112   <none>        80:32022/TCP   10s
```