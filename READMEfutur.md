# ArchTrack System

> Group 6

- [ArchTrack System](#archtrack-system)
  - [📌 Introduction](#-introduction)
  - [📖 Project Description](#-project-description)
  - [🎯 Objective of the System](#-objective-of-the-system)
  - [📏 Business Rules](#-business-rules)
  - [🗂️ ER Diagram Section](#️-er-diagram-section)
  - [🧮 Normalization Summary](#-normalization-summary)
  - [⚙️ System Features](#️-system-features)

![Kaguya](https://media1.tenor.com/m/klBPU9I_898AAAAC/mokou-kaguya.gif)

## 📌 Introduction

ArchTrack System is a lightweight and efficient student activity and system monitoring platform designed for academic environment

This project reflects a preference for performance, transparency, and control, inspired by Linux-based workflows and terminal>

---

## 📖 Project Description

The ArchTrack System is a database-driven application that allows students and administrators to:

- Monitor student activity logs
- Track academic tasks and submissions
- Manage user profiles
- Provide system-level insights (CPU usage, uptime, etc.)

It is designed to be simple, fast, and practical—no unnecessary garbage features.

## 🎯 Objective of the System

- To create a centralized system for managing student activities
- To provide real-time monitoring of system usage
- To ensure efficient tracking of academic progress
- To promote transparency between students and administrators
- To minimize system overhead while maintaining functionality

---

## 📏 Business Rules

1. Each student must have a unique ID
2. A student can have multiple activity logs
3. Each activity log must be linked to exactly one student
4. Tasks can be assigned to multiple students
5. Each task must have a deadline and status
6. Administrators have full control over system data
7. System logs must be stored securely and cannot be altered by students

---

## 🗂️ ER Diagram Section

Entities included in the system:

- --Student-- (StudentID, Name, Username, Role)
- --ActivityLog-- (LogID, Timestamp, CPU_Usage, Memory_Usage, StudentID)
- --Task-- (TaskID, Title, Description, Deadline, Status)
- --Submission-- (SubmissionID, TaskID, StudentID, DateSubmitted)
- --Admin-- (AdminID, Name, AccessLevel)

Relationships:

- A Student generates multiple ActivityLogs (1:N)
- A Student can have multiple Submissions (1:N)
- A Task can have multiple Submissions (1:N)
- Admin manages Students and Tasks (1:N)

---

## 🧮 Normalization Summary

- --1NF (First Normal Form):--
  All attributes contain atomic values; no repeating groups

- --2NF (Second Normal Form):--
  All non-key attributes fully depend on the primary key

- --3NF (Third Normal Form):--
  No transitive dependencies; data is logically structured

Result: The database is optimized, reducing redundancy and improving consistency.

---

## ⚙️ System Features

- 📊 Real-time system monitoring (CPU, Memory usage)
- 📝 Task and submission management
- 👤 Student profile handling
- 🔐 Role-based access (Admin & Student)
- 📁 Activity logging and tracking
- ⚡ Lightweight and efficient performance
- 🖥️ Terminal-friendly design (optional interface)

---
