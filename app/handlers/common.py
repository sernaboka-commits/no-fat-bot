 from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards.main_menu import main_menu_keyboard

router = Router()


# ===== States (FSM) =====
class InputState(StatesGroup):
    waiting_weight = State()
    waiting_steps = State()
    waiting_workout = State()


# ===== /start =====
@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет! Я бот NoFAT.\n"
        "Я помогу вести вес, питание и активность.\n"
        "Выберите действие в меню ниже.",
        reply_markup=main_menu_keyboard(),
    )


# ===== Menu handler =====
@router.message()
async def handle_menu(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip().lower()

    # --- Buttons / commands ---
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

    # --- If user typed a number without being in state ---
    current_state = await state.get_state()
    if current_state is None and text.replace(",", ".").replace(".", "", 1).isdigit():
        await message.answer("Похоже, вы отправили число без выбора действия. Нажмите кнопку: Вес / Шаги / Тренировка.")
        return

    # --- Fallback ---
    await message.answer("Не понял сообщение. Пожалуйста, используйте кнопки меню.")


# ===== Weight input =====
@router.message(InputState.waiting_weight)
async def save_weight(message: Message, state: FSMContext):
    raw = (message.text or "").strip().replace(",", ".")
    try:
        weight = float(raw)
    except ValueError:
        await message.answer("Введите число, например: 82.5")
        return

    # TODO: сохранить в БД (позже)
    await message.answer(
        f"✅ Вес сохранён: {weight:g} кг\n"
        f"Отличное начало дня 💪",
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()


# ===== Steps input =====
@router.message(InputState.waiting_steps)
async def save_steps(message: Message, state: FSMContext):
    raw = (message.text or "").strip().replace(" ", "")
    if not raw.isdigit():
        await message.answer("Введите целое число, например: 8500")
        return

    steps = int(raw)

    # TODO: сохранить в БД (позже)
    pretty = f"{steps:,}".replace(",", " ")
    msg = (
        f"🔥 Шаги сохранены: {pretty}\n"
        f"Так держать!"
    )
    if steps >= 10000:
        msg += " Это больше дневной нормы, отлично 🔥"

    await message.answer(msg, reply_markup=main_menu_keyboard())
    await state.clear()


# ===== Workout input =====
@router.message(InputState.waiting_workout)
async def save_workout(message: Message, state: FSMContext):
    workout = (message.text or "").strip()
    if not workout:
        await message.answer("Напишите тренировку текстом. Пример: силовая 45 минут")
        return

    # TODO: сохранить в БД (позже)
    await message.answer(
        f"🏋️ Тренировка сохранена:\n{workout}\n\n"
        f"Хорошая работа 💪",
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()
