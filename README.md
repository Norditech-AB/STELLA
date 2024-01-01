# Updating the docs

## Cleanup the docs
```bash
$ ./cleanup.sh
```


## Build the docs

```bash
$ cd docs
$ make html
```

## Copy the docs to the root of the repo

```bash
$ cd docs
$ cp -r _build/html/* ../
```

## Commit and push

```bash
$ git add .
$ git commit -m "Update docs"
$ git push
```

## All in one

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