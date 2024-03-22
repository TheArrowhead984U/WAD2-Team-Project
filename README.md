# Melody Meter



## Description

MelodyMeter, developed by Team 7C, is a comprehensive average album review platform designed with Python and the Django framework. It gives user to access to default save albums and then user can review each song seperatly. And this review of each song gives average review of whole profile. MelodyMeter also gives user to add new album according to their choice. It also show every album which user rated under its profile.

## Features

- **Search Albums:** Search Music Album and see lyrics of each song available inside album and also add album according to his choice.
- **Reviews:** Allow user to review each song and give average album rating

## Installation Instructions

Ensure you have Conda and Python installed on your system before proceeding.

1. **Clone the Repository**

```bash
git clone < https://github.com/TheArrowhead984U/WAD2-Team-Project.git >
cd WAD2-Team-Project
```

2. **Activate a Virtual Environment**

```bash
conda activate rango
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Database Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Populate the Database**

```bash
python population_script.py
```

6. **Run the Server**

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your web browser to access the application.

## Contribution Guidelines

1. Fork this repository.
2. Clone your forked repository to your local machine.
3. Make your changes and test them locally.
4. Commit your changes with a clear commit message.
5. Push your changes to your fork.
6. Submit a pull request to the original repository.
7. Wait for your pull request to be reviewed and merged.

## Acknowledgments

- 'ytmusicapi' to get albums and song details 

## Team 8D Members

- Thomas Collins
- Andrew Wilson
- Cara Bowes
- Utkarsh Agrawal

