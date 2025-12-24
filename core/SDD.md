The Islamia University of Bahawalpur

**Department of Artificial Intelligence**


**SOFTWARE DESIGN DESCRIPTION**

**(SDD DOCUMENT)**

**For**

AI SURROGATE HUMAN CLONE

**_By_**

**Shahzaib Hassan** ---- _Roll No: S22BARIN1M01005_ **Malik Muhammad Saad** - _Roll No: S22BARIN1M01043_ **Sagar Salam** ------ _Roll No: S22BARIN1M01009_

**Session 2022 - 2025**

**_Supervisor_**

**Prof. Dr Najia Saher**

**Chairperson**

**_Bachelor of Science in Artificial Intelligence_**

Table of Contents

- [Introduction 4](#_bookmark0)
- [System Architecture 4](#_bookmark1)
  - [Design Methodology: Object-Oriented Programming (OOP) 4](#_bookmark2)
  - [Software Process Model: Agile Methodology 4](#_bookmark3)
- [System Overview 5](#_bookmark4)
  - [Architectural Design 5](#_bookmark5)
  - [Module Descriptions 5](#_bookmark6)
  - [Process Diagram 7](#_bookmark7)
- [Design Models 7](#_bookmark8)
- [Algorithm & Implementation 10](#_bookmark9)
  - [NLP/NLU & NLG Module 10](#_bookmark10)
  - [Voice Processing Module 11](#_bookmark11)
  - [Agent Manager (Crew.ai) 11](#_bookmark12)
  - [Task Agents 12](#_bookmark13)
  - [WhatsApp Communication Interface 13](#_bookmark14)
  - [External API Integration Layer 13](#_bookmark15)
- [User Interface Design 14](#_bookmark16)
  - [Primary Interface - WhatsApp Integration 14](#_bookmark17)
  - [Web Dashboard - Streamlit-Based UI 14](#_bookmark18)

[APPENDIX I 15](#_bookmark19)

**Revision History**

| **Name** | **Date** | **Reason for changes** | **Version** |
| --- | --- | --- | --- |
|     |     |     |     |
|     |     |     |     |

##### Application Evaluation History

| **Comments (by committee)** | **Action Taken** |
| --- | --- |
|     |     |
|     |     |

**Supervised by Prof. Dr Najia Saher**

#### Signature

# Introduction

The development of intelligent systems capable of interacting with humans in a natural and meaningful way has become a central focus in modern artificial intelligence research. In line with this vision, our final year project aims to design and implement an AI Surrogate Agent - a conversational digital assistant that emulates human-like interaction through text and voice, supports multiple languages, and assists users in managing business operations efficiently.

This system leverages cutting-edge technologies such as the **DeepSeek API**, **Crew.ai**, and the **WhatsApp Business API**, enabling the agent to perform tasks like scheduling meetings, booking tickets, sending proposals, conducting online searches, and facilitating payments via GPay. The agent also features emotional intelligence by analyzing the tone of user input and adapting its responses accordingly, making interactions more personalized and engaging.

So far, the following core modules have been conceptualized and partially implemented:

- **Conversational Agent Module**: Implements natural language understanding and generation using DeepSeek and Crew.ai, supporting empathetic and context-aware conversations.
- **Business Assistant Module**: Integrates with external APIs (Google Calendar, Google Docs, SerpAPI, GPay) to assist in professional tasks.
- **Voice Interaction Module**: Enables voice message support through WhatsApp, using Google's Speech-to-Text and Amazon Polly for Text-to-Speech synthesis.
- **Tone & Language Adaptation Module**: Detects the emotional tone and language of incoming messages to provide appropriate and culturally sensitive responses.
- **System Integration Layer**: Ensures seamless communication between internal modules and external APIs.
- **Database Management Module**: Handles secure storage and retrieval of user preferences, conversation history, and task logs.

# System Architecture

### Design Methodology: Object-Oriented Programming (OOP)

We adopted Object-Oriented Programming (OOP) for its ability to model complex, real-world interactions in a modular and scalable way. OOP offers key benefits:

- **Modularity & Maintainability:** Encapsulation enables cleaner, more manageable code.
- **Reusability:** Inheritance reduces redundancy through shared base classes.
- **Flexibility:** Polymorphism supports dynamic behavior and easier feature integration.
- **Real-World Modeling:** OOP naturally maps software components like agents and services to real-world concepts.

These features make OOP ideal for handling the system's multiple interacting modules.

### Software Process Model: Agile Methodology

We have chosen the **Agile** software development methodology to guide our project's lifecycle.

###### Justification

- **Iterative Development:** Agile supports development in short cycles, allowing us to build and improve the system incrementally. This suits our project where requirements may change based on user feedback and testing.
- **Customer Collaboration:** Continuous engagement with users ensures that features align with real needs and expectations, improving overall project relevance.
- **Flexibility and Adaptability:** Agile allows adjustments even in later stages, helping us respond effectively to new requirements or technology shifts without major disruptions.
- **Enhanced Quality through Continuous Testing:** Frequent testing during development helps identify and resolve issues early, resulting in a more stable and reliable system.

Given the dynamic nature of our project, which integrates various technologies and requires frequent validation of functionalities, the Agile methodology provides the flexibility and responsiveness needed to manage complexities effectively.

# System Overview

### Architectural Design

The AI Surrogate Agent is a modular, multilingual conversational system that integrates multiple AI and API-driven components to provide a natural, emotionally intelligent interaction with users over WhatsApp. The architecture follows a service-oriented design, where each subsystem is loosely coupled and communicates via well-defined interfaces.

This modular structure allows for flexibility, scalability, and ease of maintenance. Each component can be developed, tested, and updated independently without affecting the overall system functionality.

The system has been decomposed into the following five major modules:

- NLP/NLU & NLG Module
- Voice Processing Module
- Agent Manager (Crew.ai)
- External API Integration Layer
- WhatsApp Communication Interface

## Module Descriptions

- - 1. **NLP/NLU & NLG Module**

**Technology:** DeepSeek API / OpenAI API

This module serves as the core intelligence of the system. It is responsible for understanding the meaning, intent, and emotional tone behind user messages. It also generates natural language responses that are contextually and emotionally appropriate.

Key Functions:

- - - - Detects user intent and emotional tone using sentiment analysis
            - Supports multilingual inputs including English, Urdu, and Punjabi
            - Generates human-like text responses using advanced language models
            - Handles code-switching and adapts to cultural nuances for more natural communication

This module ensures that the surrogate agent behaves empathetically and intelligently in conversations.

- - 1. **Voice Processing Module**

This module enables the system to interact with users through voice-based input and output. It facilitates accessibility and enhances user experience by allowing hands-free interaction.

Key Functions:

- - - - Speech-to-Text (STT): Converts voice messages into text using Google Speech-to-Text API
            - Text-to-Speech (TTS): Converts generated text responses into natural-sounding speech using ElevenLabs or Amazon Polly

By supporting both STT and TTS, this module makes the AI surrogate accessible to users who prefer verbal communication.

- - 1. **Agent Manager (Crew.ai)**

**Technology:** Crew.ai framework with multiple specialized agents

This module serves as the system's orchestrator, managing autonomous agents that handle tasks based on user input. Each agent has a specific role:

- - - - **Chat Agent:** Handles general conversations and maintains history.
            - **Schedule Agent:** Manages events and reminders via Google Calendar.
            - **Docs Agent:** Creates and shares documents through Google Docs.
            - **Search Agent:** Conducts real-time searches using SerpAPI.

The Agent Manager routes tasks to the appropriate agent based on detected intent, ensuring efficient execution.

- - 1. **External API Integration Layer**

This module securely connects the system to external APIs, simplifying third-party integrations and offering a unified interface for internal use.

###### Supported Services

- - - - WhatsApp Business API (messaging)
            - Google Calendar & Docs APIs (scheduling, documents)
            - SerpAPI (real-time search)
            - Google STT & ElevenLabs/Amazon Polly (voice processing)

###### Security & Reliability

- - - - Uses OAuth 2.0 and API keys for secure access
            - Employs retry, circuit breakers, and fallbacks for robust error handling It ensures smooth, secure, and reliable external communication.

        - **WhatsApp Communication Interface**

This module serves as the entry and exit point for all user interactions. It connects the system directly with users via WhatsApp, enabling both text and voice-based communication.

Key Functions:

- - - - Receives text and voice messages from users
            - Sends back generated text or synthesized voice responses
            - Authenticates and maintains secure communication with the WhatsApp Business API

This module ensures that the AI surrogate feels like a natural part of the user's daily communication environment.

**Fig 1:** Process Diagram of the "AI Surrogate Human Clone" System

# Design Models

- 1. **Class Diagram**

The class diagram presents an object-oriented structure of the AI Surrogate Agent, highlighting key components for processing input, generating responses, and integrating with external services.

###### Key Classes

- **User:** WhatsApp user
- **SurrogateAgent:** Core message handler
- **NLPModule:** Handles language understanding and response generation
- **ToneAnalyzer & LanguageTranslator:** Support emotional and language analysis
- **VoiceProcessor:** Manages speech-to-text and vice versa
- **AgentManager:** Directs task agents based on intent
- **TaskAgent (abstract):** Base for ChatAgent, ScheduleAgent, DocsAgent, SearchAgent
- **ExternalAPIClient (abstract):** Base for WhatsAppAPI, GoogleCalendarAPI, etc.

###### Relationships

- **Inheritance:** Specialized agents extend TaskAgent; APIs extend ExternalAPIClient
- **Composition:** AgentManager includes multiple TaskAgents
- **Association:** Modules interact as per workflow (e.g., NLPModule uses ToneAnalyzer) This modular design supports scalability, multilingualism, and emotionally aware interactions.





**Fig 3:** Sequence Diagram of the "AI Surrogate Human Clone" System

**4.2 Data Flow Diagram**

The Data Flow Diagram illustrates how data flows through the AI Surrogate Agent system. At Level 0 (context level), it shows the system's interaction with external entities such as the user and third-party APIs. At Level 1, the system is decomposed into key processes including message reception, intent processing, task routing, execution, response generation, and reply delivery. This diagram provides a functional overview of how data is received, transformed, and returned by the system during a typical interaction.


**Fig 4:** Data Flow of the "AI Surrogate Human Clone" System

# Algorithm & Implementation

This section outlines the internal logic and processing algorithms used in each major component of the AI Surrogate Agent system. The implementation details are described using pseudocode-style definitions to illustrate how input is received, processed, and transformed into meaningful output.

### NLP/NLU & NLG Module

The **NLP/NLU & NLG Module** is responsible for understanding user intent, detecting emotional tone, generating natural language responses, and supporting multilingual interaction.

Core Functions:

FUNCTION process_input(text) LANGUAGE = detect_language(text) IF LANGUAGE is not 'en' THEN

TEXT = translate(text, target='en')

INTENT = analyze_intent(TEXT) TONE = detect_tone(TEXT)

RESPONSE = generate_response(INTENT, TONE, TEXT) IF LANGUAGE is not 'en' THEN

RESPONSE = translate(RESPONSE, target=LANGUAGE) RETURN RESPONSE

END FUNCTION

- detect_language(text) uses the langdetect library to identify the input language.
- translate(text, target) calls the Google Translate API.
- analyze_intent(text) sends text to the DeepSeek API for intent detection.
- detect_tone(text) uses sentiment analysis to determine emotional state.
- generate_response(intent, tone, context) creates a natural language response based on context and tone.

### Voice Processing Module

This module handles both **speech-to-text** and **text-to-speech** conversions to support voice- based communication over WhatsApp.

Speech-to-Text Function:

FUNCTION transcribe_audio(audio_file) INIT Google STT client

LOAD audio from file

SET config: language_code = 'ur-PK' SEND request to Google STT API RETURN transcription.text

END FUNCTION

Text-to-Speech Function:

FUNCTION synthesize_speech(text) INIT Amazon Polly client CALL SynthesizeSpeech with:

Text = text OutputFormat = 'mp3' VoiceId = 'Aditi'

RETURN audio_stream END FUNCTION

### Agent Manager (Crew.ai)

The **Agent Manager** dynamically assigns tasks to specialized agents based on detected intent.

Task Routing Logic:

FUNCTION get_appropriate_agent(intent) SWITCH(intent)

CASE "chat":

RETURN ChatAgent()

CASE "schedule":

RETURN ScheduleAgent() CASE "document":

RETURN DocsAgent() CASE "search":

RETURN SearchAgent() DEFAULT:

RETURN DefaultAgent()

END FUNCTION

Each agent performs its task independently and returns the result to the manager for final response generation.

### Task Agents

Each **Task Agent** performs a specific business function. Below are the key operations of each

agent.

- - 1. ChatAgent

Handles general conversation and maintains history.

FUNCTION respond(history, new_message) COMBINE history + new_message

GENERATE conversational response using NLPModule RETURN response

END FUNCTION

- - 1. ScheduleAgent

Interacts with Google Calendar API to book events.

FUNCTION book_event(title, date, time, participants) AUTHENTICATE with Google Calendar

PREPARE event object

CALL calendar.events().insert() RETURN confirmation message

END FUNCTION

- - 1. DocsAgent

Generates and shares documents via Google Docs API.

FUNCTION create_document(template, content) AUTHENTICATE with Google Docs API CREATE document from template

INSERT content into document SHARE document with user RETURN document_link

END FUNCTION

- - 1. SearchAgent

Performs real-time web searches using SerpAPI.

FUNCTION perform_search(query) CALL SerpAPI with query PARSE results

RETURN formatted summary END FUNCTION

### WhatsApp Communication Interface

This module serves as the entry and exit point for all WhatsApp messages.

Receiving Messages:

FUNCTION receive_message(webhook_payload) EXTRACT message body or media URL

IF message is voice THEN CALL transcribe_audio()

RETURN message_text END FUNCTION

Sending Responses:

FUNCTION send_reply(recipient_id, reply_content, is_voice) IF is_voice THEN

AUDIO = synthesize_speech(reply_content) SEND audio message via WhatsApp API

ELSE

SEND text message via WhatsApp API

END IF END FUNCTION

### External API Integration Layer

This module abstracts interactions with external services and includes error handling mechanisms.

General API Call Handling:

FUNCTION call_api(endpoint, data, auth_token) SET headers with auth_token

SEND POST/GET request to endpoint IF rate limit exceeded THEN

WAIT and retry IF error THEN

RETURN fallback response

ELSE

RETURN JSON response

END FUNCTION

This layer ensures secure, reliable, and consistent communication with third-party APIs like DeepSeek, Google Calendar, and SerpAPI.

# User Interface Design

The AI Surrogate Agent provides a dual-interface system, combining the accessibility of WhatsApp-based interaction with the functionality of a dedicated web dashboard built using Streamlit.

### Primary Interface - WhatsApp Integration

The primary mode of interaction for end users is through WhatsApp, a globally popular messaging platform. This ensures ease of access and familiarity, particularly beneficial for users who prefer conversational communication over traditional apps or websites.


# APPENDIX I

- DeepSeek. (2025). _DeepSeek API_. Retrieved from <https://deepseek.com/api>
- Crew.ai. (2025). _Crew.ai Framework_. Retrieved from [https://crew.ai](https://crew.ai/)
- Google Cloud. (2025). _Speech-to-Text API_. Retrieved from <https://cloud.google.com/speech-to-text>
- Amazon Web Services. (2025). _Amazon Polly_. Retrieved from <https://aws.amazon.com/polly>
- Meta Platforms. (2025). _WhatsApp Business API_. Retrieved from <https://www.whatsapp.com/business/api>
- SerpAPI. (2025). _SerpAPI_. Retrieved from [https://serpapi.com](https://serpapi.com/)
- Google Developers. (2025). _Google Calendar API_. Retrieved from <https://developers.google.com/calendar>
- Google Developers. (2025). _Google Docs API_. Retrieved from <https://developers.google.com/docs>
- Google Developers. (2025). _GPay API_. Retrieved from <https://developers.google.com/pay/api>
- FastAPI. (2025). _FastAPI Documentation_. Retrieved from [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- Docker Inc. (2025). _Docker Documentation_. Retrieved from [https://docs.docker.com](https://docs.docker.com/)
- PostgreSQL Global Development Group. (2025). _PostgreSQL Documentation_. Retrieved from <https://www.postgresql.org/docs>