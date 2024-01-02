./cleanup.sh
cd docs
make html
cp -r _build/html/* ../
cd ..
git add .
git commit -m "Update docs"
git push
