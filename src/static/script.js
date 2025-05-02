document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM carregado - Iniciando aplicação...");

    // --- Get DOM Elements ---
    const userInfoSection = document.getElementById("user-info-section");
    const quizSection = document.getElementById("quiz-section");
    const resultsSection = document.getElementById("results-section");
    const chatSection = document.getElementById("chat-section");
    const compareSection = document.getElementById("compare-section");
    const startQuizOption = document.getElementById("start-quiz-option");
    const compareProfilesOption = document.getElementById("compare-profiles-option");
    
    console.log("Seções principais encontradas:", {
        userInfo: !!userInfoSection,
        quiz: !!quizSection,
        results: !!resultsSection,
        chat: !!chatSection,
        compare: !!compareSection
    });

    // ... (other elements)
    const summaryContainer = document.getElementById("summary-container");
    const accessCodeElement = document.getElementById("access-code");
    const chatWindow = document.getElementById("chat-window");
    const chatInput = document.getElementById("chat-input");
    const sendChatMessageButton = document.getElementById("send-chat-message");
    const userInfoForm = document.getElementById("user-info-form");
    const languageSelector = document.getElementById("language-selector");
    const nextQuestionButton = document.getElementById("next-question");
    const submitQuizButton = document.getElementById("submit-quiz");
    const chatOrionButton = document.getElementById("chat-orion");
    const shareSummaryButton = document.getElementById("share-summary");
    const downloadSummaryButton = document.getElementById("download-summary");
    const chatOrionNavButton = document.getElementById("chat-orion-option");
    const compatibilityBar = document.getElementById("compatibility-bar");
    const compatibilityLabel = document.getElementById("compatibility-label");
    const compatibilityFill = document.getElementById("compatibility-fill");

    console.log("Elementos do formulário encontrados:", {
        form: !!userInfoForm,
        languageSelector: !!languageSelector
    });

    // Elementos do formulário de comparação
    const compareForm = document.getElementById("compare-form");
    const comparisonResult = document.getElementById("comparison-result");

    // --- State Variables ---
    let currentQuestionIndex = 0;
    let quizQuestions = [];
    let userAnswers = {};
    let userNick = "";
    let userPhone = "";
    let currentLanguage = "pt";
    let currentTexts = {};
    let currentAccessCode = null;

    // --- Language Strings (including error messages) ---
    const languageStrings = {
        pt: {
            // ... (previous texts)
            shareLinkCopied: "Link de compartilhamento copiado para a área de transferência!",
            shareLinkError: "Não foi possível copiar o link. Copie manualmente:",
            // Add other share/export related texts if needed
            startTest: "Iniciar Teste",
            next: "Próxima",
            finish: "Finalizar",
            summaryTitle: "Seu Resumo Personalizado",
            accessCodeLabel: "Seu código de acesso:",
            share: "Compartilhar",
            download: "Baixar (PDF)",
            chatWithOrion: "Converse com Orion",
            chatTitle: "Converse com Orion",
            privacyNotice: "Aviso de Privacidade: Seus dados serão usados apenas para gerar seu perfil e permitir acesso futuro.",
            readMore: "Leia mais",
            nickLabel: "@Nick:",
            phoneLabel: "Telefone:",
            quizTitle: "Quiz",
            identificationTitle: "Identificação",
            chatInputPlaceholder: "Digite sua mensagem...",
            sendChat: "Enviar",
            orionTyping: "Orion está digitando...",
            alertFillFields: "Por favor, preencha o @Nick e o Telefone.",
            MISSING_NICK_PHONE: "Nick e telefone são obrigatórios.",
            FIELD_ALREADY_TAKEN: (field) => `O ${field === 'nick' ? 'nick' : 'telefone'} fornecido já está em uso.`, 
            INTERNAL_SERVER_ERROR: "Ocorreu um erro interno no servidor. Tente novamente mais tarde.",
            MISSING_RETRIEVAL_IDENTIFIER: "Forneça @nick e telefone OU código de acesso.",
            RESULT_NOT_FOUND: "Resultado não encontrado.",
            MISSING_QUIZ_DATA: "Dados do quiz incompletos (nick, telefone, respostas).",
            QUIZ_PROCESSING_FAILED: "Falha ao processar o quiz ou gerar o resumo. Tente novamente mais tarde.",
            MISSING_CHAT_DATA: "Dados do chat incompletos (nick, telefone, mensagem).",
            USER_NOT_FOUND: "Usuário não encontrado. Registre-se e complete o quiz primeiro.",
            SUMMARY_NOT_GENERATED: "Resumo do usuário ainda não foi gerado. Complete o quiz primeiro.",
            CHAT_PROCESSING_FAILED: "Falha ao processar sua mensagem no chat. Tente novamente mais tarde.",
            NO_ACTIVE_CHAT: "Nenhum histórico de chat ativo encontrado.",
            MISSING_ACCESS_CODE: "Código de acesso ausente.", // Added
            PDF_GENERATION_FAILED: "Falha ao gerar o PDF.", // Added
            GENERIC_ERROR: "Ocorreu um erro inesperado. Tente novamente.",
            QUIZ_LOADING_FAILED: "Falha ao carregar perguntas do quiz.",
            SELECT_ANSWER: "Por favor, selecione uma resposta.",
            generatingSummary: "Gerando seu resumo...",
            MISSING_ACCESS_CODES: "Por favor, insira ambos os códigos de acesso.",
            startQuiz: "Iniciar Quiz",
            compareProfiles: "Comparar Perfis",
            compareTitle: "Comparar Perfis",
            compareDescription: "Insira dois códigos de acesso para analisar a compatibilidade entre os perfis.",
            code1Label: "Código 1:",
            code2Label: "Código 2:",
            analyzeCompatibility: "Analisar Compatibilidade",
            generatingComparison: "Gerando análise de compatibilidade...",
            COMPARISON_FAILED: "Falha ao gerar a análise de compatibilidade. Tente novamente.",
            GEMINI_API_REQUEST_FAILED: "Falha ao processar a análise. Tente novamente mais tarde."
        },
        en: {
            // ... (previous texts)
            shareLinkCopied: "Share link copied to clipboard!",
            shareLinkError: "Could not copy link. Please copy manually:",
            // Add other share/export related texts if needed
            startTest: "Start Test",
            next: "Next",
            finish: "Finish",
            summaryTitle: "Your Personalized Summary",
            accessCodeLabel: "Your access code:",
            share: "Share",
            download: "Download (PDF)",
            chatWithOrion: "Chat with Orion",
            chatTitle: "Chat with Orion",
            privacyNotice: "Privacy Notice: Your data will only be used to generate your profile and allow future access.",
            readMore: "Read more",
            nickLabel: "@Nick:",
            phoneLabel: "Phone:",
            quizTitle: "Quiz",
            identificationTitle: "Identification",
            chatInputPlaceholder: "Type your message...",
            sendChat: "Send",
            orionTyping: "Orion is typing...",
            alertFillFields: "Please fill in @Nick and Phone.",
            MISSING_NICK_PHONE: "Nick and phone are required.",
            FIELD_ALREADY_TAKEN: (field) => `The provided ${field} is already in use.`,
            INTERNAL_SERVER_ERROR: "An internal server error occurred. Please try again later.",
            MISSING_RETRIEVAL_IDENTIFIER: "Please provide @nick and phone OR access code.",
            RESULT_NOT_FOUND: "Result not found.",
            MISSING_QUIZ_DATA: "Incomplete quiz data (nick, phone, answers).",
            QUIZ_PROCESSING_FAILED: "Failed to process quiz or generate summary. Please try again later.",
            MISSING_CHAT_DATA: "Incomplete chat data (nick, phone, message).",
            USER_NOT_FOUND: "User not found. Please register and complete the quiz first.",
            SUMMARY_NOT_GENERATED: "User summary has not been generated yet. Complete the quiz first.",
            CHAT_PROCESSING_FAILED: "Failed to process your chat message. Please try again later.",
            NO_ACTIVE_CHAT: "No active chat history found.",
            MISSING_ACCESS_CODE: "Missing access code.", // Added
            PDF_GENERATION_FAILED: "Failed to generate PDF.", // Added
            GENERIC_ERROR: "An unexpected error occurred. Please try again.",
            QUIZ_LOADING_FAILED: "Failed to load quiz questions.",
            SELECT_ANSWER: "Please select an answer.",
            generatingSummary: "Generating your summary...",
            MISSING_ACCESS_CODES: "Please enter both access codes.",
            startQuiz: "Start Quiz",
            compareProfiles: "Compare Profiles",
            compareTitle: "Compare Profiles",
            compareDescription: "Enter two access codes to analyze the compatibility between profiles.",
            code1Label: "Code 1:",
            code2Label: "Code 2:",
            analyzeCompatibility: "Analyze Compatibility",
            generatingComparison: "Generating compatibility analysis...",
            COMPARISON_FAILED: "Failed to generate compatibility analysis. Please try again.",
            GEMINI_API_REQUEST_FAILED: "Failed to process analysis. Please try again later."
        }
    };

    // --- Language Handling ---
    languageSelector.addEventListener("click", (event) => {
        console.log("Clique no seletor de idioma detectado");
        if (event.target.tagName === "BUTTON") {
            const lang = event.target.getAttribute("data-lang");
            console.log("Botão de idioma clicado:", {
                elemento: event.target,
                idioma: lang,
                idiomaAtual: currentLanguage
            });
            
            if (lang && lang !== currentLanguage) {
                console.log(`Mudando idioma de ${currentLanguage} para ${lang}`);
                currentLanguage = lang;
                updateTextsForLanguage(currentLanguage);
                if (quizSection.style.display === "block") {
                    displayQuestion(currentQuestionIndex);
                }
            }
        }
    });

    function updateTextsForLanguage(lang) {
        currentTexts = languageStrings[lang] || languageStrings["pt"];
        
        // Botões de opção
        document.getElementById("start-quiz-option").textContent = currentTexts.startQuiz;
        document.getElementById("compare-profiles-option").textContent = currentTexts.compareProfiles;
        
        // Seção de comparação
        document.querySelector("#compare-section h2").textContent = currentTexts.compareTitle;
        document.querySelector("#compare-section p").textContent = currentTexts.compareDescription;
        document.querySelector("label[for=\"code1\"]").textContent = currentTexts.code1Label;
        document.querySelector("label[for=\"code2\"]").textContent = currentTexts.code2Label;
        document.querySelector("#compare-form button[type=\"submit\"]").textContent = currentTexts.analyzeCompatibility;

        // Textos existentes
        document.querySelector("#user-info-form button[type=\"submit\"]").textContent = currentTexts.startTest;
        document.getElementById("next-question").textContent = currentTexts.next;
        document.getElementById("submit-quiz").textContent = currentTexts.finish;
        document.querySelector("#results-section h2").textContent = currentTexts.summaryTitle;
        const accessCodeLabelNode = document.querySelector("#results-section p").childNodes[0];
        if (accessCodeLabelNode && accessCodeLabelNode.nodeType === Node.TEXT_NODE) {
            accessCodeLabelNode.nodeValue = currentTexts.accessCodeLabel + " ";
        }
        shareSummaryButton.textContent = currentTexts.share;
        downloadSummaryButton.textContent = currentTexts.download;
        chatOrionButton.textContent = currentTexts.chatWithOrion;
        document.querySelector("#chat-section h2").textContent = currentTexts.chatTitle;
        const privacyNoticeNode = document.querySelector("footer p").childNodes[0];
        if (privacyNoticeNode && privacyNoticeNode.nodeType === Node.TEXT_NODE) {
            privacyNoticeNode.nodeValue = currentTexts.privacyNotice + " ";
        }
        document.querySelector("footer a").textContent = currentTexts.readMore;
        document.querySelector("label[for=\"nick\"]").textContent = currentTexts.nickLabel;
        document.querySelector("label[for=\"telefone\"]").textContent = currentTexts.phoneLabel;
        document.querySelector("#quiz-section h2").textContent = currentTexts.quizTitle;
        document.querySelector("#user-info-section h2").textContent = currentTexts.identificationTitle;
        document.querySelector("header h1").textContent = "Orion Quiz Interativo";
        chatInput.placeholder = currentTexts.chatInputPlaceholder;
        sendChatMessageButton.textContent = currentTexts.sendChat;
        
        return currentTexts;
    }

    function getErrorMessage(errorData) {
        const errorKey = errorData?.error_key || "GENERIC_ERROR";
        const messageOrFn = currentTexts[errorKey] || currentTexts["GENERIC_ERROR"];
        if (typeof messageOrFn === 'function') {
            return messageOrFn(errorData.field);
        }
        return messageOrFn;
    }

    // Função para mostrar uma seção e esconder as outras
    function showSection(sectionToShow) {
        // Esconde todas as seções
        userInfoSection.style.display = "none";
        quizSection.style.display = "none";
        resultsSection.style.display = "none";
        chatSection.style.display = "none";
        
        // Mostra a seção desejada
        if (sectionToShow) {
            sectionToShow.style.display = "block";
            console.log("Mostrando seção:", sectionToShow.id);
        }
    }

    // --- Event Listeners ---
    userInfoForm.addEventListener("submit", (e) => {
        e.preventDefault();
        userNick = document.getElementById("nick").value.trim();
        userPhone = document.getElementById("telefone").value.trim();
        if (!userNick || !userPhone) {
            alert(currentTexts.alertFillFields);
            return;
        }
        userInfoSection.style.display = "none";
        document.getElementById("main-nav-options").style.display = "none";
        compareSection.style.display = "none";
        quizSection.style.display = "block";
        loadQuizQuestions();
    });

    nextQuestionButton.addEventListener("click", () => {
        // ... (same as before)
        if (saveAnswer()) {
            currentQuestionIndex++;
            if (currentQuestionIndex < quizQuestions.length) {
                displayQuestion(currentQuestionIndex);
            } else {
                console.error("Reached end of questions unexpectedly.");
            }
        }
    });

    submitQuizButton.addEventListener("click", async () => {
        // ... (same as before, but store access code)
        if (saveAnswer()) {
            console.log("Quiz finished. Answers:", userAnswers);
            showSection(resultsSection);
            summaryContainer.textContent = currentTexts.generatingSummary || "Gerando seu resumo...";
            accessCodeElement.textContent = "...";
            currentAccessCode = null; // Reset access code
            compatibilityBar.style.display = "none";
            try {
                const response = await fetch("/api/quiz/submit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ nick: userNick, telefone: userPhone, answers: userAnswers, language: currentLanguage }),
                });
                const result = await response.json();
                if (!response.ok) {
                    throw result;
                }
                console.log("Summary received:", result);
                summaryContainer.textContent = result.summary;
                accessCodeElement.textContent = result.access_code;
                currentAccessCode = result.access_code; // Store the received access code
                // Exibir compatibilidade
                if (typeof result.compatibility === 'number') {
                    compatibilityBar.style.display = "block";
                    compatibilityLabel.textContent = `Compatibilidade com Orion: ${result.compatibility}%`;
                    compatibilityFill.style.width = result.compatibility + "%";
                } else {
                    compatibilityBar.style.display = "none";
                }
            } catch (errorData) {
                console.error("Failed to get summary:", errorData);
                summaryContainer.textContent = getErrorMessage(errorData);
                accessCodeElement.textContent = "N/A";
                compatibilityBar.style.display = "none";
            }
        }
    });

    chatOrionButton.addEventListener("click", () => {
        // ... (same as before)
        showSection(chatSection);
    });

    sendChatMessageButton.addEventListener("click", sendChatMessage);
    chatInput.addEventListener("keypress", (event) => {
        // ... (same as before)
        if (event.key === "Enter") {
            sendChatMessage();
        }
    });

    // --- Share and Download Button Listeners ---
    downloadSummaryButton.addEventListener("click", () => {
        if (currentAccessCode) {
            // Trigger download by navigating to the PDF export URL
            window.location.href = `/api/export/pdf/${currentAccessCode}`;
        } else {
            console.error("Access code not available for PDF download.");
            // Optionally show an error message to the user
        }
    });

    shareSummaryButton.addEventListener("click", async () => {
        if (currentAccessCode) {
            const shareUrl = `${window.location.origin}/view/${currentAccessCode}`;
            try {
                // Use Clipboard API if available (requires HTTPS or localhost)
                if (navigator.clipboard && window.isSecureContext) {
                    await navigator.clipboard.writeText(shareUrl);
                    alert(currentTexts.shareLinkCopied || "Link copied!");
                } else {
                    // Fallback for insecure contexts or older browsers
                    prompt(currentTexts.shareLinkError || "Could not copy link. Please copy manually:", shareUrl);
                }
            } catch (err) {
                console.error("Failed to copy share link:", err);
                prompt(currentTexts.shareLinkError || "Could not copy link. Please copy manually:", shareUrl);
            }
        } else {
            console.error("Access code not available for sharing.");
            // Optionally show an error message to the user
        }
    });

    // --- Chat Functions ---
    async function sendChatMessage() {
        // ... (same as before)
        const messageText = chatInput.value.trim();
        if (!messageText) return;
        displayChatMessage(messageText, "user");
        chatInput.value = "";
        showTypingIndicator(true);
        try {
            const response = await fetch("/api/chat/message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nick: userNick, telefone: userPhone, message: messageText }),
            });
            const result = await response.json();
            showTypingIndicator(false);
            if (!response.ok) {
                throw result;
            }
            displayChatMessage(result.reply, "orion");
        } catch (errorData) {
            console.error("Failed to send/receive chat message:", errorData);
            showTypingIndicator(false);
            displayChatMessage(getErrorMessage(errorData), "system");
        }
    }

    function displayChatMessage(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.className = `chat-message ${sender}-message`;
        messageElement.textContent = text;
        messageElement.setAttribute('data-sender', sender === 'user' ? userNick : 'Orion');
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showTypingIndicator(show) {
        const typingIndicator = document.getElementById("typing-indicator");
        if (typingIndicator) {
            typingIndicator.style.display = show ? "block" : "none";
            if (show) {
                typingIndicator.innerHTML = `<span class="typing-animation">${currentTexts.orionTyping || "Orion está digitando"}</span>`;
            }
        }
    }

    async function loadQuizQuestions() {
        try {
            const response = await fetch('/api/quiz/questions');
            if (!response.ok) {
                throw new Error('Falha ao carregar perguntas');
            }
            quizQuestions = await response.json();
            console.log('Perguntas carregadas:', quizQuestions);
            displayQuestion(currentQuestionIndex);
        } catch (error) {
            console.error('Erro ao carregar perguntas:', error);
            alert(currentTexts.QUIZ_LOADING_FAILED || 'Falha ao carregar perguntas do quiz.');
        }
    }

    function displayQuestion(index) {
        const questionContainer = document.getElementById('question-container');
        if (index >= quizQuestions.length) {
            console.error('Índice de pergunta inválido:', index);
            return;
        }

        const question = quizQuestions[index];
        questionContainer.innerHTML = `
            <p>${question.text}</p>
            <div class="answer-options">
                <label>
                    <input type="radio" name="answer" value="sim"> Sim
                </label>
                <label>
                    <input type="radio" name="answer" value="nao"> Não
                </label>
            </div>
        `;

        nextQuestionButton.style.display = index < quizQuestions.length - 1 ? 'inline-block' : 'none';
        submitQuizButton.style.display = index === quizQuestions.length - 1 ? 'inline-block' : 'none';
    }

    function saveAnswer() {
        const selectedAnswer = document.querySelector('input[name="answer"]:checked');
        if (!selectedAnswer) {
            alert(currentTexts.SELECT_ANSWER || 'Por favor, selecione uma resposta.');
            return false;
        }
        userAnswers[currentQuestionIndex] = selectedAnswer.value;
        return true;
    }

    // Mostrar seção de comparação
    compareSection.style.display = "block";

    // Gerenciar formulário de comparação
    compareForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const code1 = document.getElementById("code1").value.trim();
        const code2 = document.getElementById("code2").value.trim();

        if (!code1 || !code2) {
            alert(currentTexts.MISSING_ACCESS_CODES);
            return;
        }

        try {
            const response = await fetch("/api/compare-profiles", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ code1, code2 }),
            });

            const data = await response.json();
            
            if (response.ok) {
                comparisonResult.style.display = "block";
                comparisonResult.innerHTML = data.comparison;
            } else {
                alert(getErrorMessage(data));
            }
        } catch (error) {
            console.error("Erro ao comparar perfis:", error);
            alert(currentTexts.GENERIC_ERROR);
        }
    });

    // Inicializa os textos no idioma padrão
    updateTextsForLanguage(currentLanguage);

    // Exibe apenas as opções iniciais ao carregar
    userInfoSection.style.display = "none";
    quizSection.style.display = "none";
    resultsSection.style.display = "none";
    chatSection.style.display = "none";
    compareSection.style.display = "none";

    // Botão para iniciar quiz
    startQuizOption.addEventListener("click", () => {
        startQuizOption.classList.add("active");
        compareProfilesOption.classList.remove("active");
        userInfoSection.style.display = "block";
        compareSection.style.display = "none";
    });

    // Botão para comparar perfis
    compareProfilesOption.addEventListener("click", () => {
        compareProfilesOption.classList.add("active");
        startQuizOption.classList.remove("active");
        userInfoSection.style.display = "none";
        compareSection.style.display = "block";
    });

    // Botão para chat com Orion na tela inicial
    chatOrionNavButton.addEventListener("click", () => {
        userInfoSection.style.display = "none";
        quizSection.style.display = "none";
        resultsSection.style.display = "none";
        compareSection.style.display = "none";
        document.getElementById("main-nav-options").style.display = "none";
        chatSection.style.display = "block";
    });
});