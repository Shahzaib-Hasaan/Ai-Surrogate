# Building Native App with Speech-to-Text

## Prerequisites
- Node.js and npm installed
- Android Studio (for Android) or Xcode (for iOS)
- Expo CLI installed globally: `npm install -g expo-cli`

## Build Instructions

### Step 1: Prebuild Native Projects
```bash
cd f:\Projects\AI-Surrogate\ai-surrogate-mobile
npx expo prebuild
```

This will generate the `android/` and `ios/` folders with native code.

### Step 2: Run on Android

**Option A: Using Expo**
```bash
npx expo run:android
```

**Option B: Using Android Studio**
1. Open Android Studio
2. Open the `android` folder
3. Wait for Gradle sync to complete
4. Click "Run" button or press Shift+F10

### Step 3: Run on iOS (Mac only)
```bash
npx expo run:ios
```

Or open `ios/AISurrogate.xcworkspace` in Xcode and run.

## Features Available After Native Build

✅ **Speech-to-Text (STT)**
- Press and hold microphone button to record
- Slide left to cancel
- Real-time transcription
- Timer and waveform animation
- Haptic feedback

✅ **Text-to-Speech (TTS)**
- Tap speaker icon on AI messages
- Native voice synthesis

## Troubleshooting

### Android Build Errors
If you get build errors, try:
```bash
cd android
./gradlew clean
cd ..
npx expo run:android
```

### iOS Build Errors
```bash
cd ios
pod install
cd ..
npx expo run:ios
```

### Permission Issues
Make sure these permissions are in:
- **Android**: `android/app/src/main/AndroidManifest.xml`
  ```xml
  <uses-permission android:name="android.permission.RECORD_AUDIO" />
  ```

- **iOS**: `ios/AISurrogate/Info.plist`
  ```xml
  <key>NSMicrophoneUsageDescription</key>
  <string>This app needs microphone access for voice input</string>
  <key>NSSpeechRecognitionUsageDescription</key>
  <string>This app needs speech recognition for voice-to-text</string>
  ```

## Testing Voice Features

1. Build and run the app natively
2. Open a chat
3. Press and hold the microphone button
4. Speak your message
5. Release to send or slide left to cancel
6. Tap speaker icon on AI messages to hear TTS

## Creating APK for Distribution

```bash
cd android
./gradlew assembleRelease
```

APK will be at: `android/app/build/outputs/apk/release/app-release.apk`
