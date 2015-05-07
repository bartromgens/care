cd ..
git checkout v0.2.2 
python manage.py migrate --fake-initial 
git checkout v0.2.3 
python manage.py migrate
git checkout v0.2.4 
python manage.py migrate
git checkout v0.2.5 
python manage.py migrate