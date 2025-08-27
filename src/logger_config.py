import logging

# Общий формат логирования объявлен перед функцией
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_module_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

    # Обработчик файла, перезапись при запуске
    fh = logging.FileHandler(f'logs/{module_name}.log', mode='w')
    fh.setFormatter(logging.Formatter(log_format))
    logger.addHandler(fh)

    return logger
