from search import search_prompt
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Chat interativo via terminal usando RAG com Gemini.
    Digite 'sair' ou 'stop' para encerrar.
    """
    print("=" * 60)
    print("Chat RAG - Sistema de Busca em Documentos")
    print("=" * 60)
    print("Inicializando sistema...")
    print()

    # Inicializar a chain de busca
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Sistema iniciado com sucesso!")
    print("Digite suas perguntas ou 'sair'/'stop' para encerrar.")
    print("=" * 60)
    print()

    # Loop interativo de perguntas e respostas
    while True:
        try:
            # Capturar pergunta do usuário
            pergunta = input("Você: ").strip()

            # Verificar comandos de saída
            if pergunta.lower() in ["sair", "stop", "exit", "quit"]:
                print("\nEncerrando o chat. Até logo!")
                break

            # Ignorar entradas vazias
            if not pergunta:
                continue

            # Processar pergunta através da chain RAG
            print("\nAssistente: ", end="", flush=True)

            try:
                resposta = chain.invoke(pergunta)
                print(resposta)
            except Exception as e:
                print(f"Erro ao processar pergunta: {e}")

            print()

        except KeyboardInterrupt:
            print("\n\nChat interrompido. Até logo!")
            break
        except EOFError:
            print("\n\nEncerrando o chat. Até logo!")
            break

if __name__ == "__main__":
    main()
