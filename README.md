# UCSB Dining Assistant (alpha)
What if you could ask Alexa/Siri/Google Assistant where to eat and didn't have to compare the menus for 15 minutes? The goal of this application is just that!

How I got everything working:
1. started with clean ubuntu 18.04 bionic
2. installed python 3.7, pip, virtualenv, virtualenvwrapper
3. ```mkvirtualenv -a $(pwd) <env_name> -p python3.7``` (the cloud function environment im using is Flask on Python 3.7)
4. ```pip install --upgrade -r requirements.txt``` (maybe u can omit the ```--upgrade``` and be ok)
5. within the environment, do ```export FLASK_APP=test.py``` and ```export FLASK_ENV=development``` if you want to test locally. Then, install Postman and fire away

when you're done working you can ```deactivate```
if you want to reactivate the environment you can ```workon <env_name>```

# DialogFlow Intent Diagram (WIP)
![](https://docs.google.com/drawings/d/e/2PACX-1vTviOrDJjXIpIJMNTu0EwzUuZTDcktKyzeMU3uwPekKSnpcMCXgnUmxq3ATpGJOW6YO0jJC3eMRWIah/pub?w=1440&h=1080)

please let me know if you think this could be done better i'm just winging it
