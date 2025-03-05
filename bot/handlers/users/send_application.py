from aiogram import types
from bot.loader import dp
from bot.keyboards.default import full_name_keyboard, send_phone_keyboard
from bot.keyboards.inline import submit_application_keyboard, submit_application_callback
from aiogram.dispatcher import FSMContext
from bot.data.config import CHAT_ID, BOT_TOKEN
import logging
from threading import Thread
import asyncio
from bot.utils.db_api.db import create_application


@dp.message_handler(text="Ariza yuborish🗳")
async def get_application(message: types.Message, state: FSMContext):
    
    await message.answer(
        "Ismingizni va familiyangizni kiriting yoki agar ismingiz va familiyangizni to'g'ri ko'rsatilgan bo'lsa shunchaki pastdagi tugmani bosing👇",
        reply_markup=full_name_keyboard(full_name=message.from_user.full_name)
    )

    await state.set_state("full_name")


@dp.message_handler(state="full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text

    await state.update_data(full_name=full_name)

    await message.answer(
        "Telefon raqamingizni yuboring\n"
        "Shunchaki pastdagi tugmani bosing👇",
        reply_markup=send_phone_keyboard
    )

    await state.set_state("phone_number")


@dp.message_handler(state="phone_number", content_types=types.ContentType.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number

    await state.update_data(phone_number=phone_number)

    await message.answer(
        "O'zingiz haqingizda qisqacha ma'lumot bering",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.set_state("about_myself")


@dp.message_handler(state="about_myself")
async def get_about_myself(message: types.Message, state: FSMContext):
    about_myself = message.text

    await state.update_data(about_myself=about_myself)

    await message.answer(
        "Rezyume faylingizni yuboring 📄\n\n"
        "❕ <i>Fayl formati: pdf, doc, docx</i>",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.set_state("resume")


@dp.message_handler(state="resume", content_types=types.ContentType.DOCUMENT)
async def get_resume(message: types.Message, state: FSMContext):
    resume_file_id = message.document.file_id
    resume_file_name = message.document.file_name

    await state.update_data(resume_file_id=resume_file_id)
    await state.update_data(resume_file_name=resume_file_name)

    data = await state.get_data()

    full_name = data.get("full_name")
    phone_number = data.get("phone_number")
    about_myself = data.get("about_myself")

    await message.answer(
        f"<b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"<b>Ismingiz va familiyangiz:</b> {full_name}\n"
        f"<b>Telefon raqamingiz:</b> {phone_number}\n"
        f"<b>O'zingiz haqingizda:</b> {about_myself}\n"
        f"<b>Rezyume faylingiz:</b> {message.document.file_name}\n\n"
        "Ma'lumotlaringizni tasdiqlaysizmi?",
        reply_markup=submit_application_keyboard
    )

    await state.set_state("confirm_application")


async def send_resume_and_get_info(resume_file_id, user_id, full_name, phone_number, about_myself, send_time):
    try:
        sent_message = await dp.bot.send_document(
            chat_id=CHAT_ID,
            document=resume_file_id,
            caption=(
                "📄 Yangi ariza\n\n"
                f"<b>Ism va familiya:</b> {full_name}\n"
                f"<b>Telefon raqam:</b> {phone_number}\n"
                f"<b>Haqida:</b> {about_myself}\n"
                f"<b>Yuborilgan vaqti:</b> {send_time}"
            )
        )

        file_id = sent_message.document.file_id

        # Chat ID va Message ID asosida link yasash
        chat_id = str(sent_message.chat.id).replace("-100", "")  # -100 ni olib tashlash
        message_id = sent_message.message_id
        file_link = f"https://t.me/c/{chat_id}/{message_id}"

        application = await create_application(
            user_id=user_id,
            full_name=full_name,
            phone_number=phone_number,
            about_myself=about_myself,
            resume_file_id=file_id,
            resume_file_link=file_link
        )
        if application:
            logging.info("application created succesfully")

        return file_id, file_link

    except Exception as e:
        logging.exception("Xato yuz berdi resume yuborishda:", exc_info=e)
        return None, None




from django.utils.timezone import now
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def write_to_google_sheet(full_name, phone_number, about_myself, file_link):
    # Google Sheetsga ulanish
    scopes = ["https://www.googleapis.com/auth/spreadsheets", 
              "https://www.googleapis.com/auth/drive.file", 
              "https://www.googleapis.com/auth/drive"]

    credentials = Credentials.from_service_account_file(
        'service_account.json',
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    # Sheet ochish (Google Sheet nomini o'zgartiring)
    sheet = client.open_by_key("1MkTFL0KwswFPKUtJ5oTQRjbN5dwJMdwHCGymmNUJoMQ").sheet1  # sheet1 - birinchi varaq

    # Hozirgi vaqt
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ma'lumotlarni yozish
    data = [current_time, full_name, phone_number, about_myself, file_link]
    sheet.append_row(data)

    print("Data successfully written to Google Sheets")


def process_resume_background(resume_file_id, user_id, full_name, phone_number, about_myself):
    send_time = now().strftime("%Y-%m-%d %H:%M:%S")

    async def task():
        file_id, file_link = await send_resume_and_get_info(
            resume_file_id, user_id, full_name, phone_number, about_myself, send_time
        )

    loop = None
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        asyncio.create_task(task())
    else:
        loop.run_until_complete(task())




@dp.callback_query_handler(submit_application_callback.filter(), state="confirm_application")
async def submit_application(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = call.from_user.id
    action = callback_data.get("action")

    if action == "submit":
        data = await state.get_data()

        full_name = data.get("full_name")
        phone_number = data.get("phone_number")
        about_myself = data.get("about_myself")
        resume_file_id = data.get("resume_file_id")
        resume_file_name = data.get("resume_file_name")

        send_time = call.message.date.strftime("%d-%m-%Y %H:%M:%S")

        process_resume_background(resume_file_id, user_id, full_name, phone_number, about_myself)
        
        await call.message.edit_text("Arizangiz muvaffaqqiyatli yuborildi✅\n"
                                     "Siz bilan tez orada bog'lanamiz.")

        await state.finish()
    
    else:
        await call.message.edit_text("Ariza yuborish bekor qilindi❌\n"
                                     "Bosh menyuga qaytish /start")
        await state.finish()
