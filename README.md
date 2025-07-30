# 📚 Costruire un Chatbot con RAG e Strumenti Open Source
**Esempio mostrato durante il Webinar "Costruire un Chatbot con RAG e Strumenti Open Source"**

⚠️ **Nota Bene:**  
Questo progetto è stato realizzato a scopo dimostrativo per il webinar e **non è pensato per un utilizzo in produzione**.  

---

## 📌 Descrizione del Progetto
Il progetto mostra come costruire un **chatbot RAG (Retrieval Augmented Generation)** utilizzando strumenti **open source**.  
Il sistema sfrutta **[Ollama](https://ollama.ai)** come provider LLM per eseguire il modello **in locale**, integrato con **LangChain** per gestire il flusso RAG.  
I dati vengono indicizzati tramite **ChromaDB** come **vector store**, mentre l'interazione con il chatbot avviene tramite:  
- **API REST (Flask)** per le richieste al modello  
- **Interfaccia utente (Streamlit)** per una chat semplice e interattiva  

---

## 🔧 Struttura del Progetto

```
├── Chain/
│   ├── inference_endpoint.py    # Definisce la chain RAG e l'endpoint di inferenza
│   └── __init__.py              # Descrizione del package Chain
│
├── Config/
│   ├── ollama_config.py         # Gestione installazione e verifica modelli Ollama
│   ├── vector_database_config.py# Creazione e gestione del ChromaDB
│   ├── config_chatbot.py        # Pipeline di configurazione completa
│   ├── colors.py                # Utility per messaggi colorati in console
│   └── __init__.py              # Descrizione del package Config
│
├── Data/                        # Directory contenente i file sorgente (.txt, pdf o md) da indicizzare
│
├── chatbot_api_endpoint.py      # API Flask per interagire con il modello
├── app.py                       # Interfaccia Streamlit del chatbot
├── requirements.txt             # Dipendenze del progetto
```

---

## ⚙️ Requisiti

- **Python 3.10+**
- [Ollama](https://ollama.ai) (installato e aggiunto al PATH)
- Modelli Ollama (embedding e chat model)

---

## 📥 Installazione

### 1️⃣ Clonare il progetto
```bash
git clone https://github.com/DevDocentiELIS/AIWebinarChatBot.git
cd AIWebinarChatBot
```

### 2️⃣ Creare un ambiente virtuale e installare le dipendenze
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
```

### 3️⃣ Installare **Ollama**
Scaricare e installare [Ollama](https://ollama.ai).  
Verificare che sia disponibile:
```bash
ollama --version
```

### 4️⃣ Avviare i modelli necessari
Il progetto utilizza i modelli:
- **Embedding:** `nomic-embed-text:latest`
- **Chat LLM:** `mistral:latest` (può essere sostituito con `llama3.2:latest` o altri modelli compatibili con le risorse hardware a disposizione)

[Lista e caratteristiche dei modelli disponibili](https://ollama.com/library)

È possibile scaricarli manualmente:
```bash
ollama pull nomic-embed-text:latest
ollama pull mistral:latest
```

⚠️ **In alternativa**, la configurazione automatica si occuperà di scaricare i modelli se non presenti.

---

## ▶️ Avvio del Progetto

### 1️⃣ Avviare le API Flask
```bash
python chatbot_api_endpoint.py
```
Le API saranno disponibili su **http://localhost:5000/ask**

### 2️⃣ Avviare l’interfaccia Streamlit
In un **nuovo terminale**:
```bash
streamlit run app.py
```

L'interfaccia sarà disponibile su **http://localhost:8501**

---

## 🧠 Come Funziona

1. **Caricamento dei dati locali** (`Data/` - puoi inserire un certo numero di file .pdf, .txt o .md) → i file vengono suddivisi in chunk e convertiti in **embedding** tramite Ollama.
2. **Creazione del vector store** → i chunk indicizzati vengono salvati in **ChromaDB**.
3. **Configurazione LLM (ChatOllama)** → viene avviato un modello Ollama per rispondere alle domande.
4. **Esecuzione RAG Pipeline** → la query dell’utente viene arricchita con il contesto recuperato dal vector store.
5. **Interfaccia** → l’utente interagisce tramite API Flask o tramite l’interfaccia Streamlit.

- **Il file: config_chatbot.py** contiene le impostazioni relative al sistema, puoi modificarle in questa parte del file:

```
__CONFIG_PARAMS = {
    "embedding_model": "nomic-embed-text:latest",
    "chat_model": "mistral:latest",
    "data_source_path": os.path.join(__BASE_DIR, "Data"),
    "data_files_extension": "txt",
    "text_chunk_size": 1000,
    "text_chunks_overlap": 0,
    "vector_store_dir": "chatbot_vector_storage"
}
```


---

## 🔗 Endpoints Disponibili

### **POST /ask**
Richiesta:
```json
{
  "question": "Scrivi qui la tua domanda"
}
```

Risposta (streaming):
```
Risposta generata dal modello...
```

---

## 📦 Dipendenze Principali
📄 `requirements.txt` include:
- **langchain**, **langchain-ollama**, **langchain-chroma**
- **flask**, **flask-cors**, **streamlit**
- **torch**, **requests**, **unstructured**

---

## ⚠️ Avvertenze
🚨 **Questo progetto è solo a scopo dimostrativo.**
- Non è ottimizzato per produzione.
- Non include gestione avanzata degli errori o sicurezza.
- È pensato per mostrare l’integrazione RAG + Ollama + LangChain in modo semplice.
