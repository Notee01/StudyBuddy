#updating the packages
pip freeze > requirements.txt

#python env variable and pip freeze
python -m venv djenv
pip freeze -l > requirement.txt
pip install -r requirement.txt

#uploading
git status
git add .
git commit -m " "
git push origin master

#update to the original
git remote add upstream https://github.com/Notee01/Thesis-V1
git fetch upstream
git rebase upstream/master
git add .
git pull --rebase --autostash


circular import

{% for lesson in topic.lesson_topic.all %}