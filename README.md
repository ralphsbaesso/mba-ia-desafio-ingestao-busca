# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema RAG (Retrieval-Augmented Generation) para ingestão e busca de documentos PDF, utilizando LangChain com PostgreSQL/pgvector para armazenamento vetorial.

## Arquitetura

O sistema é composto por três componentes principais:

1. **Pipeline de Ingestão** (`src/ingest.py`): Processa documentos PDF e armazena embeddings no PostgreSQL com pgvector
2. **Sistema de Busca** (`src/search.py`): Recupera contexto relevante do armazenamento vetorial usando busca por similaridade
3. **Interface de Chat** (`src/chat.py`): Fornece interface de chat que utiliza o sistema de busca para responder perguntas baseadas no contexto dos documentos

## Tecnologias

- **LangChain**: Framework para aplicações LLM
- **PostgreSQL + pgvector**: Banco de dados vetorial
- **Embeddings**: Suporte para Google Gemini e OpenAI
- **Processamento de Documentos**: pypdf para parsing de PDFs

## Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Chave de API do Google Gemini OU OpenAI

## Configuração do Ambiente

### 1. Clonar o Repositório

```bash
git clone <repository-url>
cd mba-ia-desafio-ingestao-busca
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e configure as variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
# Opção 1: Google Gemini (recomendado)
GOOGLE_API_KEY=sua-chave-aqui
GOOGLE_EMBEDDING_MODEL=models/embedding-001

# Opção 2: OpenAI (alternativo)
OPENAI_API_KEY=sua-chave-aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Configuração do Banco de Dados
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag

# Nome da coleção vetorial
PG_VECTOR_COLLECTION_NAME=documentos_pdf

# Caminho do PDF para ingestão
PDF_PATH=./documentos/seu-arquivo.pdf
```

### 3. Preparar Documento PDF

Coloque o arquivo PDF que deseja processar no diretório do projeto e atualize a variável `PDF_PATH` no arquivo `.env`.

## Como Executar

### IMPORTANTE: Ordem de Execução

O sistema requer que você execute os passos na seguinte ordem:

1. Iniciar o banco de dados PostgreSQL
2. Executar o pipeline de ingestão
3. Executar o chat interativo

### Opção 1: Usando Python Diretamente

#### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

#### Passo 2: Iniciar o Banco de Dados

```bash
docker-compose up -d
```

Aguarde alguns segundos para o banco inicializar completamente. Você pode verificar o status com:

```bash
docker-compose logs postgres
```

#### Passo 3: Executar a Ingestão

IMPORTANTE: Este passo deve ser executado ANTES de usar o chat. Ele processa o PDF e armazena os embeddings no banco de dados.

```bash
python src/ingest.py
```

O processo irá:
- Ler o PDF especificado em `PDF_PATH`
- Dividir o documento em chunks
- Gerar embeddings usando o modelo configurado
- Armazenar os vetores no PostgreSQL

#### Passo 4: Executar o Chat

Após a ingestão ser concluída com sucesso, inicie o chat interativo:

```bash
python src/chat.py
```

Digite suas perguntas e pressione Enter. O sistema irá:
- Buscar contexto relevante no banco vetorial
- Usar o LLM para gerar respostas baseadas no contexto
- Responder apenas com informações do documento (não inventa respostas)

Para sair do chat, digite `sair`, `exit` ou pressione `Ctrl+C`.

### Opção 2: Usando Task (Taskfile)

Se você tiver o [Task](https://taskfile.dev) instalado, pode usar os comandos simplificados:

#### Passo 1: Instalar Dependências

```bash
task setup
```

#### Passo 2: Iniciar o Banco de Dados

```bash
task up
```

#### Passo 3: Executar a Ingestão

```bash
task ingest
```

#### Passo 4: Executar o Chat

```bash
task chat
```

## Comandos Úteis

### Gerenciamento do Banco de Dados

```bash
# Parar o banco de dados
docker-compose down

# Parar e remover volumes (limpa todos os dados)
docker-compose down -v

# Ver logs do banco
docker-compose logs -f postgres

# Acessar o PostgreSQL via CLI
docker exec -it postgres-rag psql -U postgres -d rag
```

### Verificar Dados no Banco

```bash
# Conectar ao banco
docker exec -it postgres-rag psql -U postgres -d rag

# Listar coleções
SELECT name FROM langchain_pg_collection;

# Ver quantidade de embeddings
SELECT COUNT(*) FROM langchain_pg_embedding;
```

## Estrutura do Projeto

```
.
├── src/
│   ├── ingest.py          # Pipeline de ingestão de PDFs
│   ├── search.py          # Sistema de busca vetorial
│   └── chat.py            # Interface de chat interativo
├── docker-compose.yml     # Configuração do PostgreSQL
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
└── README.md             # Este arquivo
```

## Funcionamento do Sistema

### Pipeline de Ingestão

1. Lê o documento PDF especificado em `PDF_PATH`
2. Divide o texto em chunks usando RecursiveCharacterTextSplitter
3. Gera embeddings para cada chunk usando o modelo configurado
4. Armazena os embeddings no PostgreSQL com pgvector

### Sistema de Busca e Chat

1. Recebe a pergunta do usuário
2. Converte a pergunta em embedding
3. Busca os chunks mais similares no banco vetorial
4. Envia o contexto relevante para o LLM
5. Retorna a resposta baseada apenas no contexto fornecido

O sistema utiliza um prompt estrito que:
- Responde APENAS com base no contexto fornecido
- Retorna "Não tenho informações necessárias para responder sua pergunta." quando não há contexto suficiente
- Nunca inventa informações ou usa conhecimento externo

## Troubleshooting

### Erro de Conexão com o Banco

Se você receber erros de conexão, verifique:

1. O Docker está rodando: `docker ps`
2. O container do PostgreSQL está saudável: `docker-compose ps`
3. A `DATABASE_URL` no `.env` está correta

### Erro na Ingestão

Se a ingestão falhar:

1. Verifique se o arquivo PDF existe no caminho especificado
2. Confirme que a API key está configurada corretamente
3. Verifique os logs para mensagens de erro específicas

### Chat Retorna "Não tenho informações"

Isso significa que:

1. A ingestão pode não ter sido executada
2. A pergunta está fora do escopo do documento
3. O documento não contém informação relevante para a pergunta

