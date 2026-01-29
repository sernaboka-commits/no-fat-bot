from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards.main_menu import main_menu_keyboard

router = Router()


class InputState(StatesGroup):
    waiting_weight = State()
    waiting_steps = State()
    waiting_workout = State()


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет! Я бот NoFAT.\n"
        "Я помогу вести вес, питание и активность.\n"
        "Выберите действие в меню ниже.",
        reply_markup=main_menu_keyboard(),
    )


# Меню работает ТОЛЬКО когда нет активного state
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
        await state.set_state(InputState.waiting_workout)
        await message.answer("Опишите тренировку и длительность. Пример: силовая 45 минут")
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
        await message.answer("Используйте кнопки меню, чтобы внести вес, шаги или тренировку.")
        return

    # Фоллбек для сообщений вне state
    await message.answer("Не понял сообщение. Пожалуйста, используйте кнопки меню.")


@router.message(StateFilter(InputState.waiting_weight))
async def handle_weight_input(message: Message, state: FSMContext) -> None:
    raw = (message.text or "").strip().replace(",", ".")
    try:
        weight = float(raw)
    except ValueError:
        await message.answer("Не похоже на число. Введите вес в кг, например: 82.5")
        return

    # здесь позже можно сохранять в БД / файл
    await state.update_data(weight=weight)

    await message.answer(f"Вес сохранён: {weight:g} кг\nОтличное начало дня 💪")
    await state.clear()


@router.message(StateFilter(InputState.waiting_steps))
async def handle_steps_input(message: Message, state: FSMContext) -> None:
    raw = (message.text or "").strip().replace(" ", "")
    if not raw.isdigit():
        await message.answer("Введите число шагов, например: 8500")
        return

    steps = int(raw)
    await state.update_data(steps=steps)

    # простая “похвала”
    if steps >= 10000:
        tail = "Это больше дневной нормы, так держать 🔥"
    else:
        tail = "Хорошо! Завтра попробуем чуть больше 🙂"

    await message.answer(f"Шаги сохранены: {steps:,}".replace(",", " ") + f"\n{tail}")
    await state.clear()


@router.message(StateFilter(InputState.waiting_workout))
async def handle_workout_input(message: Message, state: FSMContext) -> None:
    workout = (message.text or "").strip()
    if not workout:
        await message.answer("Напишите текстом тренировку, например: силовая 45 минут")
        return

    await state.update_data(workout=workout)

    await message.answer(f"Тренировка сохранена: {workout}\nКруто, ты в деле 💪")
    await state.clear()
