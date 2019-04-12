# UCSB Dining Assistant (alpha)
what if you could just ask your phone/iot thing where to eat and didn't have to compare the menus for 15 minutes (or is that just me???)
- if you're better at dialogflow and google cloud stuff please contact me

how i got everything working
1. started with clean ubuntu 18.04 bionic
2. installed python 3.7, pip, virtualenv, virtualenvwrapper
3. ```mkvirtualenv -a $(pwd) <env_name> -p python3.7``` (the cloud function environment im using is Flask on Python 3.7)
4. ```pip install --upgrade -r requirements.txt``` (maybe u can omit the ```--upgrade``` and be ok)
5. within the environment, do ```export FLASK_APP=test.py``` and ```export FLASK_ENV=development``` if you want to test locally. Then, install Postman and fire away

when you're done working you can ```deactivate```
if you want to reactivate the environment you can ```workon <env_name>```

