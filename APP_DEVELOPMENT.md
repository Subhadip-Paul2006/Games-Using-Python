# 📱 Games Platform — Application Development

<p align="center">
  <img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white" alt="Flutter"/>
  <img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white" alt="Dart"/>
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" alt="Firebase"/>
  <img src="https://img.shields.io/badge/Cloud_Firestore-FFA000?style=for-the-badge&logo=firebase&logoColor=white" alt="Firestore"/>
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="CI"/>
  <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white" alt="Figma"/>
</p>

<p align="center">
  <strong>The official roadmap for transforming the Python game collection into a unified cross-platform application using <em>Flutter</em> &amp; <em>Firebase</em>.</strong>
</p>

> 📌 This file documents the **Application** layer of the project.
> For the underlying Python game prototypes, see the [main README](./README.md).

---

## 🎯 Mission

Re-build the existing Python game prototypes (Snake, Tetris, Flappy Bird, Hangman, MineSneeker, Rock Paper Scissors, Tic Tac Toe, Pong) as **one polished cross-platform application** that runs on **Android, iOS and the Web** from a single Flutter codebase, backed by **Firebase** for authentication, real-time leaderboards, profiles and cloud sync.

```text
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   Python Prototypes  ──►  Flutter App  ──►  Firebase Backend     │
│   (logic reference)       (UI + Logic)      (Auth + DB + Funcs)  │
│                                                                  │
│                ▼                ▼                ▼               │
│            Android           iOS / Web        Real-time          │
│                                              Leaderboards        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🧰 Tech Stack & Tools

### 🧑‍💻 Core Languages & Frameworks

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Flutter 3.x | Cross-platform UI (Android / iOS / Web) |
| **Language** | Dart 3.x | Application logic |
| **State Management** | Riverpod / Bloc | Predictable state & dependency injection |
| **Animations** | Flame Engine, Rive, Lottie | Game rendering & micro-interactions |
| **Game Loop** | Flame 1.x | 2D game engine for Flutter |

### ☁️ Firebase Services

| Service | Purpose |
|---------|---------|
| 🔐 **Firebase Authentication** | Email / Google / Anonymous login |
| 🗄️ **Cloud Firestore** | Profiles, scores, match history, leaderboards |
| ⚡ **Cloud Functions** | Score validation, anti-cheat, daily challenges |
| 📁 **Firebase Storage** | Avatars, custom skins, downloadable assets |
| 📲 **Cloud Messaging (FCM)** | Push notifications & challenges |
| 📊 **Firebase Analytics** | User journeys & retention |
| 🐞 **Crashlytics** | Real-time crash reporting |
| 🌐 **Firebase Hosting** | Web build deployment |
| 🧪 **Remote Config** | Feature flags, A/B testing |

### 🛠️ Dev & Ops Tooling

| Tool | Use |
|------|-----|
| **Android Studio / VS Code** | IDE + Flutter plugins |
| **Figma** | UI/UX design & prototyping |
| **GitHub + GitHub Actions** | Version control & CI/CD |
| **Codemagic / Fastlane** | Automated builds & store publishing |
| **Postman** | Cloud Function endpoint testing |
| **Sentry / Crashlytics** | Error monitoring |
| **Jira / GitHub Projects** | Task tracking |
| **Discord / Slack** | Team communication |

---

## 🏗️ Application Architecture

```mermaid
flowchart TB
    subgraph Mobile["📱 Flutter Client (Android / iOS / Web)"]
        UI[Presentation Layer<br/>Widgets + Screens]
        STATE[State Layer<br/>Riverpod / Bloc]
        DOMAIN[Domain Layer<br/>Game Logic + Models]
        DATA[Data Layer<br/>Repositories]
    end

    subgraph Firebase["☁️ Firebase Backend"]
        AUTH[🔐 Authentication]
        FS[(🗄️ Firestore)]
        FN[⚡ Cloud Functions]
        ST[📁 Storage]
        FCM[📲 FCM]
        AN[📊 Analytics]
    end

    UI <--> STATE
    STATE <--> DOMAIN
    DOMAIN <--> DATA
    DATA <--> AUTH
    DATA <--> FS
    DATA <--> ST
    DATA -.-> FN
    DATA -.-> FCM
    UI -.-> AN
```

### Clean Architecture Layers

```text
lib/
├── core/                # constants, themes, utils, routing
├── data/                # Firebase repositories & DTOs
├── domain/              # entities, use-cases, abstract repos
├── presentation/        # screens, widgets, controllers
│   ├── auth/
│   ├── home/
│   ├── games/
│   │   ├── snake/
│   │   ├── tetris/
│   │   ├── flappy/
│   │   ├── hangman/
│   │   ├── minesweeper/
│   │   ├── rps/
│   │   ├── tic_tac_toe/
│   │   └── pong/
│   ├── leaderboard/
│   └── profile/
└── main.dart
```

---

## 🗺️ Detailed Roadmap

```mermaid
gantt
    title Games-Using-Python — Flutter Application Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b %Y

    section Phase 0 — Foundation
    Requirement gathering        :done,   p0a, 2026-06-20, 10d
    UI/UX design in Figma        :active, p0b, 2026-07-01, 30d
    Firebase project setup       :        p0c, 2026-07-10, 15d

    section Phase 1 — Skeleton
    Flutter project scaffold     :        p1a, 2026-08-01, 14d
    Routing + theming            :        p1b, 2026-08-10, 14d
    Auth (email + Google)        :        p1c, 2026-08-20, 21d

    section Phase 2 — Game Modules
    Snake Game (Flame)           :        p2a, 2026-09-15, 25d
    Tic Tac Toe                  :        p2b, 2026-10-01, 18d
    Hangman                      :        p2c, 2026-10-10, 18d
    Rock Paper Scissors          :        p2d, 2026-10-20, 15d
    MineSneeker                  :        p2e, 2026-11-01, 25d
    Flappy Bird (Flame)          :        p2f, 2026-11-15, 25d
    Tetris (Flame)               :        p2g, 2026-12-01, 30d
    Pong (multiplayer)           :        p2h, 2026-12-20, 25d

    section Phase 3 — Backend Features
    Firestore data modelling     :        p3a, 2026-09-15, 20d
    Global leaderboard           :        p3b, 2026-10-15, 25d
    Profile + avatar             :        p3c, 2026-11-05, 20d
    Cloud Functions (anti-cheat) :        p3d, 2026-12-01, 25d

    section Phase 4 — Polish
    Theming + animations         :        p4a, 2027-01-05, 25d
    Sound + haptics              :        p4b, 2027-01-15, 18d
    Localization (i18n)          :        p4c, 2027-02-01, 18d

    section Phase 5 — Release
    QA + automated tests         :        p5a, 2027-02-15, 21d
    Closed beta (TestFlight/Play):        p5b, 2027-03-05, 21d
    Public release v1.0          :crit,   p5c, 2027-04-01, 7d
    Post-launch support          :        p5d, 2027-04-08, 60d
```

### Phase-by-Phase Breakdown

#### 🟣 Phase 0 — Foundation & Design *(June – July 2026)*
- Define MVP scope & user personas
- Wireframe every screen in **Figma** (low-fi → hi-fi)
- Build the **design system**: colors, typography, spacing, components
- Create the **Firebase project**, enable Auth + Firestore + Storage
- Lock the **app name**, logo and store presence

#### 🔵 Phase 1 — Skeleton *(August 2026)*
- `flutter create` with null-safety & sound migration
- Configure flavors (dev / staging / prod)
- Set up routing (`go_router`), theming (light / dark), L10n bootstrap
- Implement Auth screens (Sign-in, Sign-up, Forgot password, Anonymous)
- Wire Firebase SDK + secure config via `flutter_dotenv`

#### 🟢 Phase 2 — Game Modules *(September – December 2026)*
Each game is its own Flutter package under `lib/presentation/games/<name>/` with:
- Game state machine
- Flame component tree (for arcade games) or plain widgets (for board games)
- Per-game settings, controls, tutorial
- Local high score + Firestore sync hook

#### 🟡 Phase 3 — Backend Features *(September – December 2026, parallel)*
- Firestore schema: `users`, `scores`, `matches`, `daily_challenges`
- Security rules with unit tests via `@firebase/rules-unit-testing`
- Real-time leaderboard with pagination
- Cloud Functions for score validation & anti-cheat
- Daily / weekly challenge generator

#### 🟠 Phase 4 — Polish *(January – February 2027)*
- Implicit & hero animations
- Sound (Just Audio) + haptic feedback
- Accessibility (semantics, contrast, font scaling)
- Localization (English + Hindi + Bengali to start)
- Performance pass: tree shaking, lazy routes, image caching

#### 🔴 Phase 5 — Release *(February – April 2027)*
- Unit, widget, golden & integration tests (target ≥ 70% coverage)
- Closed beta via **TestFlight** & **Play Console internal track**
- Crashlytics & Analytics dashboards reviewed weekly
- Submission to **Play Store**, **App Store**, **Web** (Firebase Hosting)
- Post-launch: weekly patches, feature flags via Remote Config

---

## 👥 Team & Task Division

```mermaid
mindmap
  root((Application Team))
    Subhadip Paul
      Lead Developer
      Firebase Architecture
      Cloud Functions
      DevOps / CI-CD
      Code Review
    Abhishek
      Flutter Frontend
      UI Implementation
      Animations
      Game UI Integration
    Samhita
      UI/UX Design
      Game Logic Port
      QA & Testing
      Asset Management
```

### 🧑‍✈️ Subhadip Paul — *Lead Developer & Backend Engineer*

> **Focus:** architecture, Firebase, infrastructure, code review.

| Area | Responsibilities |
|------|------------------|
| 🏗️ Architecture | Define clean-architecture layers, repositories, dependency graph |
| 🔐 Firebase Backend | Configure Auth providers, Firestore schema, security rules |
| ⚡ Cloud Functions | Score validation, leaderboard aggregation, daily challenges |
| 🚀 DevOps | GitHub Actions, build flavors, signing, Codemagic/Fastlane |
| 📈 Monitoring | Crashlytics, Analytics, Remote Config |
| 🧪 Backend Tests | Firestore rules tests, Functions emulator tests |
| 👀 Code Review | Final approver on all PRs touching `data/` & `domain/` |

**Key deliverables**
- ✅ Firebase project + security rules
- ✅ `data/` & `domain/` layers fully implemented
- ✅ CI/CD pipeline with automated APK + Web build
- ✅ Cloud Functions deployed & monitored

---

### 🎨 Abhishek — *Flutter Frontend Engineer*

> **Focus:** screens, widgets, navigation, game UI shell.

| Area | Responsibilities |
|------|------------------|
| 🖼️ Presentation Layer | Build every screen from Figma to pixel-perfect Flutter |
| 🎬 Animations | Hero transitions, micro-interactions, Lottie / Rive |
| 🧭 Navigation | `go_router` setup, deep links, route guards |
| 🎮 Game UI Shell | Wrappers, HUDs, pause / game-over overlays |
| 🌗 Theming | Light / dark mode, dynamic theming |
| 🧩 Reusable Widgets | Buttons, cards, dialogs, leaderboards |
| 📱 Responsive Design | Phone, tablet & web breakpoints |

**Key deliverables**
- ✅ Auth flow screens
- ✅ Home, Profile, Leaderboard, Settings screens
- ✅ Reusable widget library
- ✅ Per-game UI shells (HUD, pause menu, scoreboard)

---

### 🧪 Samhita — *UI/UX Designer & QA Lead*

> **Focus:** design system, game logic porting, testing.

| Area | Responsibilities |
|------|------------------|
| ✏️ Design | Figma wireframes, mockups, prototypes, design system |
| 🖌️ Assets | Icons, splash, sprites, sound assets, store graphics |
| 🕹️ Game Logic Port | Translate Python game logic → Dart use-cases |
| 🌍 Localization | Manage translation files (EN / HI / BN) |
| 🐛 QA & Testing | Manual test plans, widget tests, golden tests, bug triage |
| 📦 Beta Coordination | TestFlight / Play internal track, gathering tester feedback |
| 📚 Documentation | User guide, FAQ, in-app onboarding copy |

**Key deliverables**
- ✅ Complete Figma design system
- ✅ Dart ports of all 8 game logics (pure Dart, no UI)
- ✅ Test suites for every game module
- ✅ Localization + accessibility audit

---

### 🤝 Shared Responsibilities

| Activity | Everyone |
|----------|---------|
| 🔁 Daily stand-ups (15 min) | ✅ |
| 📝 Sprint planning (every 2 weeks) | ✅ |
| 🧐 Code reviews (cross-team) | ✅ |
| 📚 Documentation upkeep | ✅ |
| 🐞 Bug bashing before release | ✅ |

---

## 🧪 Quality Strategy

```mermaid
flowchart LR
    DEV[Local Dev] --> LINT[Dart Analyzer]
    LINT --> UNIT[Unit Tests]
    UNIT --> WIDGET[Widget Tests]
    WIDGET --> GOLDEN[Golden Tests]
    GOLDEN --> INT[Integration Tests]
    INT --> CI{CI: GitHub Actions}
    CI -->|pass| BETA[Closed Beta]
    CI -->|fail| DEV
    BETA --> PROD[Production Release]
```

- **Lint:** `flutter_lints` + custom rules
- **Format:** `dart format` on pre-commit hook
- **Tests:** target ≥ 70% coverage across `domain/` & `data/`
- **CI:** every PR runs analyze + tests + build (Android + Web)
- **Beta:** Play Console internal + TestFlight before each release

---

## 🚀 Getting Started (for contributors)

```bash
# 1. Clone the repo
git clone https://github.com/Subhadip-Paul2006/Games-Using-Python.git
cd Games-Using-Python/app

# 2. Install Flutter (3.x) and verify
flutter doctor

# 3. Install dependencies
flutter pub get

# 4. Configure Firebase
flutterfire configure

# 5. Run on a connected device or emulator
flutter run

# 6. Run tests
flutter test
```

> 🔑 Ask **Subhadip** for the `dev` Firebase project access before running.

---

## 📦 Release Channels

| Channel | Audience | Trigger |
|---------|----------|---------|
| `dev` | Developers only | Every push to `develop` |
| `staging` | Internal team | Tagged `v*-beta` |
| `production` | Public | Tagged `v*` on `main` |

---

## 📜 License

This application is part of the **Games-Using-Python** project and is distributed under the **MIT License**. See [`LICENSE`](./LICENSE).

---

<p align="center">
  Crafted with 💙 by the <strong>Games-Using-Python Application Team</strong><br/>
  <a href="https://github.com/Subhadip-Paul2006">Subhadip Paul</a> · Abhishek · Samhita
</p>
