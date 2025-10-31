import logging

from aiogram import Bot, Router, F
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery, ChatMember, Chat

router = Router()
logger = logging.getLogger(__name__)


# @router.message(F.chat.type == 'supergroup')
# async def delete_user_input_message_in_chat(message: Message, bot: Bot):
#     logger.info(msg='прошел в роут удаления сообщений в чате')
#     await bot.delete_message(chat_id=-1003293541701, message_id=message.message_id)


# @router.message(F.chat.type == 'private', F.text != '/start')
# async def delete_user_input_message(message: Message, bot: Bot):
#     logger.info(msg='прошел в роут удаления сообщений в приватном чате')
#     user_sent_message_id, user_chat_id = message.message_id, message.chat.id
#     await bot.delete_message(chat_id=user_chat_id, message_id=user_sent_message_id)


@router.callback_query(F.data == 'pagination')
async def process_empty_callback_data(callback: CallbackQuery):
    await callback.answer()


# @router.chat_member(F.chat.id == -1003293541701)
# async def check_test(chat_member: ChatMember, chat: Chat):
#     print(chat.model_dump_json(indent=4))
#     print('==============================')
#     print(chat_member.model_dump_json(indent=4))

# @router.my_chat_member()
# async def check_member(chat_mem: ChatMemberUpdated):
#     print(chat_mem.model_dump_json(indent=4))
