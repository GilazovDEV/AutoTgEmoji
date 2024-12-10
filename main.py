from telethon import TelegramClient, functions
from telethon.tl import types
import asyncio
import win32gui
import win32process
import psutil

# Получаем процесс и даем им айди
def get_active_process_name():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    process_name = process.name().replace(".exe", "")
    doc_ids = {
        "Code": 5384191691123090229,
        "Figma": 5384607233503946876,
        "chrome": 5384585887516485051,
        "Opera": 5384585887516485051,
        "Android": 5384067592338042212,
        "Unity": 5384077814360205688,
        "Vim": 5384196510076399424,
        "Studio": 5384471168940009751,
        "Sublime": 5386459034423419671,
        "Microsoft": 5386596567866173031,
        "powershell": 5386686882438471266,
        "Терминал": 5386686882438471266,
        "python": 5384390303295757845,
        "devenv": 5386854892969156974,
    }
    return doc_ids.get(process_name, 5386596567866173031)

# Настройки Telegram
api_id = "id"  # Заменить на ваш API ID
api_hash = "hash"  # Заменить на ваш API Hash
phone = "+num"  # Заменить на ваш номер телефона, начиная с '+'
client = TelegramClient("session_name", api_id, api_hash)

# Установка премиум-эмодзи в статус
async def set_emoji_status(emoji_document_id):
    result = await client(
        functions.account.UpdateEmojiStatusRequest(
            emoji_status=types.EmojiStatus(document_id=emoji_document_id)
        )
    )
    print(f"Эмодзи-статус установлен: {result}")

# обновляем и сравниваем эмодзи
async def monitor_processes():
    await client.start(phone)
    current_doc_id = None

    try:
        while True:
            # получаем новый айди
            new_doc_id = get_active_process_name()
            # проверяем
            if new_doc_id != current_doc_id:
                current_doc_id = new_doc_id
                # устанавливаем
                await set_emoji_status(current_doc_id)
            await asyncio.sleep(2)
            # исключаем ошибку при завершений работы
    except KeyboardInterrupt:
        print("Завершение работы бота...")
    finally:
        # отключаемся
        await client.disconnect()
        
# запускаем события
if __name__ == "__main__":
    asyncio.run(monitor_processes())

# devniel; my channel tg - @jeaunity