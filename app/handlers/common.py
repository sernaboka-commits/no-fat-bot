from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main_menu import main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот NoFAT.\n"
        "Я помогу вести вес, питание и активность.\n"
        "Выберите действие в меню ниже.",
        reply_markup=main_menu_keyboard(),
    )

@router.message()
async def handle_menu(message: Message) -> None:
    text = (message.text or "").strip().lower()

    if text in {"внести вес", "вес"}:
        await message.answer(
            "Запишите сегодняшнее значение веса (кг). Пример: 82.5"
        )
        return

    if text in {"шаги"}:
        await message.answer(
            "Введите количество шагов за день. Пример: 8500"
        )
        return

    if text in {"тренировка"}:
        await message.answer(
            "Опишите тренировку и длительность. Пример: силовая 45 минут"
        )
        return

    if text in {"синхронизировать fatsecret", "fatsecret"}:
        await message.answer(
            "Запускаю загрузку данных из FatSecret. "
            "Будут подтянуты шаги и другие доступные метрики. "
            "Остальные данные можно внести вручную."
        )
        return

    if text in {"отчет недели", "отчёт недели", "отчет"}:
        await message.answer(
            "Еженедельный отчет пока формируется вручную. "
            "В MVP здесь появится автоматический отчет."
        )
        return

    if text in {"помощь", "help"}:
        await message.answer(
            "Используйте кнопки меню, чтобы внести вес, шаги или тренировку."
        )
        return

    await message.answer(
        "Не понял сообщение. Пожалуйста, используйте кнопки меню.",
        reply_markup=main_menu_keyboard(),
    )
