# p2c

DNA primer to comment translator as kubernetes cluster in azure

# setup development env on windows 10

## install WSL

source: https://docs.microsoft.com/de-de/windows/wsl/install-win10

open powersell as administrator and enter
```
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

open microsoft store
search for linux, choose distribution and install

## install azure-cli

source: https://docs.microsoft.com/de-de/cli/azure/install-azure-cli-apt?view=azure-cli-latest

open linux distribution bash

```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

time to finish your coffee you got earlier

# k8s cluster setup

## create k8s cluster in azure

* enter portal.azure.com
* search for kubernetes services
* create kubernetes cluster
* review + create
* time to get a coffee

## inital kubectl for cli

```
az aks install-cli
set HTTPS_PROXY=<proxy-adress>:<port>
set HTTP_PROXY=<proxy-adress>:<port>
set https_proxy=<proxy-adress>:<port>
set http_proxy=<proxy-adress>:<port>
az login
az account set --subscription <subscription ID or name>
az aks get-credentials -g <resource-group> -n <clustername>
```

## create cluster role bindings for rbac auth (only initial)

```
kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard
```

## k8s cluster browser

```
az aks browse -g <resource-group> -n <clustername>
```




