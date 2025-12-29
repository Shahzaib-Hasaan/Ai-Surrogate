# Building APK for Your Android Phone (No Android Studio Required!)

## Quick Method: Using EAS Build (Easiest!)

### Step 1: Install EAS CLI
```bash
npm install -g eas-cli
```

### Step 2: Login to Expo
```bash
eas login
```
(Create a free Expo account if you don't have one)

### Step 3: Configure EAS
```bash
cd f:\Projects\AI-Surrogate\ai-surrogate-mobile
eas build:configure
```

### Step 4: Build APK
```bash
eas build --platform android --profile preview
```

This will:
- Build your app in the cloud (free!)
- Generate an APK file
- Give you a download link

### Step 5: Install on Your Phone
1. Download the APK from the link EAS provides
2. Transfer to your phone (or download directly on phone)
3. Enable "Install from Unknown Sources" in phone settings
4. Tap the APK to install
5. Done! 🎉

---

## Alternative: Local Build (If you want to build locally)

### Prerequisites
1. **Install Java JDK 17**
   - Download from: https://www.oracle.com/java/technologies/downloads/#java17
   - Set JAVA_HOME environment variable

2. **Install Android SDK Command Line Tools**
   - Download from: https://developer.android.com/studio#command-tools
   - Extract to `C:\Android\cmdline-tools`
   - Set ANDROID_HOME to `C:\Android`

3. **Set Environment Variables**
   ```powershell
   # Add to System Environment Variables:
   ANDROID_HOME=C:\Android
   JAVA_HOME=C:\Program Files\Java\jdk-17
   
   # Add to PATH:
   %ANDROID_HOME%\cmdline-tools\latest\bin
   %ANDROID_HOME%\platform-tools
   %JAVA_HOME%\bin
   ```

### Build APK Locally
```bash
cd f:\Projects\AI-Surrogate\ai-surrogate-mobile\android
.\gradlew assembleRelease
```

APK location: `android\app\build\outputs\apk\release\app-release.apk`

---

## Recommended: Use EAS Build

**Why EAS Build is better:**
- ✅ No Android Studio installation needed
- ✅ No SDK setup required
- ✅ Builds in the cloud (free tier available)
- ✅ Works on any computer
- ✅ Generates signed APK automatically
- ✅ Much faster and easier

**Free Tier Limits:**
- 30 builds per month for free
- More than enough for development!

---

## Testing Voice Features

Once installed on your phone:

1. **Open the app**
2. **Login/Register**
3. **Go to Chat**
4. **Press & hold microphone button** 🎤
5. **Speak your message**
6. **Release to send** or **slide left to cancel**
7. **Tap speaker icon** 🔊 on AI messages to hear TTS

---

## Troubleshooting

### "App not installed" error
- Enable "Install from Unknown Sources"
- Settings → Security → Unknown Sources → Enable

### Voice features not working
- Grant microphone permission when prompted
- Check Settings → Apps → AI Surrogate → Permissions → Microphone

### Build failed on EAS
- Make sure you're logged in: `eas whoami`
- Check your internet connection
- Try again: `eas build --platform android --profile preview --clear-cache`
