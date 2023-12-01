#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.


import logging
from asyncio import sleep

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, MenuButton
from telegram.constants import DiceEmoji, MenuButtonType, ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

REPO_URL = "https://github.com/RoboRich00A16/volta-il-dado-bot"


async def play_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	user_throw = update.message.dice
	bot_throw = await update.message.reply_dice(emoji=user_throw.emoji)

	if bot_throw.dice.value < user_throw.value:
		message_body = "😁 {} - {} 🤖\nHai vinto tu"
	elif bot_throw.dice.value == user_throw.value:
		message_body = "🙂 {} - {} 🤖\nAbbiamo fatto lo stesso numero"
	elif bot_throw.dice.value > user_throw.value:
		message_body = "😔 {} - {} 🤖\nHo vinto io"
	else:
		message_body = "😵‍💫 {} - {} 🤖\nCosa è successo..."

	await sleep(4)

	await context.bot.send_message(
		update.effective_message.chat_id,
		text=message_body.format(user_throw.value, bot_throw.dice.value),
		reply_to_message_id=update.message.id
	)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""Send a message when the command /help is issued."""
	await update.message.reply_text(
		"\n".join(
			[
				"/help - Mostra questo messaggio",
				"/start - Riavvia il bot",
				"/repo - Visita la repository con il codice sorgente",
				"/hoops - 🏀"
			]
		)
	)


async def hoops_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_dice(emoji=DiceEmoji.BASKETBALL)


async def repo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(
		text="Questo gioco è open source e puoi trovare il codice sorgente qui:",
		reply_markup=InlineKeyboardMarkup(
			[[
				InlineKeyboardButton(
					"Repository su GitHub",
					url=REPO_URL)
			]]
		)
	)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(
		"*Gioco dei dadi*\nTocca il dado sulla tastiera per giocare contro il bot\.",
		parse_mode=ParseMode.MARKDOWN_V2,
		reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🎲")]])
	)


def main() -> None:
	"""Start the bot."""
	# Create the Application and pass it your bot's token.
	application = Application.builder().token("1937213116:AAFRzNy_Rj4BianiJvVN7Gjt5kdKcS6l33s").build()

	# on different commands - answer in Telegram
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("help", help_command))
	application.add_handler(CommandHandler("repo", repo_command))
	application.add_handler(CommandHandler("hoops", hoops_command))

	application.add_handler(MessageHandler(filters.Dice.DICE, play_dice))

	# Run the bot until the user presses Ctrl-C
	application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()
