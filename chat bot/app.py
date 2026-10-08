from flask import Flask, request, jsonify, render_template_string
import re
from datetime import datetime

app = Flask(__name__)

# ============================================================
# KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = {
    "Python": {
        "category": "Programming",
        "keywords": ["python", "python language", "python programming"],
        "answer": """
        Python is a high-level, interpreted programming language.
        It is popular because of its simple syntax and large collection
        of libraries. Python is widely used in AI, machine learning,
        data science, automation, web development and software development.
        """
    },

    "Artificial Intelligence": {
        "category": "AI & ML",
        "keywords": ["artificial intelligence", "ai", "what is ai"],
        "answer": """
        Artificial Intelligence (AI) is a field of computer science
        that focuses on creating systems capable of performing tasks
        that normally require human intelligence. Examples include
        speech recognition, image recognition, recommendation systems
        and intelligent chatbots.
        """
    },

    "Machine Learning": {
        "category": "AI & ML",
        "keywords": ["machine learning", "ml", "what is machine learning"],
        "answer": """
        Machine Learning is a branch of Artificial Intelligence where
        computers learn patterns from data and use those patterns to
        make predictions or decisions without being explicitly programmed
        for every situation.
        """
    },

    "Deep Learning": {
        "category": "AI & ML",
        "keywords": ["deep learning", "neural network", "neural networks"],
        "answer": """
        Deep Learning is a subfield of machine learning that uses
        artificial neural networks with multiple layers. It is commonly
        used for image recognition, speech recognition, natural language
        processing and computer vision.
        """
    },

    "Database": {
        "category": "Database",
        "keywords": ["database", "data storage", "database system"],
        "answer": """
        A database is an organized collection of data that can be
        stored, managed, searched and updated efficiently.
        Examples include MySQL, PostgreSQL, MongoDB and SQLite.
        """
    },

    "DBMS": {
        "category": "Database",
        "keywords": ["dbms", "database management system"],
        "answer": """
        DBMS stands for Database Management System.
        It is software used to create, store, manage and retrieve
        data from databases. Examples include MySQL, Oracle,
        PostgreSQL and SQL Server.
        """
    },

    "SQL": {
        "category": "Database",
        "keywords": ["sql", "structured query language"],
        "answer": """
        SQL stands for Structured Query Language.
        It is used to communicate with relational databases.
        Common SQL commands include SELECT, INSERT, UPDATE, DELETE,
        CREATE and ALTER.
        """
    },

    "MongoDB": {
        "category": "Database",
        "keywords": ["mongodb", "mongo db", "nosql"],
        "answer": """
        MongoDB is a NoSQL database that stores data in flexible,
        JSON-like documents. It is commonly used in modern web
        applications and Python-based systems.
        """
    },

    "HTML": {
        "category": "Web Development",
        "keywords": ["html", "hypertext markup language"],
        "answer": """
        HTML stands for HyperText Markup Language.
        It provides the basic structure of web pages using elements
        such as headings, paragraphs, images, links, tables and forms.
        """
    },

    "CSS": {
        "category": "Web Development",
        "keywords": ["css", "cascading style sheets"],
        "answer": """
        CSS stands for Cascading Style Sheets.
        It is used to control the appearance and layout of websites,
        including colors, fonts, spacing, animations and responsive design.
        """
    },

    "JavaScript": {
        "category": "Web Development",
        "keywords": ["javascript", "js"],
        "answer": """
        JavaScript is a programming language mainly used to make
        websites interactive. It can handle events, manipulate
        web page elements, validate forms and communicate with servers.
        """
    },

    "Flask": {
        "category": "Web Development",
        "keywords": ["flask", "python flask"],
        "answer": """
        Flask is a lightweight Python web framework.
        It can be used to create websites, REST APIs, dashboards
        and web applications.
        """
    },

    "Algorithm": {
        "category": "Computer Science",
        "keywords": ["algorithm", "algorithms"],
        "answer": """
        An algorithm is a step-by-step procedure used to solve
        a problem or perform a task. Examples include binary search,
        BFS, DFS, Dijkstra's algorithm and sorting algorithms.
        """
    },

    "Computer": {
        "category": "Computer Science",
        "keywords": ["computer", "computer system"],
        "answer": """
        A computer is an electronic device that accepts input,
        processes data, stores information and produces output.
        Major components include the CPU, memory, storage,
        input devices and output devices.
        """
    },

    "AI Chatbot": {
        "category": "AI & ML",
        "keywords": ["chatbot", "ai chatbot", "knowledge base chatbot"],
        "answer": """
        An AI chatbot is a software application that communicates
        with users using natural language. A chatbot can use rules,
        knowledge bases, machine learning or large language models
        to generate responses.
        """
    },

    "Computer Vision": {
        "category": "AI & ML",
        "keywords": ["computer vision", "image recognition", "image processing"],
        "answer": """
        Computer Vision is a field of AI that enables computers
        to understand and analyze images and videos.
        Applications include face recognition, object detection,
        medical imaging and autonomous vehicles.
        """
    }
}


# ============================================================
# CHAT STATISTICS
# ============================================================

stats = {
    "questions": 0,
    "known": 0,
    "unknown": 0
}


# ============================================================
# TEXT PROCESSING
# ============================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================================================
# CHATBOT ENGINE
# ============================================================

def get_response(user_message):

    cleaned = clean_text(user_message)

    # Greetings
    greetings = [
        "hi",
        "hello",
        "hey",
        "hai",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if cleaned in greetings:
        return {
            "answer": "Hello! 👋 I'm your Knowledge Base Assistant. What would you like to learn?",
            "topic": "General",
            "confidence": 100
        }

    # Thanks
    if cleaned in ["thanks", "thank you", "thankyou"]:
        return {
            "answer": "You're welcome! 😊 Feel free to ask me another question.",
            "topic": "General",
            "confidence": 100
        }

    # Search knowledge base
    best_topic = None
    best_score = 0

    user_words = set(cleaned.split())

    for topic, data in KNOWLEDGE_BASE.items():

        score = 0

        for keyword in data["keywords"]:

            keyword_clean = clean_text(keyword)

            # Exact phrase
            if keyword_clean in cleaned:
                score += 10

            # Word matching
            keyword_words = set(keyword_clean.split())
            common = user_words.intersection(keyword_words)

            score += len(common) * 2

        # Topic name matching
        topic_clean = clean_text(topic)

        if topic_clean in cleaned:
            score += 10

        if score > best_score:
            best_score = score
            best_topic = topic

    # Match found
    if best_topic and best_score >= 2:

        stats["known"] += 1

        confidence = min(98, 60 + best_score * 5)

        return {
            "answer": KNOWLEDGE_BASE[best_topic]["answer"].strip(),
            "topic": best_topic,
            "category": KNOWLEDGE_BASE[best_topic]["category"],
            "confidence": confidence
        }

    # No match
    stats["unknown"] += 1

    return {
        "answer": """
        I couldn't find a suitable answer in my current knowledge base.
        Try asking about Python, AI, Machine Learning, DBMS, SQL,
        MongoDB, HTML, CSS, Flask, Algorithms or Computer Vision.
        """.strip(),
        "topic": "Unknown",
        "category": "Unknown",
        "confidence": 0
    }


# ============================================================
# MAIN DASHBOARD
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>KnowledgeBase AI</title>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: #0b1120;
    color: #e5e7eb;
    min-height: 100vh;
}

/* ================= SIDEBAR ================= */

.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    height: 100vh;
    background: #111827;
    border-right: 1px solid #263244;
    padding: 25px 18px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 35px;
}

.logo-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
}

.logo h2 {
    font-size: 19px;
}

.logo span {
    color: #818cf8;
}

.menu-title {
    color: #64748b;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 20px 10px 10px;
}

.menu-item {
    padding: 13px 14px;
    margin: 5px 0;
    border-radius: 10px;
    cursor: pointer;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: 0.2s;
}

.menu-item:hover,
.menu-item.active {
    background: #1e293b;
    color: white;
}

.status {
    position: absolute;
    bottom: 25px;
    left: 18px;
    right: 18px;
    background: #172033;
    border: 1px solid #263244;
    border-radius: 12px;
    padding: 15px;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 7px;
}

/* ================= MAIN ================= */

.main {
    margin-left: 250px;
    padding: 30px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.page-title h1 {
    font-size: 28px;
    margin-bottom: 6px;
}

.page-title p {
    color: #64748b;
}

.time {
    color: #94a3b8;
    font-size: 14px;
}

/* ================= STAT CARDS ================= */

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 25px;
}

.card {
    background: #111827;
    border: 1px solid #263244;
    border-radius: 15px;
    padding: 20px;
}

.stat-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stat-info p {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 8px;
}

.stat-info h2 {
    font-size: 28px;
}

.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    background: #1e293b;
}

/* ================= CONTENT ================= */

.content {
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 20px;
}

/* ================= CHAT ================= */

.chat-card {
    height: 650px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.chat-header {
    padding: 20px;
    border-bottom: 1px solid #263244;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.bot-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.bot-avatar {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
}

.bot-info h3 {
    font-size: 15px;
}

.bot-info p {
    color: #22c55e;
    font-size: 12px;
    margin-top: 3px;
}

.chat-body {
    flex: 1;
    overflow-y: auto;
    padding: 22px;
}

.message {
    margin-bottom: 18px;
    display: flex;
    gap: 10px;
}

.message.user {
    justify-content: flex-end;
}

.message-content {
    max-width: 75%;
    padding: 13px 16px;
    border-radius: 14px;
    line-height: 1.6;
    font-size: 14px;
    white-space: pre-line;
}

.message.bot .message-content {
    background: #1e293b;
    border: 1px solid #293548;
}

.message.user .message-content {
    background: #4f46e5;
    color: white;
}

.message-meta {
    font-size: 10px;
    color: #64748b;
    margin-top: 5px;
}

/* ================= INPUT ================= */

.chat-input {
    padding: 18px;
    border-top: 1px solid #263244;
}

.input-box {
    display: flex;
    gap: 10px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 7px;
}

.input-box input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    color: white;
    padding: 10px;
    font-size: 14px;
}

.input-box button {
    border: none;
    background: #6366f1;
    color: white;
    border-radius: 9px;
    padding: 0 20px;
    cursor: pointer;
    font-weight: bold;
}

.input-box button:hover {
    background: #4f46e5;
}

/* ================= RIGHT PANEL ================= */

.panel {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.panel-card {
    background: #111827;
    border: 1px solid #263244;
    border-radius: 15px;
    padding: 20px;
}

.panel-card h3 {
    font-size: 15px;
    margin-bottom: 17px;
}

.topic-search {
    width: 100%;
    padding: 11px;
    border-radius: 9px;
    border: 1px solid #334155;
    background: #0f172a;
    color: white;
    outline: none;
    margin-bottom: 14px;
}

.topic {
    padding: 11px;
    border-radius: 8px;
    margin-bottom: 5px;
    background: #172033;
    cursor: pointer;
    font-size: 13px;
    transition: 0.2s;
}

.topic:hover {
    background: #263244;
}

.category {
    color: #818cf8;
    font-size: 11px;
    display: block;
    margin-top: 3px;
}

.quick-question {
    width: 100%;
    padding: 10px;
    margin-bottom: 8px;
    text-align: left;
    background: #172033;
    border: 1px solid #263244;
    color: #cbd5e1;
    border-radius: 8px;
    cursor: pointer;
}

.quick-question:hover {
    background: #263244;
    color: white;
}

/* ================= TYPING ================= */

.typing {
    display: none;
    padding: 10px 15px;
    color: #64748b;
    font-size: 12px;
}

.typing span {
    animation: blink 1.2s infinite;
}

@keyframes blink {
    0%, 80%, 100% {
        opacity: 0.2;
    }

    40% {
        opacity: 1;
    }
}

/* ================= RESPONSIVE ================= */

@media(max-width: 1000px) {

    .sidebar {
        width: 70px;
    }

    .logo h2,
    .menu-item span,
    .menu-title,
    .status {
        display: none;
    }

    .main {
        margin-left: 70px;
    }

    .stats {
        grid-template-columns: repeat(2, 1fr);
    }

    .content {
        grid-template-columns: 1fr;
    }
}

@media(max-width: 600px) {

    .main {
        padding: 15px;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .topbar {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
}

</style>

</head>


<body>

<!-- ================= SIDEBAR ================= -->

<div class="sidebar">

    <div class="logo">

        <div class="logo-icon">
            🧠
        </div>

        <h2>Knowledge<span>AI</span></h2>

    </div>


    <div class="menu-title">
        Workspace
    </div>


    <div class="menu-item active">
        <span>▦</span>
        <span>Dashboard</span>
    </div>


    <div class="menu-item">
        <span>💬</span>
        <span>Chat Assistant</span>
    </div>


    <div class="menu-item">
        <span>📚</span>
        <span>Knowledge Base</span>
    </div>


    <div class="menu-item">
        <span>📊</span>
        <span>Analytics</span>
    </div>


    <div class="menu-title">
        System
    </div>


    <div class="menu-item">
        <span>⚙</span>
        <span>Settings</span>
    </div>


    <div class="status">

        <span class="status-dot"></span>

        <span style="font-size:13px;">
            System Online
        </span>

    </div>

</div>


<!-- ================= MAIN ================= -->

<div class="main">

    <div class="topbar">

        <div class="page-title">

            <h1>Knowledge Base Dashboard</h1>

            <p>Intelligent information assistant</p>

        </div>

        <div class="time" id="time"></div>

    </div>


    <!-- ================= STATISTICS ================= -->

    <div class="stats">

        <div class="card stat-card">

            <div class="stat-info">

                <p>Knowledge Topics</p>

                <h2>{{ topics }}</h2>

            </div>

            <div class="stat-icon">
                📚
            </div>

        </div>


        <div class="card stat-card">

            <div class="stat-info">

                <p>Questions Asked</p>

                <h2 id="questions">0</h2>

            </div>

            <div class="stat-icon">
                💬
            </div>

        </div>


        <div class="card stat-card">

            <div class="stat-info">

                <p>Known Answers</p>

                <h2 id="known">0</h2>

            </div>

            <div class="stat-icon">
                ✓
            </div>

        </div>


        <div class="card stat-card">

            <div class="stat-info">

                <p>Unknown Questions</p>

                <h2 id="unknown">0</h2>

            </div>

            <div class="stat-icon">
                ?
            </div>

        </div>

    </div>


    <!-- ================= CONTENT ================= -->

    <div class="content">


        <!-- CHAT -->

        <div class="card chat-card">

            <div class="chat-header">

                <div class="bot-info">

                    <div class="bot-avatar">
                        🧠
                    </div>

                    <div>

                        <h3>Knowledge Base Assistant</h3>

                        <p>● Online</p>

                    </div>

                </div>

                <div style="font-size:12px;color:#64748b;">
                    Local AI
                </div>

            </div>


            <div class="chat-body" id="chatBody">

                <div class="message bot">

                    <div>

                        <div class="message-content">

                            Hello! 👋

                            I'm your Knowledge Base Assistant.

                            Ask me anything about the topics
                            available in my knowledge base.

                        </div>

                        <div class="message-meta">
                            KnowledgeAI • Now
                        </div>

                    </div>

                </div>

            </div>


            <div class="typing" id="typing">
                KnowledgeAI is thinking <span>● ● ●</span>
            </div>


            <div class="chat-input">

                <div class="input-box">

                    <input
                        id="messageInput"
                        type="text"
                        placeholder="Ask something..."
                        autocomplete="off"
                    >

                    <button onclick="sendMessage()">
                        Send ➤
                    </button>

                </div>

            </div>

        </div>


        <!-- RIGHT PANEL -->

        <div class="panel">


            <!-- KNOWLEDGE -->

            <div class="panel-card">

                <h3>📚 Knowledge Base</h3>

                <input
                    class="topic-search"
                    id="topicSearch"
                    placeholder="Search topics..."
                    onkeyup="filterTopics()"
                >


                <div id="topicsList">

                    {% for topic, data in knowledge.items() %}

                    <div
                        class="topic"
                        data-topic="{{ topic }}"
                        onclick="askTopic('{{ topic }}')"
                    >

                        {{ topic }}

                        <span class="category">
                            {{ data.category }}
                        </span>

                    </div>

                    {% endfor %}

                </div>

            </div>


            <!-- QUICK QUESTIONS -->

            <div class="panel-card">

                <h3>⚡ Quick Questions</h3>

                <button
                    class="quick-question"
                    onclick="setQuestion('What is Python?')"
                >
                    What is Python?
                </button>

                <button
                    class="quick-question"
                    onclick="setQuestion('What is Artificial Intelligence?')"
                >
                    What is Artificial Intelligence?
                </button>

                <button
                    class="quick-question"
                    onclick="setQuestion('What is Machine Learning?')"
                >
                    What is Machine Learning?
                </button>

                <button
                    class="quick-question"
                    onclick="setQuestion('What is DBMS?')"
                >
                    What is DBMS?
                </button>

            </div>


        </div>

    </div>

</div>


<script>

/* ================= TIME ================= */

function updateTime() {

    const now = new Date();

    document.getElementById("time").innerText =
        now.toLocaleDateString() +
        " • " +
        now.toLocaleTimeString();

}

setInterval(updateTime, 1000);

updateTime();


/* ================= SEND MESSAGE ================= */

function sendMessage() {

    const input =
        document.getElementById("messageInput");

    const message =
        input.value.trim();

    if (!message) return;

    addMessage(message, "user");

    input.value = "";

    document.getElementById("typing").style.display = "block";

    fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    })

    .then(response => response.json())

    .then(data => {

        setTimeout(() => {

            document.getElementById("typing").style.display = "none";

            addMessage(
                data.answer,
                "bot",
                data.topic,
                data.confidence
            );

            updateStats();

        }, 500);

    });

}


/* ================= ADD MESSAGE ================= */

function addMessage(
    text,
    type,
    topic = "",
    confidence = ""
) {

    const chatBody =
        document.getElementById("chatBody");

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "message " + type;

    let meta = "";

    if (type === "bot") {

        meta =
            "KnowledgeAI • " +
            topic +
            " • Confidence: " +
            confidence +
            "%";

    } else {

        meta = "You • Now";

    }

    wrapper.innerHTML = `

        <div>

            <div class="message-content">
                ${text}
            </div>

            <div class="message-meta">
                ${meta}
            </div>

        </div>

    `;

    chatBody.appendChild(wrapper);

    chatBody.scrollTop =
        chatBody.scrollHeight;

}


/* ================= UPDATE STATISTICS ================= */

function updateStats() {

    fetch("/stats")

    .then(response => response.json())

    .then(data => {

        document.getElementById("questions")
            .innerText = data.questions;

        document.getElementById("known")
            .innerText = data.known;

        document.getElementById("unknown")
            .innerText = data.unknown;

    });

}


/* ================= QUICK QUESTION ================= */

function setQuestion(question) {

    document.getElementById("messageInput")
        .value = question;

    document.getElementById("messageInput")
        .focus();

}


/* ================= TOPIC ================= */

function askTopic(topic) {

    setQuestion("What is " + topic + "?");

    sendMessage();

}


/* ================= SEARCH TOPICS ================= */

function filterTopics() {

    const search =
        document.getElementById("topicSearch")
        .value
        .toLowerCase();

    const topics =
        document.querySelectorAll(".topic");

    topics.forEach(topic => {

        const name =
            topic.innerText.toLowerCase();

        if (name.includes(search)) {

            topic.style.display = "block";

        } else {

            topic.style.display = "none";

        }

    });

}


/* ================= ENTER KEY ================= */

document.getElementById("messageInput")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    });

</script>

</body>

</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HTML,
        topics=len(KNOWLEDGE_BASE),
        knowledge=KNOWLEDGE_BASE
    )


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "").strip()

    stats["questions"] += 1

    response = get_response(message)

    return jsonify(response)


@app.route("/stats")
def get_stats():

    return jsonify({
        "questions": stats["questions"],
        "known": stats["known"],
        "unknown": stats["unknown"]
    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("       KNOWLEDGE BASE AI CHATBOT")
    print("=" * 60)
    print("Server running at: http://127.0.0.1:5000")
    print("Press CTRL+C to stop")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )