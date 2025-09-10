# Fan or Fraud? (Django University Project)

![Python](https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![SQLite](https://img.shields.io/badge/SQLite-%230073A9.svg?style=for-the-badge&logo=sqlite&logoColor=white)![Bootstrap](https://img.shields.io/badge/Bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

## Description

This repository is a self-made Django project designed to build and showcase web development skills. **Fan or Fraud?** is a user-friendly quiz website about TV programmes. It allows users to test their knowledge on favourite TV shows and programmes, and create their own quizzes for others to try.

*All TV series are pulled from OMDb's movie database via its RESTful web service, meaning any show that exists can have its own quiz.*

## Features

- **User profiles:** Registration and login, custom bio and profile picture via image upload.
- **Quiz creation:** Users can generate their own quizzes, add multiple-choice questions, and manage (update/delete) their quizzes.
- **Quiz application:** Take available quizzes (yours and others), view previous quiz attempts/history, compare with others.
- **Boundless TV Programmes:** Pulls show data from OMDb, so any TV show can have a quiz.
- **Search:** Search for series and quizzes.
- **CRUD support** for quizzes and questions.

## Project Structure

- `project2_root/project2_site/`: Django site logic and settings
- `project2_root/quiz/`: Quiz application (models, views, templates)
- `project2_root/user/`: Custom user profile logic (bio, image upload)
- `project2_root/general/`: General site utilities and configuration
- `project2_root/project2_site/static/`: Static files (CSS, etc.)
- `project2_root/project2_site/templates/`: Site-wide base templates

## Future improvements, tweaks

- Enhance user actions (e.g., mute, ban, richer profile customization)
- Improve quiz editing (e.g., banner image, richer media support)
- More analytics on quiz attempts and comparison
- Dark mode support

---
*CSC1025 - Project 2 by Kensho Mueller-Mark & Amin Loui Osman*
