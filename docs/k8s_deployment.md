# Kubernetes Deployment Guide for SFMShop

## Описание

Проект разворачивается в Kubernetes с использованием:

- Deployment (3 реплики приложения)
- Service (LoadBalancer для внешнего доступа)


##  Развертывание

1. Собрать Docker-образ:
```
docker build -t microserviceshop:latest -f docker/Dockerfile .
```

2. Применить конфиги:
```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Проверки:
1. Проверяем, что запустилось действительно 3 пода:
```
kubectl get pods
```

2. Проверка, что запущен сервис:
```
kubectl get services
```

3. Запущена реплика
```
kubectl get deployments
```

## Масштабирование
1. Увеличение количества реплик до 5:
```
kubectl scale deployment microserviceshop-deployment --replicas=5
```
2. Проверка количества подов:
```
kubectl get pods
```