# Updating the docs

## Cleanup the docs
MacOS/Unix
```bash
$ ./cleanup.sh
```

Windows
```bash
$ cleanup.bat
```

## Build the docs

```bash
$ cd docs
$ make html
```

## Copy the docs to the root of the repo

MacOS/Unix
```bash
$ cd docs
$ cp -r _build/html/* ../
```

Windows
```bash
$ cd docs
$ xcopy _build\html\* ..\ /E /I

```
## Commit and push

```bash
$ git add .
$ git commit -m "Update docs"
$ git push
```

## All in one

MacOS/Unix
```bash
$ ./cleanup.sh
$ cd docs
$ make html
$ cp -r _build/html/* ../
$ cd ..
$ git add .
$ git commit -m "Update docs"
$ git push
```

Windows
```bash
$ cleanup.sh
$ cd docs
$ make html
$ xcopy _build\html\* ..\ /E /I
$ cd ..
$ git add .
$ git commit -m "Update docs"
$ git push
```