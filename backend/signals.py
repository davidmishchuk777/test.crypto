# Список сигналов
signals = []

# Добавление сигнала
def add_signal(signal):
    # Чтобы не дублировать один и тот же сигнал
    if signal not in signals:
        signals.append(signal)

# Получение всех сигналов
def get_signals():
    return signals
