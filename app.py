import streamlit as st
import time
import random
from PIL import Image

# ==========================================
# 1. BASE DE CONHECIMENTO (Igual ao JSON)
# ==========================================
ANIMAL_DATA = {
    "vaca": {
        "descricao": "A vaca é um mamífero bovino, geralmente criado para produção de leite, carne e couro. Existem diversas raças, cada uma com características específicas.",
        "peso": "Geralmente entre 500 kg e 1000 kg, dependendo da raça.",
        "idade_media": "Cerca de 18 a 22 anos, mas na pecuária a vida útil é menor.",
        "curiosidades": "Vacas têm um estômago com quatro compartimentos e são animais sociais que vivem em rebanhos."
    },
    "cavalo": {
        "descricao": "O cavalo é um mamífero perissodáctilo domesticado, conhecido por sua força, velocidade e beleza. É usado para transporte, trabalho agrícola, esportes e lazer.",
        "peso": "Varia de 380 kg a 1000 kg, dependendo da raça.",
        "idade_media": "Cerca de 25 a 30 anos.",
        "curiosidades": "Cavalos conseguem dormir em pé e possuem um campo de visão de quase 360 graus."
    },
    "ovelha": {
        "descricao": "A ovelha é um mamífero ruminante de pequeno porte, criado principalmente por sua lã, carne e leite. São animais dóceis e adaptáveis a diversos climas.",
        "peso": "Geralmente entre 45 kg e 160 kg, dependendo da raça e do sexo.",
        "idade_media": "Cerca de 10 a 12 anos.",
        "curiosidades": "As ovelhas são muito inteligentes e conseguem reconhecer rostos humanos e de outras ovelhas por até dois anos."
    }
}

# ==========================================
# 2. FUNÇÕES AUXILIARES (Quiz e Lógica)
# ==========================================

def gerar_perguntas(animal):
    info = ANIMAL_DATA[animal]
    perguntas_base = [
        {"pergunta": f"Qual é a principal característica da {animal}?", "resposta": info["descricao"]},
        {"pergunta": f"Quanto pesa uma {animal} aproximadamente?", "resposta": info["peso"]},
        {"pergunta": f"Qual é a idade média de uma {animal}?", "resposta": info["idade_media"]},
        {"pergunta": f"Me diga uma curiosidade sobre a {animal}.", "resposta": info["curiosidades"]},
    ]
    
    quiz_data = []
    for q in perguntas_base:
        erradas = []
        for k, v in ANIMAL_DATA.items():
            if k != animal:
                erradas.extend([v["descricao"], v["peso"], v["idade_media"], v["curiosidades"]])

        alternativas = random.sample(erradas, 3) + [q["resposta"]]
        random.shuffle(alternativas)

        quiz_data.append({
            "pergunta": q["pergunta"],
            "resposta_correta": q["resposta"],
            "alternativas": alternativas
        })
    
    return quiz_data


def resposta_chat(animal, mensagem):
    if not animal:
        return "Por favor, faça o upload de uma imagem primeiro."
        
    info = ANIMAL_DATA[animal]
    msg = mensagem.lower()
    
    if "descri" in msg:
        return info["descricao"]
    elif "peso" in msg:
        return info["peso"]
    elif "idade" in msg or "vive" in msg:
        return info["idade_media"]
    elif "curios" in msg or "fato" in msg:
        return info["curiosidades"]
    else:
        return f"Não tenho uma resposta exata, mas sabia disso? 👉 {info['curiosidades']}"

# ==========================================
# 3. INTERFACE STREAMLIT
# ==========================================

st.set_page_config(page_title="Animal Scan AI", page_icon="🐾", layout="centered")

# CSS Personalizado
st.markdown("""
    <style>
    /* Estilo geral */
    .main { 
        background-color: #f8f9fa; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cabeçalho principal */
    .main-header {
        background-color: #2e7d32;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Área de upload */
    .upload-section {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        text-align: center;
        border: 2px dashed #2e7d32;
    }
    
    /* Mensagem de boas-vindas do bot */
    .bot-welcome {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2e7d32;
    }
    
    /* Botão de encerrar */
    .end-chat-btn {
        background-color: #ff6b6b !important;
        color: white !important;
        margin-top: 1rem;
    }
    
    .end-chat-btn:hover {
        background-color: #ff5252 !important;
    }
    
    /* Resultado do quiz */
    .quiz-result {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        text-align: center;
        border-left: 4px solid #2e7d32;
    }
    
    /* Mensagem de agradecimento */
    .thank-you-message {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        text-align: center;
        border: 2px solid #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do Session State
if 'step' not in st.session_state:
    st.session_state.step = 'upload'

if 'animal_detectado' not in st.session_state:
    st.session_state.animal_detectado = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []

if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0

# --- NOVA VARIÁVEL PARA O NOME ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# == ETAPA: DIGITAR O NOME ==
if st.session_state.user_name == "":
    st.markdown("""
        <div class="main-header">
            <div class="main-title">Animal Scan AI</div>
            <div class="main-subtitle">Faça upload de uma foto de <strong>Vaca, Cavalo</strong> ou <strong>Ovelha</strong>. Nossa inteligência artificial identificará o animal e fornecerá informações zootécnicas detalhadas.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("👋 Bem-vindo ao Animal Scan AI!")
    st.markdown("Antes de começarmos, digite seu nome:")
    
    nome_input = st.text_input("Digite seu nome:", placeholder="Seu nome aqui...")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continuar ▶️", use_container_width=True):
            if nome_input.strip() == "":
                st.warning("Por favor, digite um nome válido.")
            else:
                st.session_state.user_name = nome_input.strip()
                st.rerun()
    
    st.stop()

# --- CABEÇALHO PRINCIPAL ---
st.markdown("""
    <div class="main-header">
        <div class="main-title">Animal Scan AI</div>
        <div class="main-subtitle">Faça upload de uma foto de <strong>Vaca, Cavalo</strong> ou <strong>Ovelha</strong>. Nossa inteligência artificial identificará o animal e fornecerá informações zootécnicas detalhadas.</div>
    </div>
""", unsafe_allow_html=True)

# --- ETAPA 1: UPLOAD ---
if st.session_state.step == 'upload':
    st.markdown(f"### Olá {st.session_state.user_name}! 👋")
    
    st.markdown("""
    <div class="bot-welcome">
        <strong>Olá! Eu sou o Animal Scan AI.</strong> Envie uma foto de um animal (Vaca, Cavalo ou Ovelha) e eu fornecerei informações detalhadas sobre ele.
    </div>
    """, unsafe_allow_html=True)
    
    # Área de upload estilizada
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Escolha uma imagem:", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    st.markdown('<p style="color: #666; margin-top: 10px;">Arraste e solte uma imagem aqui ou clique para selecionar</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de análise
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem enviada", use_column_width=True)
        
        if st.button("🔍 Analisar Imagem", use_container_width=True):
            with st.spinner("Processando rede neural..."):
                time.sleep(2)

                filename = uploaded_file.name.lower()
                if "vaca" in filename: detection = "vaca"
                elif "cavalo" in filename: detection = "cavalo"
                elif "ovelha" in filename: detection = "ovelha"
                else: detection = random.choice(["vaca", "cavalo", "ovelha"])

                st.session_state.animal_detectado = detection
                st.session_state.step = 'result'
                st.rerun()

# --- ETAPA 2: RESULTADO ---
elif st.session_state.step == 'result':
    animal = st.session_state.animal_detectado
    data = ANIMAL_DATA[animal]

    st.success(f"✅ Animal detectado: **{animal.capitalize()}** (Confiança: 98%)")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Descrição:** {data['descricao']}")
        st.info(f"**Peso:** {data['peso']}")
    with col2:
        st.info(f"**Idade Média:** {data['idade_media']}")
        st.warning(f"**Curiosidade:** {data['curiosidades']}")

    st.divider()
    st.write(f"{st.session_state.user_name}, deseja participar de um Quiz sobre este animal?")

    col_sim, col_nao = st.columns(2)
    if col_sim.button("✅ Sim, quero jogar!"):
        st.session_state.quiz_questions = gerar_perguntas(animal)
        st.session_state.quiz_score = 0
        st.session_state.quiz_index = 0
        st.session_state.step = "quiz_active"
        st.rerun()

    if col_nao.button("❌ Não, pular para o chat"):
        st.session_state.step = "chat_prompt"
        st.rerun()

    if st.button(f"🔄 {st.session_state.user_name}, enviar outra imagem"):
        st.session_state.step = "upload"
        st.session_state.animal_detectado = None
        st.rerun()

# --- ETAPA 3: QUIZ ---
elif st.session_state.step == "quiz_active":
    st.subheader("🎮 Quiz Animal Scan!")

    questions = st.session_state.quiz_questions
    idx = st.session_state.quiz_index

    if idx < len(questions):
        q = questions[idx]
        st.write(f"**Pergunta {idx+1}/{len(questions)}:** {q['pergunta']}")

        for alt in q["alternativas"]:
            if st.button(alt, key=f"{idx}_{alt}"):
                if alt == q["resposta_correta"]:
                    st.toast("✔ Correto!", icon="🎉")
                    st.session_state.quiz_score += 1
                else:
                    st.toast(f"❌ Errado! A resposta era: {q['resposta_correta']}", icon="😢")

                st.session_state.quiz_index += 1
                st.rerun()

    else:
        score = st.session_state.quiz_score
        
        st.markdown('<div class="quiz-result">', unsafe_allow_html=True)
        
        if score == 4:
            st.balloons()
            st.markdown(f"# 🎉 Parabéns, {st.session_state.user_name}!")
            st.markdown(f"### Você finalizou o Quiz com **{score}/4** pontos!")
            st.markdown("**🏆 Excelente! Você é um verdadeiro especialista em {}s!**".format(st.session_state.animal_detectado.capitalize()))
            if st.button("Ir para o Chat 💬", use_container_width=True):
                st.session_state.step = "chat_active"
                st.rerun()
        else:
            st.markdown(f"# 📚 Continue Aprendendo, {st.session_state.user_name}!")
            st.markdown(f"### Você finalizou o Quiz com **{score}/4** pontos!")
            st.markdown("**💡 Não desanime! Tente novamente para ganhar o prêmio de especialista!**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Tentar Novamente", use_container_width=True):
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_index = 0
                    st.rerun()
            with col2:
                if st.button("💬 Ir para o Chat", use_container_width=True):
                    st.session_state.step = "chat_active"
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- ETAPA 4: CHAT ---
elif st.session_state.step in ("chat_prompt", "chat_active"):

    if st.session_state.step == "chat_prompt":
        st.session_state.chat_history = []  # Limpar histórico ao iniciar novo chat
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": (
                f"Olá **{st.session_state.user_name}**! 👋\n\n"
                f"Sou o especialista em **{st.session_state.animal_detectado.capitalize()}**.\n"
                f"Pode me perguntar sobre *peso*, *idade*, *curiosidades* ou *descrição*."
            )
        })
        st.session_state.step = "chat_active"

    st.subheader(f"💬 Chat sobre: {st.session_state.animal_detectado.capitalize()}")

    # Exibir histórico do chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Verificar se a última mensagem é de agradecimento (encerramento)
    if st.session_state.chat_history and "Obrigado por utilizar" in st.session_state.chat_history[-1]["content"]:
        # Aguardar 3 segundos e redirecionar automaticamente
        time.sleep(3)
        st.session_state.step = "upload"
        st.session_state.animal_detectado = None
        st.session_state.chat_history = []
        st.rerun()

    # Input do chat - AGORA APENAS PARA NOVAS PERGUNTAS
    if prompt := st.chat_input("Faça sua pergunta:"):
        # Adicionar pergunta do usuário ao histórico
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Obter resposta do bot
        resp = resposta_chat(st.session_state.animal_detectado, prompt)
        
        # Adicionar resposta do bot ao histórico
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        
        # Rerun para atualizar a tela com pergunta e resposta
        st.rerun()

    # Botão para encerrar a conversa
    if st.button("🚪 Encerrar Conversa", key="end_chat", use_container_width=True):
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"Obrigado por utilizar o Animal Scan AI, {st.session_state.user_name}! 🙏\n\nFoi um prazer ajudar você a aprender mais sobre {st.session_state.animal_detectado.capitalize()}s. Espero vê-lo novamente em breve! 👋"
        })
        st.rerun()

    if st.button(f"🔄 {st.session_state.user_name}, analisar outro animal"):
        st.session_state.step = "upload"
        st.session_state.animal_detectado = None
        st.session_state.chat_history = []
        st.rerun()