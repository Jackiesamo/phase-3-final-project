
# Budget Tracker

## Description

The Budget Tracker is a Python CLI application that helps users manage their personal finances by recording income, expenses, categories, and transaction history. All data is stored in a SQLite database, allowing users to maintain an accurate and persistent financial record.

## Author

Jacklyne owuor

## Setup Instructions

1. Clone this repository
2. Navigate into project directory
3. Install pipenv if not already installed
4. Create and activate the virtual environment


## BDD (Behavior Driven Development)

1. Input: Income amount and description

Output: Income added and stored in the database

2. Input: Expense amount, category, and description

Output: Expense recorded and saved in the database

3. Input: Invalid amount (negative or non-numeric)

Output: Error message requesting valid input

4. Input: View all transactions

Output: List showing dates, types, categories, and amounts

5. Input: View current balance

Output: Balance calculated as total income minus total expenses

6. Input: Exit application

Output: Program closes successfully



## Technologies Used
. Python 3.x

. SQLite

. Pipenv

. Pytest

. Object-Oriented Programming (OOP)

## Contact Information

GitHub: https://github.com/Jackiesamo
## License


MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.