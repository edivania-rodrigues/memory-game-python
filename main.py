import random
import tkinter as tk

# criação da janela principal
janela = tk.Tk()
janela.title("Jogo da Memória")
janela.geometry("500x520")

# conjuntos possíveis de emojis
conjuntos_emojis = [
    ["🐶", "🐱", "🐸", "🐵"],
    ["🍎", "🍌", "🍓", "🍇"],
    ["🚀", "🪐", "🌙", "⭐"],
    ["⚽", "🏀", "🏈", "⚾"],
    ["🐼", "🐯", "🦊", "🐻"]
]


# função responsável por gerar as cartas do jogo
def gerar_cartas():
    emojis_escolhidos = random.choice(conjuntos_emojis)
    cartas = emojis_escolhidos * 2
    random.shuffle(cartas)
    return cartas


cartas = gerar_cartas()

botoes = []
primeira_carta = None
segunda_carta = None
tentativas = 0
verificando = False

# texto de status
status_label = tk.Label(janela, text="Encontre os pares!", font=("Arial", 14))
status_label.pack(pady=10)

# contador de tentativas
tentativas_label = tk.Label(janela, text="Tentativas: 0", font=("Arial", 12))
tentativas_label.pack(pady=5)

# frame que contém o tabuleiro
tabuleiro = tk.Frame(janela)
tabuleiro.pack(expand=True, fill="both")

# configuração das colunas
for i in range(4):
    tabuleiro.columnconfigure(i, weight=1)

# configuração das linhas
for i in range(2):
    tabuleiro.rowconfigure(i, weight=1)


# função para reiniciar o jogo
def reiniciar_jogo():
    global cartas, primeira_carta, segunda_carta, tentativas, verificando

    cartas = gerar_cartas()
    primeira_carta = None
    segunda_carta = None
    tentativas = 0
    verificando = False

    tentativas_label.config(text="Tentativas: 0")
    status_label.config(text="Encontre os pares!")

    for botao in botoes:
        botao.config(text="?", bg="white", state="normal")


# verifica se o jogador venceu
def verificar_vitoria():
    for botao in botoes:
        if botao["text"] == "?":
            return

    status_label.config(
        text=f"Parabéns! Você encontrou todos os pares em {tentativas} tentativas! 🎉"
    )


# compara as duas cartas escolhidas
def verificar_par():
    global primeira_carta, segunda_carta, verificando

    if cartas[primeira_carta] != cartas[segunda_carta]:
        botoes[primeira_carta].config(text="?")
        botoes[segunda_carta].config(text="?")
    else:
        botoes[primeira_carta].config(bg="#90EE90", state="disabled")
        botoes[segunda_carta].config(bg="#90EE90", state="disabled")

    primeira_carta = None
    segunda_carta = None
    verificando = False

    verificar_vitoria()


# função chamada ao clicar em uma carta
def revelar_carta(indice):
    global primeira_carta, segunda_carta, tentativas, verificando

    if verificando:
        return

    if botoes[indice]["text"] != "?":
        return

    botoes[indice]["text"] = cartas[indice]

    if primeira_carta is None:
        primeira_carta = indice

    elif segunda_carta is None and indice != primeira_carta:
        segunda_carta = indice
        tentativas += 1
        tentativas_label.config(text=f"Tentativas: {tentativas}")
        verificando = True
        janela.after(1000, verificar_par)


# criação das cartas (botões)
for i in range(len(cartas)):
    botao = tk.Button(
        tabuleiro,
        text="?",
        font=("Arial", 32),
        bg="white",
        command=lambda i=i: revelar_carta(i)
    )
    botao.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")
    botoes.append(botao)


# botão de reiniciar
botao_reiniciar = tk.Button(
    janela,
    text="Jogar Novamente",
    font=("Arial", 12),
    command=reiniciar_jogo
)
botao_reiniciar.pack(pady=20)

# loop principal da interface
janela.mainloop()