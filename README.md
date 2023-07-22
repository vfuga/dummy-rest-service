# Собрать образ
- docker build -f .\docker\Dockerfile -t dummy-generator .
  
# Запустить контейнер
- docker run --rm -ti -p 0.0.0.0:8800:80 --name dummy-generator dummy-generator

# Example: 
  - посылаем произвольный (но валидный!!! json)
    - curl -X POST http://localhost:8800 -d '{"a": "a"}' -H "Content-Type: application/json"
  - получаем пачку данных
    - curl -X GET http://localhost:8800
  - получаем одну строку
    - curl -X GET http://localhost:8800/one