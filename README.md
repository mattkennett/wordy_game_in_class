# Wordy Game

Wordy Game is a hangman-style word puzzle. Users will be given a category and shown the blank spaces representing the
letters of a puzzle. They will guess until they miss three times or successfully solve the puzzle.

## Data Model

### WordyUser (child of django.contrib.auth.models.AbstractUser)

- favorite_color : String (optional)
- score: Int (property)

## Site Functional Areas

### User Management

- Register New Users
- Log In / Log Out
- Update Existing Users

### View All Games

- Show new game form
- List all of the user's existing games

### View Game Instance

- Show game state and status (Win, Lose, In Progress)
- While game is In Progress, accept one character at a time as input to update state

### View Leaderboard

- Show list of all users sorted by the user's score (paginated with 50 users at a time)