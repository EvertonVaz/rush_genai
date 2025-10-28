# 🎬 Locadora - Chatbot de Recomendação de Filmes

Sistema de chatbot inteligente que recomenda filmes usando RAG (Retrieval-Augmented Generation) com ChromaDB e Gemini 2.5.

## 📋 Funcionalidades

- **Recomendação de Filmes**: Busca semântica em base de dados de filmes usando embeddings
- **Gerenciamento de Favoritos**: Adicione, avalie e marque filmes como assistidos
- **Histórico Persistente**: Banco SQLite com histórico de conversas e resumos automáticos
- **Roteamento Inteligente**: Sistema que decide entre resposta casual ou sugestão de filme
- **Function Calling**: Integração com funções para manipular dados do usuário

## 🏗️ Arquitetura

### Componentes Principais

```
rush_genai/
├── main.py              # Interface Streamlit
├── process_json.py      # Processamento e busca vetorial (ChromaDB)
├── utils.py             # Funções auxiliares
└── chatbot/
    ├── chatbot.py       # Lógica de LLM (Gemini)
    ├── database.py      # Repositórios SQLAlchemy
    ├── models.py        # Modelos ORM
    ├── schemas.py       # Schemas Pydantic
    ├── prompts.py       # Geradores de prompt
    ├── func_declarations.py  # Declarações de function calling
    └── history_manager.py    # Gerenciador de histórico
```

### Stack Técnica

- **LLM**: Google Gemini 2.5 Flash Lite
- **Embeddings**: SentenceTransformer (paraphrase-multilingual-MiniLM-L12-v2)
- **Vector DB**: ChromaDB
- **Database**: SQLite + SQLAlchemy
- **Interface**: Streamlit
- **Validação**: Pydantic

## 🔄 Fluxo de Execução

1. **Input do Usuário** → Streamlit captura a mensagem
2. **Roteamento** → `choose_assistant()` classifica como `friendly` ou `movie_suggestion`
3. **Busca Vetorial** (se movie_suggestion) → ChromaDB retorna 3 filmes similares
4. **Geração de Resposta** → Gemini gera resposta contextualizada
5. **Function Calling** (opcional) → Executa ações (adicionar favorito, avaliar, etc.)
6. **Persistência** → Salva no histórico; a cada 10 mensagens gera resumo

## 🚀 Como Usar

### Pré-requisitos

```bash
# Variáveis de ambiente (.env)
GOOGLE_GENAI_API_KEY=sua_chave_aqui
```

### Instalação

```bash
# Instalar dependências (via poetry ou pip)
poetry install
# ou
pip install -r requirements.txt
```

### Executar

```bash
streamlit run main.py
```

## 📊 Banco de Dados

### Tabelas SQLite

- **messages**: Histórico de mensagens (user/assistant)
- **summaries**: Resumos automáticos a cada 10 mensagens
- **favorites**: Filmes favoritos, notas e status de assistido

### ChromaDB Collections

- **movies**: Embeddings de filmes (`movies.json`) com metadados completos

## 🎯 Exemplo de Uso

```
Usuário: "Quero um filme de ficção científica com robôs"
→ Roteador: movie_suggestion
→ ChromaDB: Busca 3 filmes similares
→ Gemini: Gera resposta com base nos filmes + histórico
→ Resposta: "Que tal 'Ex Machina'? É sobre IA e tem ótimas críticas..."

Usuário: "Adicione aos meus favoritos"
→ Function Call: add_to_favorites()
→ Resposta: "Filme adicionado aos favoritos ✅"
```

## 🔧 Configurações Importantes

### Embeddings
- Modelo: `paraphrase-multilingual-MiniLM-L12-v2`
- Cache de modelo para evitar recarregamento

### LLM
- **simple_model**: Roteamento (temp=0.0, JSON mode, sem thinking)
- **thinking_model**: Resposta final (temp=1.0, com function calling)

### Resumos Automáticos
- Acionado a cada 10 mensagens
- Máximo 120 palavras
- Armazenado em tabela separada

## 📝 Functions Disponíveis

- `get_favorites()`: Lista filmes favoritos
- `add_to_favorites(movie_id, titulo)`: Adiciona aos favoritos
- `set_rating(movie_id, rating)`: Define nota (0-10)
- `get_rating(movie_id)`: Consulta nota
- `set_watched(movie_id)`: Marca como assistido
- `check_watched(movie_id)`: Verifica se assistiu
- `exit()`: Encerra chatbot

## 🎨 Interface Streamlit

- Container de chat com altura fixa (300px)
- Exibe histórico de mensagens
- Spinner durante processamento
- Layout wide para melhor visualização

## ⚡ Otimizações

- **Cache de Embeddings**: Modelo carregado uma única vez
- **Medição de Tempo**: Decorator `@measure_time_execution`
- **ChromaDB Persistente**: Evita reprocessamento do JSON
- **Resumos Inteligentes**: Reduz contexto mantendo relevância

## 🐛 Tratamento de Erros

- Validação de entrada vazia
- Limpeza de markdown em respostas JSON
- Tratamento de JSONDecodeError
- Verificação de existência de filme antes de adicionar favorito

---

