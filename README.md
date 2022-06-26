# What's the prupose of Betterlife ?
Berttelife is a Django API used to keep track and manage projects created by organizations/NGOs.
The API was created with DRF (Django Rest Framework).
You can access the list of all the available endpoints of the API here : https://documenter.getpostman.com/view/11214441/UzBsHQFj

# How to setup the API locally ?
Follow the following steps:
1. Clone this repo locally : ```gh repo clone Virgin75/codoc-virgin``` (via GitHub CLI) and then ```cd codoc-virgin/betterlife```
2. Create a virtual env and activate it : ```python3 -m venv -env``` and ```source env/bin/activate```
3. Install the dependencies : ```pip3 install -r requirements.txt```
4. Make the migrations, migrate and run the test server : ```python manage.py makemigrations && python manage.py migrate && python manage.py runserver"
5. Create a super user if needed : ```python manage.py createsuperuser```

You can access the admin interface here : http://127.0.0.1:8000/admin/
