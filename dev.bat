@echo off
set ARG=%1
IF DEFINED ARG (
    IF "%ARG%"=="-p" (
        git pull origin main
    ) ELSE (
        git pull origin dev
    )
) ELSE (
    git pull origin dev
) 