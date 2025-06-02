# Storify

## About

Storify is a FastAPI based file storage server which allows users to upload files and share them via a URL. 

## Features

- Fast and simple hosting of static files
- Authentication for Users to manage their stored assets.
- Protected resources which require a valid JWT to be accessed. Protected resources could be profile pictures, user-specific content etc.

## How to start

### Debian (and its derivates)

Requirements:

- A working python3 installation
- CLI access

Setup:

- Create a venv using `python3 venv .venv`
- Activate via `source .venv/bin/activate`
- Execute `pip install .`   install the dependencies.
- Finally run `uvicorn api.main:app` to launch the api.

## Windows

Requirements:

- A working python3 installation
- Access to CMD


- Create a venv using `python3 venv .venv`
- Activate via `.venv\Scripts\activate`
- Execute `pip install .`   install the dependencies.
- Finally run `uvicorn api.main:app` to launch the api.

>  [!IMPORTANT]
> **Powershell execution policy**
> 
> If you encounter an issue with activating your venv on windows, please refer to following StackOverflow discussion: https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows
>
> **Missing VS C++ Build tools**
> 
> Sometimes the C++ build tools are not installed on Windows.
> Those need to be installed first. Please refer to following discussion:
>  
> https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst
>

## Debian support

in future versions when the API runs stable, I will package this application for Debian which should simplify the setup process alot.

