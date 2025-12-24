**The Islamia University of Bahawalpur**

**Department of Artificial Intelligence**


**SOFTWARE REQUIREMENTS SPECIFICATION**

**(SRS DOCUMENT)**

for

**AI SURROGATE HUMAN CLONE**

**_By_**

**Shahzaib Hassan** ---- _Roll No: S22BARIN1M01005_ **Malik Muhammad Saad** - _Roll No: S22BARIN1M01043_ **Sagar Salam** ------ _Roll No: S22BARIN1M01009_

**_Supervisor_**

**Prof Dr. Najia Saher**

**_Bachelor of Science in Artificial Intelligence_**

1

# Table of Contents

[Table of Contents 2](#_bookmark0)

[Revision History 1](#_bookmark1)

[Application Evaluation History 2](#_bookmark2)

- [Introduction 3](#_bookmark3)
  - [Purpose 3](#_bookmark4)
  - [Scope 3](#_bookmark5)
- [Overall description 4](#_bookmark6)
  - [Product perspective 4](#_bookmark7)
  - [Operating environment 4](#_bookmark8)
  - [Accessibility 4](#_bookmark9)
  - [Design and implementation constraints 4](#_bookmark10)
- [Requirement identifying technique 4](#_bookmark11)
  - [Use case diagram 5](#_bookmark12)
  - [Use case description 6](#_bookmark13)
- [Functional Requirements 7](#_bookmark14)
  - [Functional Requirement FR-1 7](#_bookmark15)
  - [Functional Requirement FR-2 7](#_bookmark16)
  - [Functional Requirement FR-3 8](#_bookmark17)
  - [Functional Requirement FR-4 8](#_bookmark18)
  - [Functional Requirement FR-5 9](#_bookmark19)
  - [Functional Requirement FR-6 9](#_bookmark20)
  - [Functional Requirement FR-7 9](#_bookmark21)
  - [Functional Requirement FR-8 10](#_bookmark22)
  - [Functional Requirement FR-9 10](#_bookmark23)
  - [Functional Requirement FR-10 11](#_bookmark24)
- [Non-Functional Requirements 11](#_bookmark25)
  - [Usability 11](#_bookmark26)
  - [Performance 12](#_bookmark27)
  - [Security 12](#_bookmark28)
  - [Scalability 12](#_bookmark29)

[References 13](#_bookmark30)

2

# Revision History

| **Name** | **Date** | **Reason for changes** | **Version** |
| --- | --- | --- | --- |
|     |     |     |     |
|     |     |     |     |

1

# Application Evaluation History

| **Comments (by committee)** | **Action Taken** |
| --- | --- |
|     |     |
|     |     |

**Supervised by**

**&lt;Supervisor's Name&gt;**

### Signature

2

# Introduction

AI Surrogate Human Clone is a cutting-edge, emotionally intelligent virtual assistant designed to revolutionize human-AI interaction through **WhatsApp**. Combining advanced natural language processing, multilingual communication, voice integration, and persistent memory, this AI agent offers a human-like conversational experience that adapts to users' emotions and preferences over time.

Built to serve as a versatile digital companion, the AI clone can handle both personal and professional tasks with ease-from scheduling meetings and drafting documents to offering empathetic support and real-time search. Whether engaging through **text or voice**, in **English, Urdu, or Punjabi**, it ensures accessible, secure, and responsive communication for users across contexts.

By integrating smart task execution, sentiment analysis, and contextual memory, this project redefines what's possible with AI assistants-merging **utility, empathy, and intelligence** into a single, seamless experience.

## Purpose

The purpose of this Software Requirements Specification (SRS) document is to define the functional and non-functional requirements for the "AI Surrogate Human Clone", a conversational AI agent designed to interact with users via WhatsApp using both text and voice. This system will support multiple languages, understand emotional tone, and perform tasks such as scheduling meetings, creating documents, performing web searches, and facilitating payments.

This document serves as a guide for developers, testers, and stakeholders involved in the design, implementation, and evaluation of the system.

## Scope

The "AI Surrogate Human Clone" is intended to function as an intelligent personal assistant that communicates with users over WhatsApp. It will be capable of understanding and responding to user input in English, Urdu, and Punjabi, while maintaining natural and emotionally aware conversations. It assists users with business tasks, customer support, companionship, and productivity through real-time natural conversation, voice synthesis, and emotion-adaptive responses.

Key features include:

- - - Text and voice-based interaction via WhatsApp
      - Emotional tone detection
      - Multilingual support and translation
      - Task execution (scheduling, document creation, web search, GPay integration)
      - Integration with external services such as Google Calendar, Google Docs, SerpAPI, and the WhatsApp Business API
      - Optional Web Dashboard built using Streamlit for advanced users or administrators

The system will be developed using Python and FastAPI, and deployed using Docker. Data persistence will be handled through PostgreSQL.

3

# Overall description

## Product perspective

The product is a standalone intelligent system integrating NLP, TTS/STT, emotional AI, and memory storage components. It is not an upgrade or part of an existing product line, but rather a novel, AI-powered personal assistant accessible via WhatsApp.

## Operating environment

- - - Android and iOS smartphones with WhatsApp installed
      - Programming Language: Python 3.10+
      - Backend Framework: FastAPI
      - Natural Language Processing (NLP): DeepSeek API, Crew.ai
      - Voice Processing: Google Speech-to-Text, Amazon Polly
      - External APIs: WhatsApp Business API, Google Calendar, Google Docs, SerpAPI, GPay
      - Database: PostgreSQL
      - Deployment: Docker containers orchestrated via cloud services
      - Optional Web Dashboard: Streamlit-based UI for advanced users or administrators
      - Communication Interface:
      - User Interaction: Through WhatsApp on Android/iOS devices (text and voice)
      - System Communication: RESTful API calls over HTTPS for secure data exchange with external services

## Accessibility

- - - End users do not require any special hardware or software beyond access to WhatsApp on a smartphone.
      - The backend system runs remotely on cloud infrastructure and scales automatically based on demand.

## Design and implementation constraints

- - - System must adhere to WhatsApp Business API limitations
      - Natural language responses must remain under message length limits
      - All communication must be encrypted (end-to-end where possible)
      - OpenAI APIs may impose token usage and rate limits
      - The assistant must work efficiently on 3G/4G mobile networks
      - Privacy compliance with GDPR and local regulations is mandatory

# Requirement identifying technique

The Requirement Identifying Technique used in this project is Use Case Modeling. This approach is well-suited for interactive systems like the "AI Surrogate Human Clone", which involv4es real-time communication with users and performs a variety of tasks such as scheduling meetings, creating documents, performing web searches, and analyzing emotional tone.

Use cases provide a structured way to capture functional requirements by describing how users interact with the system to achieve specific goals. Each use case includes a description of the main flow of events, alternative flows, exceptions, preconditions, postconditions, business rules, and assumptions.

In this document, we define several key use cases that represent core functionalities of the system. These use cases were derived from the Software Design Description (SDD) and refined through scenario-based discussions and feature mapping.

## Use case diagram

This UML use case diagram illustrates how a user interacts with the AI Surrogate Human Clone system. It highlights five core interactions: sending messages, receiving responses, requesting voice replies, scheduling meetings, and generating documents. These use cases represent the main functional capabilities of the virtual assistant, focusing on natural communication, productivity, and task automation.


**Fig 1:** UML Use Case Diagram for AI Surrogate Human Clone

5

## Use case description

This use case describes the core functionality of the AI Surrogate Human Clone - responding to users via WhatsApp using either text or voice. This use case outlines how the system processes incoming messages, detects sentiment, generates context-aware replies, and responds in a timely and emotionally intelligent manner. It includes the main interaction flow, alternative scenarios, exception handling, and relevant business rules.

**Table 1: Respond to User via WhatsApp (Text/Voice)**

<div class="joplin-table-wrapper"><table><tbody><tr><th><p><strong>Use Case ID:</strong></p></th><th><p>UC-1</p></th></tr><tr><td><p><strong>Use Case Name:</strong></p></td><td><p>Respond to User via WhatsApp (Text/Voice)</p></td></tr><tr><td><p><strong>Actors:</strong></p></td><td><p><strong>Primary: </strong>End User</p><p><strong>Secondary: </strong>WhatsApp API, Speech API</p></td></tr><tr><td><p><strong>Description:</strong></p></td><td><p>User interacts with the AI via text or voice message on WhatsApp. The system understands intent, detects emotion, and provides personalized, empathetic responses.</p></td></tr><tr><td><p><strong>Trigger:</strong></p></td><td><p>User sends a message via WhatsApp.</p></td></tr><tr><td><p><strong>Preconditions:</strong></p></td><td><p><strong>PRE-1: </strong>User is registered and authorized.</p><p><strong>PRE-2: </strong>WhatsApp API is operational.</p></td></tr><tr><td><p><strong>Postconditions:</strong></p></td><td><p><strong>POST-1: </strong>Response is sent.</p><p><strong>POST-2: </strong>Context is logged in memory.</p><p><strong>POST-3: </strong>Sentiment is analyzed and stored.</p></td></tr><tr><td><p><strong>Normal Flow:</strong></p></td><td><ol><li>User sends message (voice/text)</li><li>System converts voice to text (if needed)</li><li>System analyzes sentiment and context</li><li>System generates intelligent reply using GPT</li><li>System responds with TTS (if voice output required)</li></ol></td></tr><tr><td><p><strong>Alternative Flows:</strong></p></td><td><p><strong>A1: </strong>User sends unsupported file</p><p>→ System replies with error and instructions</p><p><strong>A2: </strong>Voice not detected properly</p><p>→ Ask user to resend message</p></td></tr><tr><td><p><strong>Exceptions:</strong></p></td><td><p><strong>E1: </strong>API timeout</p><p>→ Retry or notify user</p></td></tr><tr><td><p><strong>Business Rules</strong></p></td><td><p><strong>BR-1: </strong>Reply time must not exceed 3 seconds</p><p><strong>BR-2: </strong>Memory must be updated after every interaction</p></td></tr><tr><td><p><strong>Assumptions:</strong></p></td><td><p>Users prefer voice interaction during hands-free scenarios</p></td></tr></tbody></table></div>

6

# Functional Requirements

Functional requirements define the **core behaviors and capabilities** that the AI Surrogate Human Clone must exhibit to fulfill its purpose as a human-like virtual assistant. These requirements focus on what the system should _do_ - such as communicating with users, interpreting language and emotions, remembering user preferences, and executing tasks.

In this project, the functional requirements include:

- **Conversational Interaction** via WhatsApp using both **text and voice**
- **Multilingual Support** (English, Urdu, Punjabi)
- **Emotional Intelligence** to detect and respond empathetically to user emotions
- **Persistent Memory** to personalize future interactions
- **Smart Task Execution**, including scheduling events, drafting documents, and conducting real- time web searches

Together, these features make the system **interactive**, **adaptive**, and **intelligent**, providing a seamless and human-like experience for personal, business, and productivity tasks.

## Functional Requirement FR-1

This table defines the core functionality of enabling two-way text communication between the user and the AI via WhatsApp.

**Table 2: WhatsApp Text Chat**

| **Identifier** | FR-1 |
| --- | --- |
| **Title** | WhatsApp Text Chat |
| **Requirement** | The system shall process and respond to user messages sent via WhatsApp. |
| **Source** | Stakeholders |
| **Rationale** | Core communication channel |
| **Business Rule** | BR-1: Reply time must not exceed 3 seconds. |
| **Dependencies** | None |
| **Priority** | High |

## Functional Requirement FR-2

This requirement allows the AI to convert speech to text and generate voice replies, enabling hands-free user interaction.

**Table 3: Voice Input & Output**

| **Identifier** | FR-2 |
| --- | --- |
| **Title** | Voice Input & Output |
| **Requirement** | The system shall convert voice input to text and respond with human- like synthesized speech. 7 |

| **Source** | Users |
| --- | --- |
| **Rationale** | Enhances accessibility and hands-free usability. |
| **Business Rule** | BR-2: Memory must be updated after every interaction. |
| **Dependencies** | FR-1 |
| **Priority** | High |

## Functional Requirement FR-3

The system must support multiple languages, making the assistant inclusive and regionally accessible.

**Table 4: Multilingual Communication**

| **Identifier** | FR-3 |
| --- | --- |
| **Title** | Multilingual Communication |
| **Requirement** | The system shall understand and respond in English, Urdu, and Punjabi. |
| **Source** | Market Need |
| **Rationale** | Expands accessibility to multilingual users. |
| **Business Rule** | None |
| **Dependencies** | FR-1, FR-2 |
| **Priority** | Medium |

## Functional Requirement FR-4

This functionality enables the AI to detect and respond to emotional cues for more empathetic and human-like interactions.

**Table 5: Emotional Response**

| **Identifier** | FR-4 |
| --- | --- |
| **Title** | Emotional Response |
| **Requirement** | The system shall detect emotional tone and tailor its replies empathetically. |
| **Source** | AI Design |
| **Rationale** | Mimics emotional intelligence and improves user experience. |
| **Business Rule** | BR-2 |
| **Dependencies** | FR-1 |
| **Priority** | High 8 |

## Functional Requirement FR-5

The AI must remember user preferences and past interactions to personalize future responses.

**Table 6: Memory of User Preferences**

| **Identifier** | FR-5 |
| --- | --- |
| **Title** | Memory of User Preferences |
| **Requirement** | The system shall store and recall user preferences and conversation history. |
| **Source** | Users |
| **Rationale** | Enables personalized, context-aware interaction. |
| **Business Rule** | BR-2 |
| **Dependencies** | FR-4 |
| **Priority** | High |

## Functional Requirement FR-6

The AI will integrate with Google Calendar to schedule appointments based on user input.

**Table 7: Task Execution - Scheduling**

| **Identifier** | FR-6 |
| --- | --- |
| **Title** | Task Execution - Scheduling |
| **Requirement** | The system shall schedule appointments using the Google Calendar API. |
| **Source** | Users |
| **Rationale** | Automates scheduling, saves user time. |
| **Business Rule** | BR-3: User must have authorized Google access. |
| **Dependencies** | FR-5 |
| **Priority** | Medium |

## Functional Requirement FR-7

The assistant will draft professional or personal documents/messages on request.

**Table 8: Task Execution - Writing**

| **Identifier** | FR-7 |
| --- | --- |
| **Title** | Task Execution - Writing |

9

| **Requirement** | The system shall draft messages, emails, and short documents based on user input. |
| --- | --- |
| **Source** | Users |
| **Rationale** | Supports productivity and communication tasks. |
| **Business Rule** | None |
| **Dependencies** | FR-1 |
| **Priority** | Medium |

## Functional Requirement FR-8

The AI must be able to perform and summarize real-time web searches as requested by the

user.

**Table 9: Task Execution - Real-Time Search**

| **Identifier** | FR-8 |
| --- | --- |
| **Title** | Task Execution - Real-Time Search |
| **Requirement** | The system shall perform web searches using search APIs and provide summarized results. |
| **Source** | Users |
| **Rationale** | Aids in research and quick access to information. |
| **Business Rule** | None |
| **Dependencies** | FR-1 |
| **Priority** | Medium |

## Functional Requirement FR-9

This functionality enables the virtual assistant to facilitate secure transactions by integrating with Google Pay (GPay) for making payments.

**Table 10: Make Payments via GPay**

| **Identifier** | FR-0 |
| --- | --- |
| **Title** | Make Payments via GPay |
| **Requirement** | The system shall enable users to initiate and complete secure payments using GPay within the conversation. |
| **Source** | Users |
| **Rationale** | Supports financial tasks and enhances<br><br>convenience. 10 |

| **Business Rule** | BR-4: User must verify identity before payment. |
| --- | --- |
| **Dependencies** | FR-1 (Text Chat), FR-5 (Memory) |
| **Priority** | Medium |

## Functional Requirement FR-10

This feature ensures that all interactions are stored securely to support personalized responses and long-term memory functionality.

**Table 11: Maintain Conversation History**

| **Identifier** | FR-10 |
| --- | --- |
| **Title** | Maintain Conversation History |
| **Requirement** | The system shall log and store past conversations for contextual understanding and future reference. |
| **Source** | System Design |
| **Rationale** | Enhances personalization and continuity across sessions. |
| **Business Rule** | BR-2: Memory must be updated after each interaction. |
| **Dependencies** | FR-1 (Text Chat), FR-5 (Memory) |
| **Priority** | High |

# Non-Functional Requirements

Non-functional requirements define the quality characteristics, operational criteria, and technical constraints of the AI Surrogate Human Clone. These requirements ensure the system is usable, responsive, secure, and scalable, aligning with user expectations and performance standards.

## Usability

The system should offer a seamless and intuitive user experience that requires minimal learning effort and accommodates users of varying technical proficiency.

- - - The WhatsApp-based interface must be easy to navigate, requiring no additional app installation.
      - The system shall support both text and voice communication modes to ensure accessibility for users with varying preferences.
      - Voice responses must use natural, human-like tone and pacing to simulate real conversation.
      - An automatic onboarding sequence should greet new users with clear instructions on how 1t1o interact with the assistant and what features are available.
      - The system shall provide contextual help during user interactions when confusion or errors are detected.

## Performance

The system must perform with minimal latency and high reliability to ensure a smooth, responsive experience.

- - - At least 95% of system responses must be delivered to the user within 3 seconds of receiving a request.
      - The Speech-to-Text (STT) and Text-to-Speech (TTS) engines must process inputs and outputs with a delay of less than 1 second for every 100 words.
      - The system must support a minimum of 1,000 concurrent users without degradation in response time or accuracy.
      - Scheduled tasks (e.g., meeting reminders) must be executed on time with less than 1-minute deviation.

## Security

To maintain trust and protect user data, the system must adhere to high standards of security and data privacy.

- - - All communication must be encrypted using SSL/TLS protocols or equivalent to prevent interception or tampering.
      - User data, including preferences and conversation history, must be anonymized and stored in encrypted databases.
      - Authentication and authorization must be enforced for sensitive actions such as payments and calendar access.
      - Third-party services (e.g., GPay, Google Calendar) must only be accessed after the user provides explicit, verifiable consent.
      - Regular security audits and penetration tests should be conducted to identify vulnerabilities.

## Scalability

The system must be designed to scale efficiently as user demand increases.

- - - The backend architecture shall be horizontally scalable, allowing new instances to be spun up automatically during high load.
      - Serverless functions or microservices should auto-scale in real time based on incoming traffic.

12

- - - System design should support future expansion, such as integration with other messaging platforms (e.g., Telegram, Messenger) and APIs without major rework.
      - Load testing must confirm that performance metrics remain stable as traffic increases.

# References

- - - Google Developers. (2025). _GPay API_. Retrieved from <https://developers.google.com/pay/api>
      - FastAPI. (2025). _FastAPI Documentation_. Retrieved from [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
      - Docker Inc. (2025). _Docker Documentation_. Retrieved from [https://docs.docker.com](https://docs.docker.com/)
      - PostgreSQL Global Development Group. (2025). _PostgreSQL Documentation_. Retrieved from <https://www.postgresql.org/docs>

13