# Meeting Insights iOS App

Native SwiftUI iOS application for capturing and managing meeting insights.

## Features

- Real-time meeting recording with audio capture
- Streaming transcription and insights
- Offline cache with Core Data
- Background upload support
- Secure token storage with Keychain

## Requirements

- iOS 16.0+
- Xcode 15.0+
- Swift 5.9+

## Setup

1. Open `MeetingInsights.xcodeproj` in Xcode
2. Configure API endpoint in `Services/APIClient.swift`
3. Build and run

## Architecture

- **MVVM**: ViewModels handle business logic
- **Combine**: Reactive data flow
- **Core Data**: Local persistence
- **URLSession**: Network layer with background tasks

## Project Structure

```
MeetingInsights/
├── Views/          # SwiftUI views
├── ViewModels/     # View models
├── Services/       # API client, recording service
├── Models/         # Data models
└── Utils/          # Utilities
```

## Development

The iOS app is currently a placeholder structure. Full implementation includes:

- Recording service with AVAudioRecorder
- WebSocket client for real-time updates
- Core Data models for offline sync
- Authentication flow
- Meeting list and detail views

