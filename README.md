# Athlete Nutritional & Training Recovery Dashboard

> Group 6

official System logo:

![alt text](./Kaguya.gif)

## Members

- Bazar, Cyrus Troy C. [(AlieeLinux)](https://github.com/alieelinux)
- Serrano Joshua
- Imperial Jl
- Salamatin

## 💯 Progressions

- title: ✅
- Project Description: Okayish ✅❓
- Objective of the system: Okayish ✅❓
- Business Rule: Planning ❌
- Entity relationship diagram: Semi done ❌
- Normalization summary: Undone ❌
- System Features: Planning ❌

---

**table of contents:**

- [Athlete Nutritional \& Training Recovery Dashboard](#athlete-nutritional--training-recovery-dashboard)
  - [Members](#members)
  - [💯 Progressions](#-progressions)
  - [📌 Introduction](#-introduction)
  - [📖 Project Description](#-project-description)
  - [🎯 Objective of the System](#-objective-of-the-system)
  - [⬇️ Installation](#️-installation)
    - [Instal mariadb from official mariadb site (Mysql support soon)](#instal-mariadb-from-official-mariadb-site-mysql-support-soon)
    - [start the mariadb server](#start-the-mariadb-server)

## 📌 Introduction

Athlete Nutritional & Training Recovery Dashboard is a lightweight and efficient monitoring designed for athletes to track their health and stuffs

This project reflects a preference for performance, transparency, and control, inspired by Linux-based workflows and terminal.

---

## 📖 Project Description

The Athlete Nutritional & Training Recovery Dashboard is a database-driven application that allows students and administrators to:

- Monitor Nutrition logs
- training_sessions
- recovery_logs
- recovery_logs

It is designed to be simple, fast, and practical—no unnecessary garbage features.

## 🎯 Objective of the System

- Centralized Athlete Data Management
- Support for CRUD Operations
- Data Organization Through Relational Database Design
- Performance and Health Monitoring
- Data-Driven Insights Generation
- User-Friendly Command-Line Interface and web app interface
- Foundation for Future Expansion

## ⬇️ Installation

### Instal mariadb from official mariadb site (Mysql support soon)

- [https://mariadb.org/download/](https://mariadb.org/download/)

### start the mariadb server

- **Windows Services (Recommended):**
  - Press Win + R, type services.msc, and hit Enter.
Locate the MariaDB service (often named MariaDB or MySQL). Right-click and select Start.

- **cmd**
  - Run this on cmd or powershell as administrator

    ```ps1
    net start mysql
    ```

- **Linux Via systemd**
  - open your terminal and run

    ```bash
    sudo systemctl start mariadb
    ```

  - or enable it on boot

    ```bash
    sudo systemctl enable --now mariadb
    ```

![Kaguya](https://media1.tenor.com/m/klBPU9I_898AAAAC/mokou-kaguya.gif)
