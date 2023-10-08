import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from config_data.config import Config, load_config
from handlers import admin_handlers, user_handlers
from keyboards.main_menu import set_main_menu
import psycopg2


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

    try:
        conn = psycopg2.connect(dbname="CKDB",
                                user="pr_user",
                                password="Pa$$w0rd",
                                host="vpngw.avalon.ru",
                                port="5432")
        cursor = conn.cursor()
        print("Информация о сервере PostgreSQL")
        print(conn.get_dsn_parameters(), "\n")
    except:
        print("connection refused")
    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    # dp.include_router(admin_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
