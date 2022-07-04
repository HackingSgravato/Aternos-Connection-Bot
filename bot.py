import logging
from python_aternos import Client
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5547563695:AAEzdFD-h3B3cVhZRVOhmMJQyEA9frINIBg'

aternos = None
list_server = None
choosen_server = None
_username = None
_password = None


def start(update, context):
    update.message.reply_text('Ciao, digita /help per capirne di più.')



def help(update, context):
    update.message.reply_text('/username [username] per inserire il nome utente del tuo account aternos\n/password [password] per inserire la password del tuo account aternos\n/login per effettuare l\'accesso al tuo account aternos\n/on per accendere il tuo server aternos\n/off per spegnere il tuo server aternos\n/list per avere la tua lista server\n/select [numero] per selezionare il tuo server aternos nel caso in cui ne avessi più di uno')



def username(update, context):
    _username = " ".join(context.args)
    update.message.reply_text("Username inserito: " + _username)



def password(update, context):
    _password = " ".join(context.args)
    update.message.reply_text("Password inserita: " + _password)



def listcommand(update, context):
    counter = 0
    for server in list_server:
        update.message.reply_text('ID (numero) ' + counter)
        update.message.reply_text('Status ' + server.status)
        update.message.reply_text('Full address ' + server.address)
        counter = counter + 1
    update.message.reply_text('Ora digita /select [numero] per selezionare il server da gestire')


def echo(update, context):
    update.message.reply_text(update.message.text + '\ncomando non riconosciuto, digita /help per capirne di più.')



def error(update, context):
    logger.warning('Update "%s" ha causato l\'errore "%s"', update, context.error)



def login(update, context):
    update.message.reply_text(f'accedendo al tuo account aternos\nUsername: {_username}\nPassword: {_password}')
    aternos = Client.from_credentials(_username, _password)
    update.message.reply_text('accesso effettuato')
    list_server = aternos.list_servers()
    choosen_server = list_server[0]
    udpate.message.reply_text('il primo server nella tua lista server è stato selezionato, se vuoi cambiarlo digita /list')


def select(update, context):
    numero = " ".join(context.args)
    choosen_server = list_server[int(numero)]
    update.message.reply_text('Hai selezionato il server numero ' + numero)



def on(update, context):
    update.message.reply_text('accendendo il server')
    choosen_server.start()
    update.message.reply_text('Il server è online')



def off(update, context):
    update.message.reply_text('spegnendo il server')
    choosen_server.stop()
    update.message.reply_text('il server è offline')



def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("on", on))
    dp.add_handler(CommandHandler("off", off))
    dp.add_handler(CommandHandler("login", login)) 
    dp.add_handler(CommandHandler("select", select))
    dp.add_handler(CommandHandler("list", listcommand))
    dp.add_handler(CommandHandler("username", username))
    dp.add_handler(CommandHandler("password", password))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://peaceful-channel-islands-67705.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()