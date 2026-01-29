from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.main_menu import main_menu_keyboard

router = Router()


class InputState(StatesGroup):
    waiting_weight = State()
    waiting_steps = State()
    waiting_training = State()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот NoFAT.\n"
        "Я помогу вести вес, питание и активность.\n"
        "Выберите действие в меню ниже.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(StateFilter(None))
async def handle_menu(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip().lower()

    if text in {"внести вес", "вес"}:
        await state.set_state(InputState.waiting_weight)
        await message.answer("Запишите сегодняшнее значение веса (кг). Пример: 82.5")
        return

    if text in {"шаги"}:
        await state.set_state(InputState.waiting_steps)
        await message.answer("Введите количество шагов за день. Пример: 8500")
        return

    if text in {"тренировка"}:
        await state.set_state(InputState.waiting_training)
        await message.answer("Опишите тренировку и длительность. Пример: силовая 45 минут")
        return

    if text in {"синхронизировать fatsecret", "fatsecret"}:
        await message.answer(
            "Запускаю загрузку данных из FatSecret. "
            "Будут подтянуты шаги и другие доступные метрики. "
            "Остальные данные можно внести вручную."
        )
        # TODO: тут позже вызовешь сервис FatSecret и пришлёшь результат пользователю
        return

    if text in {"отчет недели", "отчёт недели", "отчет"}:
        await message.answer(
            "Еженедельный отчет пока формируется вручную. "
            "В MVP здесь появится автоматический отчет."
        )
        return

    if text in {"помощь", "help"}:
        await message.answer("Используйте кнопки меню, чтобы внести вес, шаги или тренировку.")
        return

    # Если пользователь в состоянии (ждём ввод) — сюда он не должен попадать,
    # потому что его перехватят хендлеры ниже по StateFilter(...)
    # Если состояния нет — отработает fallback в конце файла.


@router.message(StateFilter(InputState.waiting_weight))
async def save_weight(message: Message, state: FSMContext):
    raw = (message.text or "").strip().replace(",", ".")
    try:
        weight = float(raw)
    except Exception:
        await message.answer("Введите число. Пример: 82.5")
        return

    # TODO: тут позже сохраняй в БД/файл
    await message.answer(f"✅ Вес сохранён: {weight} кг\nОтличное начало дня 💪")
    await state.clear()


@router.message(StateFilter(InputState.waiting_steps))
async def save_steps(message: Message, state: FSMContext):
    raw = (message.text or "").strip().replace(" ", "")
    if not raw.isdigit():
        await message.answer("Введите целое число. Пример: 8500")
        return

    steps = int(raw)

    # TODO: тут позже сохраняй в БД/файл
    pretty = f"{steps:,}".replace(",", " ")
    await message.answer(f"✅ Шаги сохранены: {pretty}\nЭто мощно, так держать 🔥")
    await state.clear()


@router.message(StateFilter(InputState.waiting_training))
async def save_training(message: Message, state: FSMContext):
    training = (message.text or "").strip()
    if not training:
        await message.answer("Напишите текстом. Пример: силовая 45 минут")
        return

    # TODO: тут позже сохраняй в БД/файл
    await message.answer(f"✅ Тренировка сохранена:\n{training}\nКруто 💪")
    await state.clear()


@router.message(StateFilter(None))
async def fallback(message: Message, state: FSMContext):
    await message.answer("Не понял сообщение. Пожалуйста, используйте кнопки меню.")
