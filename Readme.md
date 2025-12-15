# 🤖 Faq Helper • Chat

Um **assistente inteligente de perguntas frequentes (FAQ)** com interface de **chat**, desenvolvido em **Python + PyQt5**, utilizando **IA local** baseada em *Sentence Transformers* para entender perguntas semelhantes em linguagem natural.

O projeto foi pensado para uso **corporativo**, especialmente em contextos como **RH, TI, Financeiro ou Suporte Interno**, oferecendo uma experiência moderna, simples e eficiente.

---

## ✨ Funcionalidades

* 💬 Interface de chat moderna (estilo WhatsApp)
* 🤖 IA local com embeddings (Sentence Transformers)
* 🧠 Entendimento de perguntas semelhantes
* 🕒 Respostas com data e hora
* ⌨️ Envio com **ENTER** (Shift + Enter para nova linha)
* ✍️ Indicador **“🤖 digitando…”**
* 👋 Mensagem automática de boas-vindas
* 🌞 Saudação dinâmica (Bom dia / Boa tarde / Boa noite)
* 📋 Menu inicial com opções disponíveis (gerado a partir do `faq.json`)
* 🎨 Interface customizada com cores e balões de diálogo
* 🖥️ Aplicação desktop (Windows / Linux)

---

## 🧠 Como funciona a IA

* As perguntas do arquivo `faq.json` são convertidas em **vetores (embeddings)**
* A pergunta do usuário também é convertida em embedding
* O sistema calcula a **similaridade semântica**
* A resposta mais próxima é retornada
* Caso a similaridade seja baixa, o bot retorna uma mensagem padrão

Tudo roda **localmente**, sem dependência de APIs externas.

---

## 📂 Estrutura do Projeto

```
faq-helper/
│
├── main.py            # Aplicação principal
├── faq.json           # Base de perguntas e respostas
├── requirements.txt   # Dependências do projeto
├── README.md          # Documentação
```

---

## 🛠️ Requisitos

* Python **3.10+** (recomendado)
* Ambiente virtual (`venv`) recomendado

---

## 📦 Instalação

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/sarmanhodiego/faq-helper.git
cd faq-helper
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

Ativar:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Executar a aplicação

```bash
python main.py
```

Na primeira execução, o modelo de IA será baixado automaticamente.

---

## 📝 Configuração do FAQ

Edite o arquivo `faq.json` para adicionar ou alterar perguntas:

```json
{
  "pergunta": "Como posso solicitar férias?",
  "resposta": "Você deve solicitar férias com pelo menos 30 dias de antecedência."
}
```

O menu inicial do bot é **gerado automaticamente** a partir desse arquivo.

---

## 🎯 Casos de Uso

* Atendimento interno (RH, TI, Financeiro)
* FAQ corporativo offline
* Totens de atendimento
* Sistemas internos sem acesso à internet

---

## 🚀 Possíveis Evoluções

* 💾 Persistência de histórico (SQLite / JSON)
* 🔊 Resposta por voz (TTS)
* 🌙 Tema escuro / claro
* 🔢 Menu interativo por números
* 📦 Geração de executável (.exe)
* 👥 Multiusuário

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais e corporativos internos.

---

## 👨‍💻 Autor

Desenvolvido por **Diego Sarmanho**

Sinta-se à vontade para abrir *issues*, enviar *pull requests* ou sugerir melhorias 🚀
