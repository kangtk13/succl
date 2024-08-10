import nest_asyncio
nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ContextTypes
)
import logging
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read the bot's API token from environment variables
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

if not API_TOKEN:
    raise ValueError("TELEGRAM_API_TOKEN environment variable not set")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🌟컬쳐캐피탈이란?🌟", callback_data='item1')],
        [InlineKeyboardButton("🌟리딩 시간🌟", callback_data='item2'), InlineKeyboardButton("🌟거래 시간🌟", callback_data='item3')],
        [InlineKeyboardButton("🌟입출금 시간🌟", callback_data='item4'), InlineKeyboardButton("🌟잔고 보정🌟", callback_data='item5')],
        [InlineKeyboardButton("🌟거래 수수료🌟", callback_data='item6'), InlineKeyboardButton("🌟긴급 연락🌟", callback_data='item7')],
        [InlineKeyboardButton("🌟입출금 페이다 접속🌟", callback_data='item8')],
        [InlineKeyboardButton("🌟사칭 관련 안내🌟", callback_data='item9')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('🔵아래 메뉴를 선택해주세요🔵', reply_markup=reply_markup)

# Button click response handler function
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.callback_query
        user_message = query.data

        # "Processing..." message update
        await query.answer(text="답변 처리중...", show_alert=False)

        # Actual response processing
        response_dict = {
            'item1': "컬쳐캐피탈은 두바이에 본사를 두고 각국에 서비스를 제공중인 글로벌 CFD 증권사입니다.\n\n"
                     "아래 링크를 통해 컬쳐캐피탈에 대한 모든 정보를 확인 할 수 있습니다.\n\n"
                     "신규분들은 아래 공지 꼭 확인부탁드립니다.\n\n"
                     "https://url.kr/snwz24",
            'item2': "📊주식 리딩\n오전 09:00~11:30\n오후 13:00~15:30\n\n"
                     "🇭🇰항셍 리딩\n오전 10:30~11:15\n\n"
                     "🇺🇸나스닥 리딩\n오후 16:00~17:00\n오후 22:30~23:30",
            'item3': "🪙코인 (가상화폐)\n24시간\n\n"
                     "🇺🇸US500 (S&P)\n07:05 ~ 익일 06:00\n※ 토요일 오전 05:00\n\n"
                     "🇺🇸US100 (나스닥)\n07:05 ~ 익일 06:00\n※ 토요일 오전 05:00\n\n"
                     "🇭🇰HKIND (항셍)\n10:20 ~ 13:00\n14:35 ~ 17:15\n18:20 ~ 익일 04:00\n※ 토요일 오전 04:00\n\n"
                     "💱외환 (통화쌍)\n06:01 ~ 토요일 05:55\n\n"
                     "🥇XAUUSD (금)\n07:01 ~ 익일 06:00\n※ 토요일 오전 05:55\n\n"
                     "🥈XAGUSD (은)\n07:01 ~ 익일 06:00\n※ 토요일 오전 05:55\n\n"
                     "☁️NGAS (가스)\n07:00 ~ 익일 06:00\n※ 토요일 오전 05:00\n\n"
                     "🇺🇸WTI (오일)\n07:05 ~ 익일 06:00\n※ 토요일 오전 05:00\n\n"
                     "🇬🇧BRENT (오일)\n10:05 ~ 익일 07:00\n금요일 09:05 ~ 토요일 06:00\n※ 토요일 오전 06:00",
            'item4': "💰입금💰\n월 오전 9시 ~ 토 오전 9시\n24시간 입금 가능합니다.\n\n"
                     "💰출금💰\n월 오전 9시 ~ 금 오후 9시\n주말, 공휴일 제외 출금 가능합니다.\n",
            'item5': "잔고와 크레딧이 마이너스인 경우\n담당자에게 잔고보정 요청바랍니다.\n\n"
                     "잔고보정 없이 예치 시 불이익은\n이용자에게 있습니다.\n\n"
                     "꼭! 유념해주시기 바랍니다.",
            'item6': "진입, 청산, 왕복 수수료 등...\n직접 차감되는 수수료가 없습니다.\n\n"
                     "스프레드값이 적용 되어 거래량에 따라\n유동적으로 변동됩니다.",
            'item7': "🎇컬쳐캐피탈 주용환 본부장🎇\n\n"
                     "☎ 010 - 7765 - 4473\n카카오톡 ID : cclyh\n\n"
                     "🎇컬쳐캐피탈 강태구 본부장🎇\n\n"
                     "☎ 010 - 9842 - 3772\n카카오톡 ID : ccl.kr\n\n"
                     "🟢텔레그램 24시간 채팅 채널🟢\n\n"
                     "https://t.me/culturecapital",
            'item8': "https://m.pay-da.co.kr/\n\n"
                     "플레이스토어, 앱스토어에서 Payda 검색\n전자지갑 사용으로 세금이 발생하지 않습니다.\n\n"
                     "입금 수수료 = 0원\n출금 수수료 = 500원\n\n"
                     "▼▼ 페이다 가이드 ▼▼\nhttps://url.kr/65t6vu",
            'item9': "컬쳐캐피탈을 사칭하여 증거금 편취 등...\n피해가 발생할 수 있는 상황이 발생하고 있습니다.\n\n"
                     "컬쳐캐피탈은 담당자 변경 전 미리 안내해드리고 있으며\n모르는 번호로 담당자가 변경되었다고 연락이 오신다면\n연락처 차단을 적극 권장 드립니다.\n\n"
                     "메타 트레이더를 이용하는 불법 업체로 인해\n피해 사례가 점차 증가하고 있습니다.\n\n"
                     "담당자 이름을 거론하며 ,손실복구, 교육, 담당자 변경 등\n프로그램 설치 권유, 가입 권유 연락이 오신다면\n연락처 차단과 함께 긴급 연락처로 연락주시면\n도움드리도록 하겠습니다."
        }

        response = response_dict.get(user_message, 'Unknown item')

        # Update the message with the response
        await query.edit_message_text(text=response)

        # Schedule resend_menu to be sent after 2 seconds
        await asyncio.sleep(2)
        await resend_menu(context.application.bot, update.effective_chat.id)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await query.edit_message_text(text="오류가 발생했습니다. 다시 시도해주세요.")

async def resend_menu(bot, chat_id: int) -> None:
    keyboard = [
        [InlineKeyboardButton("🌟컬쳐캐피탈이란?🌟", callback_data='item1')],
        [InlineKeyboardButton("🌟리딩 시간🌟", callback_data='item2'), InlineKeyboardButton("🌟거래 시간🌟", callback_data='item3')],
        [InlineKeyboardButton("🌟입출금 시간🌟", callback_data='item4'), InlineKeyboardButton("🌟잔고 보정🌟", callback_data='item5')],
        [InlineKeyboardButton("🌟거래 수수료🌟", callback_data='item6'), InlineKeyboardButton("🌟긴급 연락🌟", callback_data='item7')],
        [InlineKeyboardButton("🌟입출금 페이다 접속🌟", callback_data='item8')],
        [InlineKeyboardButton("🌟사칭 관련 안내🌟", callback_data='item9')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(chat_id=chat_id, text='🔵아래 메뉴를 선택해주세요🔵', reply_markup=reply_markup)

# Entry point for the bot
if __name__ == '__main__':
    asyncio.run(main())