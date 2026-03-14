from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from signals import get_signals
from scanner import start_scanner

# Создаём приложение
app = FastAPI(title="Crypto Spread Scanner")

# Разрешаем запросы с любого источника (для frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить конкретным доменом
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Запускаем сканер в фоновом потоке
start_scanner()

# Главная страница
@app.get("/")
def root():
    return {"status": "scanner running"}

# Получение текущих сигналов
@app.get("/signals")
def signals():
    return get_signals()
