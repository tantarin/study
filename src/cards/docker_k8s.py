from src.models import Question

DOCKER_K8S_CARDS = [
    Question(
        text="Основы Docker",
        theory="""Docker - это платформа для контейнеризации приложений:

1. Основные концепции:
- Образы (Images)
- Контейнеры (Containers)
- Dockerfile
- Docker Compose
- Docker Registry

2. Компоненты Docker:
- Docker Engine
- Docker CLI
- Docker Hub
- Docker Desktop

3. Управление контейнерами:
- Создание и запуск
- Сети и порты
- Тома и данные
- Логирование
- Мониторинг

4. Безопасность:
- Привилегии
- Изоляция
- Сканирование образов
- Secrets""",
        theory_summary="Docker позволяет упаковывать приложения в контейнеры для обеспечения изоляции и переносимости.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем Docker на практических примерах:

1. Создание Dockerfile:
```dockerfile
# Базовый образ
FROM openjdk:17-jdk-slim

# Рабочая директория
WORKDIR /app

# Копирование файлов
COPY target/*.jar app.jar

# Открытие порта
EXPOSE 8080

# Запуск приложения
ENTRYPOINT ["java", "-jar", "app.jar"]
```

2. Сборка и запуск контейнера:
```bash
# Сборка образа
docker build -t myapp:1.0 .

# Запуск контейнера
docker run -d \
    --name myapp \
    -p 8080:8080 \
    -e SPRING_PROFILES_ACTIVE=prod \
    myapp:1.0

# Просмотр логов
docker logs -f myapp
```

3. Docker Compose для микросервисов:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DB_HOST=postgres
    depends_on:
      - postgres

  postgres:
    image: postgres:14
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

4. Управление сетями:
```bash
# Создание сети
docker network create my-network

# Подключение контейнера к сети
docker network connect my-network myapp

# Просмотр сетей
docker network ls
```

5. Работа с томами:
```bash
# Создание тома
docker volume create my-data

# Монтирование тома
docker run -d \
    --name myapp \
    -v my-data:/app/data \
    myapp:1.0

# Просмотр томов
docker volume ls
```

Практические советы:
1. Используйте многоэтапную сборку для уменьшения размера образов
2. Не запускайте контейнеры от root
3. Регулярно обновляйте базовые образы
4. Используйте .dockerignore для исключения ненужных файлов
5. Настраивайте health checks для контейнеров""",
        points=0
    ),
    Question(
        text="Основы Kubernetes",
        theory="""Kubernetes (K8s) - это оркестратор контейнеров:

1. Основные концепции:
- Pod
- Deployment
- Service
- ConfigMap
- Secret
- Volume

2. Архитектура:
- Master Node
- Worker Nodes
- kubelet
- kube-proxy
- etcd
- API Server

3. Управление ресурсами:
- Namespace
- Resource Quotas
- Limits и Requests
- Horizontal Pod Autoscaling

4. Сети и сервисы:
- ClusterIP
- NodePort
- LoadBalancer
- Ingress
- Network Policies""",
        theory_summary="Kubernetes обеспечивает автоматизацию развертывания, масштабирования и управления контейнерами.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем Kubernetes на практических примерах:

1. Создание Deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

2. Создание Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

3. Настройка ConfigMap и Secret:
```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  SPRING_PROFILES_ACTIVE: "prod"
  LOG_LEVEL: "INFO"

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c2VjcmV0  # base64 encoded
```

4. Настройка Ingress:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

5. Настройка Horizontal Pod Autoscaling:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

Практические советы:
1. Используйте Health Checks для Pod'ов
2. Настраивайте Resource Limits
3. Применяйте Network Policies для безопасности
4. Используйте Namespaces для изоляции
5. Регулярно обновляйте образы контейнеров""",
        points=0
    )
] 