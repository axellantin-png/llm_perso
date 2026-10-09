let currentConversationId = null;

async function sendMessage(){

    const input =
        document.getElementById(
            "messageInput"
        );


    const message = input.value;


    if(!message || !currentConversationId){
        return;
    }


    input.value = "";


    addMessage(
        "user",
        message
    );


    const response = await fetch(
        `/chat/${currentConversationId}`,
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(
                {
                    message:message
                }
            )
        }
    );


    const reader =
        response.body.getReader();


    const decoder =
        new TextDecoder();


    let assistantMessage =
        "";


    addMessage(
        "assistant",
        ""
    );


    const chat =
        document.getElementById(
            "chat"
        );


    const lastMessage =
        chat.lastElementChild;



    while(true){

        const {
            done,
            value
        } = await reader.read();


        if(done){
            break;
        }


        const chunk =
            decoder.decode(
                value
            );


        assistantMessage += chunk;


        lastMessage.innerHTML =
        `
        <b>assistant</b> :
        ${assistantMessage}
        `;

    }

}

async function deleteConversation(id){

    if(!confirm("Supprimer ?")){
        return;
    }


    await fetch(
        `/conversation/${id}`,
        {
            method:"DELETE"
        }
    );


    if(currentConversationId===id){

        currentConversationId=null;

        document
        .getElementById("chat")
        .innerHTML="";
    }


    loadConversations();

}

async function renameConversation(id){

    const title =
        prompt(
            "Nouveau nom"
        );


    if(!title){
        return;
    }


    await fetch(
        `/conversation/${id}`,
        {
            method:"PATCH",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                title:title
            })
        }
    );


    loadConversations();

}

async function loadConversations() {
    try {
        const response = await fetch("/conversations");
        if (!response.ok) throw new Error("Erreur lors de la récupération des conversations");
        
        const conversations = await response.json();
        const container = document.getElementById("conversationList");
        
        container.innerHTML = "";

        conversations.forEach(conversation => {
            const item = document.createElement("div");
            item.className = "conversation-item"; // Optionnel : pour vos styles CSS

            item.innerHTML = `
                <span>${conversation.title}</span>
                <button class="rename">✏️</button>
                <button class="delete">🗑️</button>
            `;

            // Clic sur toute la ligne pour ouvrir la conversation
            item.onclick = () => {
                openConversation(conversation.id);
            };

            // Clic sur le bouton renommer
            item.querySelector(".rename").onclick = (event) => {
                event.stopPropagation(); // Empêche d'ouvrir la conversation en cliquant sur le bouton
                renameConversation(conversation.id);
            };

            // Clic sur le bouton supprimer
            item.querySelector(".delete").onclick = (event) => {
                event.stopPropagation(); // Empêche d'ouvrir la conversation en cliquant sur le bouton
                deleteConversation(conversation.id);
            };

            // On ajoute l'item (la ligne entière) au conteneur
            container.appendChild(item);
        });
    } catch (error) {
        console.error("Erreur:", error);
    }
}

async function createConversation(){

    const response = await fetch(
        "/conversation",
        {
            method:"POST"
        }
    );


    const conversation =
        await response.json();


    currentConversationId =
        conversation.id;


    document
    .getElementById("chat")
    .innerHTML="";


    await loadConversations();


    openConversation(
        conversation.id
    );

}

async function openConversation(id){

    currentConversationId=id;


    const response =
        await fetch(
            `/conversation/${id}`
        );


    const conversation =
        await response.json();


    displayConversation(
        conversation
    );

}

function addMessage(
    role,
    content
){

    const chat =
        document.getElementById(
            "chat"
        );


    const div =
        document.createElement(
            "p"
        );


    div.innerHTML =
    `
    <b>${role}</b> :
    ${content}
    `;


    chat.appendChild(
        div
    );


    chat.scrollTop =
        chat.scrollHeight;


}


function displayConversation(
    conversation
){

    const chat =
        document.getElementById(
            "chat"
        );


    chat.innerHTML="";


    conversation.messages.forEach(
        message=>{


            chat.innerHTML +=
            `
            <p>
            <b>${message.role}</b> :
            ${message.content}
            </p>
            `;


        }
    );

}



loadConversations();

document
.getElementById(
    "sendButton"
)
.onclick =
sendMessage;

document
.getElementById(
    "newConversation"
)
.onclick =
createConversation;


// --- LOGIQUE POUR L'UPLOAD DE FICHIER ---
const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("uploadButton");
const uploadStatus = document.getElementById("uploadStatus");

// Ouvre l'explorateur de fichiers quand on clique sur "Joindre"
uploadButton.onclick = () => {
    fileInput.click();
};

// Se déclenche quand un fichier est sélectionné
fileInput.onchange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    uploadStatus.textContent = `Upload en cours de ${file.name}...`;
    uploadButton.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/chat/upload-temp-document", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            uploadStatus.textContent = `✅ ${file.name} est prêt !`;
            
            // On peut ajouter un petit message visuel dans le chat
            if (currentConversationId) {
                addMessage("système", `Le document <b>${file.name}</b> a été analysé. Vous pouvez lui poser des questions !`);
            }
        } else {
            uploadStatus.textContent = `❌ Erreur lors de l'upload.`;
        }
    } catch (error) {
        console.error("Erreur d'upload:", error);
        uploadStatus.textContent = `❌ Erreur de connexion.`;
    } finally {
        uploadButton.disabled = false;
        // On réinitialise l'input pour pouvoir uploader le même fichier si besoin
        fileInput.value = ""; 
        
        // Efface le status après 5 secondes
        setTimeout(() => {
            if (uploadStatus.textContent.includes("✅")) {
                uploadStatus.textContent = "Aucun fichier sélectionné";
            }
        }, 5000);
    }
};