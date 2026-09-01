import discord
from discord.ext import commands
import random
import os



# Tenta importar a função do modelo local
try:
    from model import get_class
except ImportError as e:
    print(f"Erro ao importar 'model.py' ou dependências (TensorFlow/Pillow): {e}")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Informações adicionais sobre cada ave
info_aves = {
    "Pombo": "🕊️ **Pombo:** Muito comum em áreas urbanas. Alimenta-se de grãos e sementes.",
    "Pardal": "🐤 **Pardal:** Uma pequena ave urbana muito adaptável e presente em quase todo o mundo.",
    "Urubu": "🦅 **Urubu:** Ave de rapina fundamental para a limpeza do ecossistema, pois se alimenta de matéria orgânica.",
    "Papagaio": "🦜 **Papagaio:** Conhecido por sua plumagem colorida e alta capacidade de imitar sons."
}

frases = [
    "Respeite a fauna local e preserve o habitat das aves.",
    "Nunca alimente animais silvestres com comida industrializada.",
    "Mantenha a cidade limpa para evitar a proliferação desordenada de certas espécies."
]

dicas = [
    "Observe passarinhos sem incomodá-los.",
    "Plante árvores nativas para atrair aves da região.",
    "Evite usar sacos de lixo abertos para não atrair vetores de doenças."
]


@bot.command()
async def hello(ctx):
    await ctx.send("hello im bot")


@bot.command()
async def eco(ctx):
    await ctx.send(random.choice(frases))


@bot.command()
async def dica(ctx):
    await ctx.send("💡 Dica: " + random.choice(dicas))

@bot.command()
async def salvar(ctx):
    # Verifica se a função de IA foi carregada corretamente
    if get_class is None:
        await ctx.send("❌ O sistema de IA não está disponível. Verifique se o TensorFlow e o arquivo `model.py` estão configurados no servidor.")
        return

    if not ctx.message.attachments:
        await ctx.send("⚠️ Por favor, envie uma imagem junta com o comando `$salvar`!")
        return

    if not os.path.exists("imagens"):
        os.makedirs("imagens")

    for arquivo in ctx.message.attachments:
        caminho_imagem = f"imagens/{arquivo.filename}"
        await arquivo.save(caminho_imagem)

        try:
            classe_bruta, precisao = get_class(caminho_imagem)
            porcentagem = round(precisao * 100, 2)

            classe_limpa = classe_bruta.strip()
            if " " in classe_limpa:
                classe_limpa = classe_limpa.split(" ", 1)[1].strip()

            chave_busca = classe_limpa.lower()
            detalhes = info_aves.get(chave_busca, f"Ave identificada: **{classe_limpa}**")

            await ctx.send(
                f"🦅 **Análise da Ave pela IA:**\n"
                f"• **Espécie detectada:** {classe_limpa.capitalize()}\n"
                f"• **Confiança:** {porcentagem}%\n\n"
                f"{detalhes}"
            )
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao analisar a imagem: `{e}`")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    palavras = ["poluição", "lixo", "sujeira"]

    if any(p in message.content.lower() for p in palavras):
        await message.channel.send("🚫 Vamos cuidar do meio ambiente juntos! 💚")

    await bot.process_commands(message)



