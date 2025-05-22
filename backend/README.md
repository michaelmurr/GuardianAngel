## How to work with it

### After you clone this repo create a virtual environment:

win/mac
```console
$ python -m venv .venv
```

---

### Activate it:

win
```console
$ .venv\Scripts\Activate.ps1
```

mac
```console
$ source .venv/bin/activate
```

---

### Check the Virtual Environment is Active:

win
```console
$ Get-Command python
```

mac
```console
$ which python
```

<br>

> [!NOTE]
> If it shows the python binary at .venv\Scripts\python, inside of your project, then it worked.

---

### Upgrade pip:

```console
$ python -m pip install --upgrade pip
```

---

### Install Packages from `requirements.txt`:

```console
$ pip install -r requirements.txt
```

---

### Run the server:

```console
$ python -m uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['M:\\dev\\boarded-backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [10656] using WatchFiles
INFO:     Started server process [4016]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

<br>

> [!IMPORTANT]
> Once you are done working on your project you should deactivate the virtual environment.
> ```console
> $ deactivate
> ```

Reference [fastapi Docs](https://fastapi.tiangolo.com/virtual-environments/#__tabbed_3_2).
