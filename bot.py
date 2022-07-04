import logging
from discord_webhook import DiscordWebhook, DiscordEmbed
from python_aternos import Client
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5547563695:AAEzdFD-h3B3cVhZRVOhmMJQyEA9frINIBg'

aternos = None
choosen_server = None
_username = None
_password = None



def start(update, context):
    update.message.reply_text('Ciao, digita /help per capirne di più.')



def help(update, context):
    update.message.reply_text('/username [username] per inserire il nome utente del tuo account aternos\n/password [password] per inserire la password del tuo account aternos\n/login per effettuare l\'accesso al tuo account aternos\n/on per accendere il tuo server aternos\n/off per spegnere il tuo server aternos\n/list per avere la tua lista server con le dedicate informazioni\n/select [numero] per selezionare il tuo server aternos nel caso in cui ne avessi più di uno\n/status [numero] per avere lo status di un tuo server aternos\n/config [private token] per connettersi ad un server aternos e poterlo gestire senza inserire le credenziali, così che anche i tuoi amici possono utilizzare questo bot. Se vuoi avere un tuo private token digita /requestoken [ID Discord]')



def username(update, context):
    global _username
    _username = " ".join(context.args)
    update.message.reply_text("Username aggiornato: " + _username)



def password(update, context):
    global _password
    _password = " ".join(context.args)
    update.message.reply_text("Password aggiornata: " + _password)



def requestoken(update, context):
    discordid = " ".join(context.args)
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/993432214949863484/e3lFusJ2jZsiDiXevANQeuXae2sE_3PsMxKV7nUOP3P4Nngm2n0DEPaD4xZQ1KiWmk36')
    embed = DiscordEmbed(title='User request', description='private token request', color='03b2f8')
    embed.set_timestamp()
    embed.add_embed_field(name='Infos', value=f'{discordid} is requesting a private token')
    webhook.add_embed(embed)
    response = webhook.execute()
    update.message.reply_text('request submitted')



def configserver(update, context):
    token = str(" ".join(context.args))
    match token:
        case 'huzuniliteserver400100bi':
            presettedlogin(update, 'HackingSgravato', 'APK3PUH74xEdtbf')

        case _:
            update.message.reply_text('token non valido')



def presettedlogin(update, username, password):
    global aternos
    global choosen_server
    aternos = Client.from_credentials(username, password)
    update.message.reply_text('accesso effettuato')
    choosen_server = aternos.list_servers()[0]
    update.message.reply_text('il primo server nella tua lista server è stato selezionato, se vuoi cambiarlo digita /list')



def listcommand(update, context):
    counter = 0
    for server in aternos.list_servers():
        update.message.reply_text('ID (numero) ' + str(counter) + '\nStatus ' + server.status + '\nFull address ' + server.address)
        counter = counter + 1
    update.message.reply_text('Ora digita /select [numero] per selezionare il server da gestire')



def serverstatus(update, context):
    numero = int(" ".join(context.args))
    server = aternos.list_servers()[numero]
    update.message.reply_text(f'{server.address} || Status {server.status}')



def echo(update, context):
    update.message.reply_text(update.message.text + '\ncomando non riconosciuto, digita /help per capirne di più.')



def error(update, context):
    logger.warning('Update "%s" ha causato l\'errore "%s"', update, context.error)



def login(update, context):
    global aternos
    global choosen_server
    update.message.reply_text(f'accedendo al tuo account aternos\nUsername: {_username}\nPassword: {_password}')
    aternos = Client.from_credentials(_username, _password)
    update.message.reply_text('accesso effettuato')
    choosen_server = aternos.list_servers()[0]
    update.message.reply_text('il primo server nella tua lista server è stato selezionato, se vuoi cambiarlo digita /list')


def select(update, context):
    global choosen_server
    numero = " ".join(context.args)
    choosen_server = aternos.list_servers()[int(numero)]
    update.message.reply_text('Hai selezionato il server numero ' + numero)



def on(update, context):
    update.message.reply_text('accendendo il server. se sei impaziente e vuoi vedere lo status del server in questione puoi digitare /status [numero]')
    choosen_server.start()
    update.message.reply_text('Il server si sta avviando, per saperne di più /status [numero]')



def off(update, context):
    update.message.reply_text('spegnendo il server')
    choosen_server.stop()
    update.message.reply_text('il server si sta spegnendo, per saperne di più /status [numero]')



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
    dp.add_handler(CommandHandler("status", serverstatus))
    dp.add_handler(CommandHandler("requestoken", requestoken))
    dp.add_handler(CommandHandler("config", configserver))
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