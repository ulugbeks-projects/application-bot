from bot.loader import bot
from bot.data.config import CHAT_ID
import logging
import asyncio


async def send_resume_file_to_chat_async(resume_file_id, **other_data):
    try:
        await bot.send_document(
            chat_id=CHAT_ID,
            document=resume_file_id,
            caption=(
                f"<b>Yangi ariza:</b>\n\n"
                f"<b>Ismi va familiya:</b> {other_data.get('full_name')}\n"
                f"<b>Telefon raqam:</b> {other_data.get('phone_number')}\n"
                f"<b>O'zi haqida:</b> {other_data.get('about_myself')}\n"
                f"<b>Yuborilgan vaqti:</b> {other_data.get('send_time')}\n"
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        logging.exception(e)
    finally:
        await bot.session.close()  # Muhim!

def send_resume_file_to_chat_task(resume_file_id, **other_data):
    asyncio.run(send_resume_file_to_chat_async(resume_file_id, **other_data))