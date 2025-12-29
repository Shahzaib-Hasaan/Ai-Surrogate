# AI Surrogate Mobile App - Technical Documentation

**Version**: 1.0.0  
**Last Updated**: December 29, 2024  
**Platform**: React Native (Expo)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Features & Implementation](#features--implementation)
6. [State Management](#state-management)
7. [API Integration](#api-integration)
8. [UI/UX Design](#uiux-design)
9. [Components Documentation](#components-documentation)
10. [Screens Documentation](#screens-documentation)
11. [Services & Utilities](#services--utilities)
12. [Setup & Configuration](#setup--configuration)

---

## 1. Project Overview

The AI Surrogate Mobile App is a React Native application built with Expo that provides an intelligent conversational AI assistant. The app features real-time streaming responses, conversation history management, user authentication, and a modern WhatsApp-inspired UI.

### Key Capabilities
- Real-time AI chat with streaming responses
- Text-to-Speech (TTS) for AI messages
- Conversation history management
- User authentication (login/register)
- Profile management
- Insights and analytics
- Offline-first architecture with AsyncStorage
- Dark/Light theme support

---

## 2. Technology Stack

### Core Framework
- **React Native**: 0.81.5
- **Expo SDK**: ~54.0.30
- **TypeScript**: ~5.9.2
- **React**: 19.1.0

### Navigation
- **@react-navigation/native**: ^6.1.18
- **@react-navigation/native-stack**: ^6.9.25
- **@react-navigation/bottom-tabs**: ^6.6.1

### State Management
- **Zustand**: ^5.0.9 (Lightweight state management)

### UI Libraries
- **react-native-paper**: ^5.14.5 (Material Design components)
- **@expo/vector-icons**: ^15.0.3 (Icon library)
- **react-native-animatable**: ^1.4.0 (Animations)

### Networking
- **Axios**: ^1.13.2 (HTTP client)

### Storage
- **@react-native-async-storage/async-storage**: ^2.2.0 (Local storage)
- **expo-secure-store**: ~15.0.8 (Secure token storage)

### Features
- **expo-speech**: ~14.0.8 (Text-to-Speech)
- **expo-speech-recognition**: Latest (Speech-to-Text)
- **expo-haptics**: ~15.0.8 (Haptic feedback)
- **expo-clipboard**: ~8.0.8 (Clipboard operations)
- **expo-blur**: ^15.0.8 (Blur effects)
- **expo-linear-gradient**: ^15.0.8 (Gradient backgrounds)

### Additional Libraries
- **react-native-markdown-display**: ^7.0.2 (Markdown rendering)
- **react-syntax-highlighter**: ^15.5.0 (Code syntax highlighting)
- **react-native-chart-kit**: ^6.12.0 (Charts for insights)

---

## 3. Architecture

### Architecture Pattern
The app follows a **modular component-based architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Screens  │  │Components│  │Navigation│  │  Theme   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Hooks   │  │  Stores  │  │  Utils   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Services │  │   API    │  │ Storage  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles
1. **Modular Components**: Reusable, single-responsibility components
2. **Separation of Concerns**: Clear boundaries between UI, logic, and data
3. **Type Safety**: Full TypeScript implementation
4. **State Management**: Centralized state with Zustand stores
5. **API-First**: Backend-driven data with optimistic updates

---

## 4. Project Structure

```
ai-surrogate-mobile/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── chat/            # Chat-specific components
│   │   │   ├── ChatHeader.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── ChatLoading.tsx
│   │   │   └── TypingIndicator.tsx
│   │   ├── conversations/   # Conversation list components
│   │   │   ├── ConversationItem.tsx
│   │   │   ├── DeleteConfirmDialog.tsx
│   │   │   └── EmptyConversations.tsx
│   │   ├── profile/         # Profile screen components
│   │   │   ├── ProfileHeader.tsx
│   │   │   ├── SettingsSection.tsx
│   │   │   ├── DataSection.tsx
│   │   │   └── AppInfoSection.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── CodeBlock.tsx
│   │   ├── EmptyState.tsx
│   │   └── ... (other shared components)
│   │
│   ├── screens/             # Screen components
│   │   ├── LoginScreen.tsx
│   │   ├── RegisterScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── ChatScreen.tsx
│   │   ├── ConversationsScreen.tsx
│   │   ├── InsightsScreen.tsx
│   │   └── ProfileScreen.tsx
│   │
│   ├── navigation/          # Navigation configuration
│   │   ├── RootNavigator.tsx
│   │   └── BottomTabNavigator.tsx
│   │
│   ├── store/               # Zustand state stores
│   │   ├── authStore.ts     # Authentication state
│   │   ├── chatStore.ts     # Chat & messages state
│   │   └── themeStore.ts    # Theme preferences
│   │
│   ├── services/            # API & external services
│   │   ├── api.ts           # Axios instance configuration
│   │   ├── authService.ts   # Authentication API calls
│   │   ├── chatService.ts   # Chat API calls
│   │   └── streamingService.ts  # Streaming responses
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useConversations.ts  # Conversation management logic
│   │   └── useKeyboardScroll.ts # Keyboard handling
│   │
│   ├── theme/               # Design system
│   │   ├── colors.ts        # Color palette
│   │   ├── typography.ts    # Text styles
│   │   ├── spacing.ts       # Spacing constants
│   │   ├── gradients.ts     # Gradient definitions
│   │   └── animations.ts    # Animation presets
│   │
│   ├── types/               # TypeScript type definitions
│   │   └── index.ts
│   │
│   ├── config/              # App configuration
│   │   └── api.ts           # API endpoints & base URL
│   │
│   └── utils/               # Utility functions
│       └── validation.ts
│
├── assets/                  # Static assets (images, fonts)
├── docs/                    # Documentation
├── package.json
├── tsconfig.json
├── app.json                 # Expo configuration
└── index.ts                 # App entry point
```

---

## 5. Features & Implementation

### 5.1 Authentication System

**Implementation**: JWT-based authentication with secure token storage

**Files**:
- `src/store/authStore.ts` - Auth state management
- `src/services/authService.ts` - API calls
- `src/screens/LoginScreen.tsx` - Login UI
- `src/screens/RegisterScreen.tsx` - Registration UI

**Features**:
- Email/password authentication
- JWT token storage in SecureStore
- Auto-login on app launch
- Token refresh mechanism
- Logout functionality

**Flow**:
```
User Input → authService.login() → Store JWT in SecureStore 
→ Update authStore → Navigate to Home
```

### 5.2 Real-Time Chat with Streaming

**Implementation**: Server-Sent Events (SSE) for streaming AI responses

**Files**:
- `src/screens/ChatScreen.tsx` - Main chat interface
- `src/store/chatStore.ts` - Chat state & logic
- `src/services/streamingService.ts` - SSE implementation
- `src/components/MessageBubble.tsx` - Message display

**Features**:
- Real-time streaming responses
- Optimistic UI updates
- Typing indicators
- Message history
- Auto-scroll to latest message
- WhatsApp-style UI design

**Streaming Flow**:
```
User sends message → Optimistic update → POST /api/chat/message
→ SSE stream opens → Chunks received → Update message content
→ Stream completes → Final message saved
```

### 5.3 Text-to-Speech (TTS)

**Implementation**: Native device TTS using expo-speech

**Files**:
- `src/components/MessageBubble.tsx` - TTS button & logic

**Features**:
- Play/pause button on AI messages
- Native voice synthesis
- Visual feedback (icon changes)
- No backend required

**Usage**:
```typescript
Speech.speak(message.content, {
    language: 'en-US',
    pitch: 1.0,
    rate: 0.9,
    onDone: () => setIsSpeaking(false),
});
```

### 5.4 Speech-to-Text (STT)

**Implementation**: Native device speech recognition using expo-speech-recognition

**Files**:
- `src/components/chat/ChatInput.tsx` - Voice recording button & STT logic

**Features**:
- Press-and-hold microphone button
- Real-time transcription
- Automatic punctuation
- Visual feedback (icon changes to green when recording)
- No backend required
- Supports multiple languages

**Usage**:
```typescript
// Start recording
ExpoSpeechRecognitionModule.start({
    lang: 'en-US',
    interimResults: true,
    maxAlternatives: 1,
    continuous: false,
    requiresOnDeviceRecognition: false,
    addsPunctuation: true,
    contextualStrings: ['AI', 'Surrogate', 'chat'],
});

// Listen for results
useSpeechRecognitionEvent('result', (event) => {
    const transcript = event.results[0]?.transcript;
    if (transcript) {
        onChangeText(value + transcript);
    }
});

// Stop recording
ExpoSpeechRecognitionModule.stop();
```

**Permissions**:
- Android: `RECORD_AUDIO` permission
- iOS: Microphone usage description in app.json

### 5.5 Conversation Management

**Implementation**: CRUD operations for conversation history

**Files**:
- `src/screens/ConversationsScreen.tsx` - List view
- `src/hooks/useConversations.ts` - Business logic
- `src/components/conversations/*` - UI components

**Features**:
- List all conversations
- Search conversations
- Delete conversations
- Pull-to-refresh
- Empty state handling
- Optimistic updates

### 5.5 Profile & Settings

**Implementation**: Modular profile screen with sections

**Files**:
- `src/screens/ProfileScreen.tsx` - Main profile screen
- `src/components/profile/*` - Profile sections

**Features**:
- User information display
- Settings management
- Data usage statistics
- App information
- Logout functionality

### 5.6 Loading States & UX

**Implementation**: Loading animations and feedback

**Files**:
- `src/components/chat/ChatLoading.tsx` - Chat loading animation
- `src/screens/ConversationsScreen.tsx` - List loading

**Features**:
- Fade-in animations
- Pulsing text
- WhatsApp-style spinners
- Immediate navigation feedback
- Skeleton screens

---

## 6. State Management

### Zustand Stores

#### 6.1 authStore.ts
**Purpose**: Manages authentication state

**State**:
```typescript
{
  user: User | null,
  token: string | null,
  isLoading: boolean,
  error: string | null
}
```

**Actions**:
- `login(email, password)` - Authenticate user
- `register(userData)` - Create new account
- `logout()` - Clear session
- `loadUser()` - Load user from storage
- `clearError()` - Reset error state

#### 6.2 chatStore.ts
**Purpose**: Manages chat messages and conversations

**State**:
```typescript
{
  messages: Message[],
  conversations: Conversation[],
  currentConversationId: string | null,
  isLoading: boolean,
  isSending: boolean,
  isTyping: boolean,
  isStreaming: boolean,
  streamingContent: string,
  error: string | null
}
```

**Actions**:
- `sendStreamingMessage(content)` - Send message with streaming
- `loadMessages(conversationId)` - Load conversation history
- `loadConversations()` - Load all conversations
- `deleteConversation(id)` - Remove conversation
- `clearMessages()` - Reset messages

#### 6.3 themeStore.ts
**Purpose**: Manages theme preferences

**State**:
```typescript
{
  isDark: boolean
}
```

**Actions**:
- `toggleTheme()` - Switch between light/dark
- `setTheme(isDark)` - Set specific theme

---

## 7. API Integration

### Base Configuration

**File**: `src/config/api.ts`

```typescript
export const API_BASE_URL = 'https://ai-surrogate-27pf.onrender.com';

export const API_ENDPOINTS = {
  // Auth
  REGISTER: '/api/auth/register',
  LOGIN: '/api/auth/login',
  ME: '/api/auth/me',
  
  // Chat
  SEND_MESSAGE: '/api/chat/message',
  GET_CONVERSATIONS: '/api/chat/conversations',
  GET_MESSAGES: (id) => `/api/chat/conversations/${id}/messages`,
  
  // Conversations
  DELETE_CONVERSATION: (id) => `/api/conversations/${id}`,
};
```

### Axios Instance

**File**: `src/services/api.ts`

**Features**:
- Automatic JWT token injection
- Request/response interceptors
- Error handling
- Token refresh logic

```typescript
apiClient.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Service Layer

#### authService.ts
- `login(email, password)` - POST /api/auth/login
- `register(userData)` - POST /api/auth/register
- `getCurrentUser()` - GET /api/auth/me

#### chatService.ts
- `sendMessage(messageData)` - POST /api/chat/message
- `getConversations()` - GET /api/chat/conversations
- `getMessages(conversationId)` - GET /api/chat/conversations/:id/messages
- `deleteConversation(id)` - DELETE /api/conversations/:id

#### streamingService.ts
- `streamMessage(content, conversationId, callbacks)` - SSE streaming

---

## 8. UI/UX Design

### Design System

#### Color Palette (WhatsApp-Inspired)

**Light Mode**:
- Background: `#EFEAE2` (Beige)
- User Bubble: `#DCF8C6` (Light green)
- AI Bubble: `#FFFFFF` (White)
- Text: `#111B21` (Dark gray)
- Accent: `#25D366` (WhatsApp green)

**Dark Mode**:
- Background: `#0B141A` (Dark blue-gray)
- User Bubble: `#005C4B` (Dark green)
- AI Bubble: `#1F2C34` (Dark gray)
- Text: `#E9EDEF` (Light gray)
- Accent: `#00A884` (Teal green)

#### Typography

**File**: `src/theme/typography.ts`

```typescript
{
  h1: { fontSize: 32, fontWeight: '700' },
  h2: { fontSize: 28, fontWeight: '600' },
  h3: { fontSize: 24, fontWeight: '600' },
  h4: { fontSize: 20, fontWeight: '600' },
  body: { fontSize: 16, fontWeight: '400' },
  caption: { fontSize: 14, fontWeight: '400' },
  small: { fontSize: 12, fontWeight: '400' }
}
```

#### Spacing

**File**: `src/theme/spacing.ts`

```typescript
{
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48
}
```

### UI Components

#### Message Bubbles
- Rounded corners (8px)
- Tail effect (2px corner radius)
- Shadows for depth
- Dynamic text colors
- TTS button integration

#### Animations
- Fade-in: 300ms
- Pulse: 1500ms infinite
- Slide-in: 200ms
- Smooth scrolling

---

## 9. Components Documentation

### Chat Components

#### ChatHeader.tsx
**Purpose**: Displays conversation partner info and back button

**Props**:
```typescript
{
  userName: string,
  isDark: boolean,
  onBackPress: () => void
}
```

**Features**:
- Avatar with first letter
- User name display
- "AI Surrogate" subtitle
- Back navigation button

#### ChatInput.tsx
**Purpose**: Message input with emoji picker

**Props**:
```typescript
{
  value: string,
  onChangeText: (text: string) => void,
  onSend: () => void,
  isSending: boolean,
  isDark: boolean
}
```

**Features**:
- Multi-line text input
- Emoji picker modal
- Attachment button (placeholder)
- Send button with loading state
- Character limit (5000)

#### ChatLoading.tsx
**Purpose**: Loading animation for message history

**Props**:
```typescript
{
  isDark: boolean
}
```

**Features**:
- Fade-in animation
- Pulsing text
- WhatsApp-style spinner
- Theme-aware colors

#### MessageBubble.tsx
**Purpose**: Individual message display

**Props**:
```typescript
{
  message: Message
}
```

**Features**:
- WhatsApp-style bubbles
- Code block support
- TTS playback button
- Timestamp display
- Dynamic colors based on sender/theme

### Conversation Components

#### ConversationItem.tsx
**Purpose**: Single conversation card

**Props**:
```typescript
{
  conversation: Conversation,
  onPress: () => void,
  onDelete: () => void
}
```

**Features**:
- Conversation title
- Relative timestamp
- Delete button
- Card press handling

#### EmptyConversations.tsx
**Purpose**: Empty state for conversation list

**Features**:
- Icon display
- Helpful message
- Call-to-action

#### DeleteConfirmDialog.tsx
**Purpose**: Confirmation dialog for deletion

**Props**:
```typescript
{
  visible: boolean,
  onDismiss: () => void,
  onConfirm: () => void
}
```

### Profile Components

#### ProfileHeader.tsx
**Purpose**: User profile information

**Features**:
- User avatar
- Username display
- Email display
- Statistics (messages, conversations)

#### SettingsSection.tsx
**Purpose**: App settings

**Features**:
- Theme toggle
- Notification settings
- Sound settings

#### DataSection.tsx
**Purpose**: Usage statistics

**Features**:
- Message count
- Conversation count
- Data usage charts

#### AppInfoSection.tsx
**Purpose**: App information

**Features**:
- Version number
- About information
- Links to documentation

---

## 10. Screens Documentation

### LoginScreen.tsx
**Route**: `/login`

**Features**:
- Email/password form
- Form validation
- Error display
- Loading state
- Navigate to register
- Auto-login if token exists

### RegisterScreen.tsx
**Route**: `/register`

**Features**:
- Username, email, password fields
- Form validation
- Error handling
- Navigate to login
- Success feedback

### HomeScreen.tsx
**Route**: `/home` (Tab: Home)

**Features**:
- Welcome message
- Recent conversations
- Quick actions
- Statistics overview

### ChatScreen.tsx
**Route**: `/chat`

**Features**:
- Message list with auto-scroll
- Streaming responses
- Typing indicator
- TTS playback
- Message input
- Keyboard avoidance
- Loading animation
- WhatsApp-style UI

**Key Implementation**:
```typescript
// Auto-scroll to last message
useEffect(() => {
  if (!isLoading && messages.length > 0) {
    setTimeout(() => {
      flatListRef.current?.scrollToEnd({ animated: true });
    }, 100);
  }
}, [isLoading, messages.length]);
```

### ConversationsScreen.tsx
**Route**: `/conversations` (Tab: Conversations)

**Features**:
- Conversation list
- Search functionality
- Pull-to-refresh
- Delete conversations
- Empty state
- Loading state
- New chat FAB

### InsightsScreen.tsx
**Route**: `/insights` (Tab: Insights)

**Features**:
- Usage statistics
- Charts and graphs
- Activity timeline
- Trends analysis

### ProfileScreen.tsx
**Route**: `/profile` (Tab: Profile)

**Features**:
- User information
- Settings management
- Data statistics
- App information
- Logout button

---

## 11. Services & Utilities

### streamingService.ts

**Purpose**: Handle Server-Sent Events for streaming responses

**Key Function**:
```typescript
export const streamMessage = async (
  content: string,
  conversationId: string | null,
  callbacks: {
    onConversationId?: (id: string) => void,
    onChunk?: (chunk: string) => void,
    onComplete?: (messageId: string) => void,
    onError?: (error: string) => void
  }
) => {
  // SSE implementation
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, conversation_id })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    callbacks.onChunk?.(chunk);
  }
};
```

### Custom Hooks

#### useConversations.ts
**Purpose**: Encapsulate conversation management logic

**Returns**:
```typescript
{
  conversations: Conversation[],
  isLoading: boolean,
  refreshing: boolean,
  searchQuery: string,
  deleteDialogVisible: boolean,
  setSearchQuery: (query: string) => void,
  handleRefresh: () => Promise<void>,
  handleNewChat: (navigation) => void,
  handleOpenChat: (id, navigation) => void,
  handleDeleteConversation: (id) => void,
  confirmDelete: () => Promise<void>,
  cancelDelete: () => void
}
```

#### useKeyboardScroll.ts
**Purpose**: Handle keyboard appearance and auto-scroll

**Usage**:
```typescript
const flatListRef = useKeyboardScroll(messages, isTyping);
```

**Features**:
- Listens to keyboard events
- Auto-scrolls when keyboard opens
- Auto-scrolls when new message arrives

---

## 12. Setup & Configuration

### Environment Setup

1. **Install Dependencies**:
```bash
npm install
```

2. **Configure API**:
Edit `src/config/api.ts`:
```typescript
export const API_BASE_URL = 'YOUR_BACKEND_URL';
```

3. **Run Development Server**:
```bash
npm start
# or
expo start
```

4. **Run on Device**:
```bash
npm run android  # Android
npm run ios      # iOS
```

### Backend Configuration

**Required Endpoints**:
- POST `/api/auth/register` - User registration
- POST `/api/auth/login` - User login
- GET `/api/auth/me` - Get current user
- POST `/api/chat/message` - Send message (SSE streaming)
- GET `/api/chat/conversations` - List conversations
- GET `/api/chat/conversations/:id/messages` - Get messages
- DELETE `/api/conversations/:id` - Delete conversation

### Build for Production

**Android APK**:
```bash
eas build --platform android --profile preview
```

**iOS IPA**:
```bash
eas build --platform ios --profile preview
```

---

## Summary

The AI Surrogate Mobile App is a production-ready React Native application featuring:

✅ **Modern Architecture**: Modular, type-safe, and maintainable  
✅ **Real-Time Chat**: Streaming AI responses with SSE  
✅ **Rich Features**: TTS, conversation management, authentication  
✅ **Polished UI**: WhatsApp-inspired design with smooth animations  
✅ **Optimized UX**: Loading states, auto-scroll, keyboard handling  
✅ **Scalable**: Clear separation of concerns, reusable components  

The codebase follows React Native and TypeScript best practices, ensuring long-term maintainability and ease of feature additions.
