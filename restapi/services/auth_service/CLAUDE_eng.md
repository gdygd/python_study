# CLAUDE.md

This file provides guidance to Claude Code when working with this Python
project.

------------------------------------------------------------------------

# Project Overview

This project is a Python backend service.

Main goals:

-   Clean architecture
-   Maintainable code
-   Testable modules
-   Production-ready logging and error handling

Python version: 3.11+

------------------------------------------------------------------------

# Project Structure
```
project_root/
├── bin
│   └── log
├── CLAUDE.md
├── example 
├── poetry.lock
├── pyproject.toml
├── ref
│   └── db
│       ├── dbhandler.go
│       ├── mdb
│       │   ├── mdb_c.go
│       │   ├── mdbhandler.go
│       │   └── mdb_r.go
│       └── model.go
├── src
│   ├── app
│   │   ├── api
│   │   └── gapi
│   ├── db                          # repository
│   ├── infra
│   ├── main.py                     # 애플리케이션 엔트리포인트
│   ├── proto
│   ├── service                     # 비즈니스 로직
│   └── utils
└── tests

```
Rules:

-   API layer must not access DB directly
-   API → Service → Repository structure
-   Business logic belongs to service layer

------------------------------------------------------------------------

# Coding Guidelines

Follow these rules strictly.

## General

-   Use Python 3.11+ features
-   Follow PEP8
-   Use type hints everywhere
-   Avoid global state
-   Write small functions

Example:

def get_user(user_id: int) -\> User: ...

------------------------------------------------------------------------

# Naming Convention

Variable: snake_case\
Function: snake_case\
Class: PascalCase\
Constant: UPPER_CASE

Example:

user_id\
get_user()\
UserService\
MAX_RETRY

------------------------------------------------------------------------

# Error Handling

Never silently ignore errors.

Bad:

try: do_something() except: pass

Good:

try: do_something() except Exception as e: logger.error("operation
failed", exc_info=e) raise

------------------------------------------------------------------------

# Logging

Use structured logging.

import logging logger = logging.getLogger(**name**)

logger.info("user created", extra={"user_id": user_id})

Log Levels:

DEBUG -- development\
INFO -- normal operation\
WARNING -- unexpected but recoverable\
ERROR -- failures

------------------------------------------------------------------------

# Database Access

Database access must go through repository layer.

Repository example:

class UserRepository: def get_user(self, user_id: int) -\> User: ...

Service example:

class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, user_id: int) -> User:
        return self.repo.get_user(user_id)

------------------------------------------------------------------------

# Testing

Use pytest.

tests/ - test_user_service.py - test_repository.py

Example:

def test_get_user(): user = service.get_user(1) assert user.id == 1

Rules:

-   Every service must have tests
-   Avoid testing private functions
-   Mock external dependencies

------------------------------------------------------------------------

# Dependency Management

Use pip + requirements.txt or poetry.

Install:

pip install -r requirements.txt

------------------------------------------------------------------------

# Formatting

Tools:

black isort flake8

Commands:

black . isort . flake8

------------------------------------------------------------------------

# Security Guidelines

-   Validate all input
-   Never expose stack traces
-   Do not hardcode secrets

Use environment variables:

DATABASE_URL JWT_SECRET REDIS_HOST

------------------------------------------------------------------------

# Pull Request Guidelines

Each PR must include:

-   clear description
-   test coverage
-   no lint errors

------------------------------------------------------------------------

# Summary

Core principles:

-   Clean architecture
-   Separation of concerns
-   Testability
-   Maintainability
