# covid-chatbot

## Introduction
This repository showcases the working of a Covid-19 information assistant, built with RASA 2.0

The COVID-19 Bot can: 
- Take an Indian pincode/state name/district name as input and provides appropriate covid-19 results 
- Accept the pincode number typed in words (each digit spelled in words)
- Save the last used location and prompt user for reusing the pincode to fetch result
- Fetch the below mentioned information for the specific location based on the pincode provided  
  - Cases in the last 24 hours
  - Deaths in the last 24 hours
  - Recoveries in the last 24 hours
  - Overall cases reported
  - Overall deaths
  - Overall active cases


## Resources used
[Covid19-India API](https://documenter.getpostman.com/view/10724784/SzYXXKmA?version=latest)

[Postal PIN Code API](http://www.postalpincode.in/Api-Details)

## Rasa shell commands

    rasa train
    rasa shell
    rasa run actions -vv //before running this make sure you've also added required config in endpoints.yml
    rasa run -m models --enable-api --cors "*" --debug
    rasa data validate // to check if there are conflicts

## Screenshots

Username given here will be stored

![image](https://user-images.githubusercontent.com/43683444/117583828-06bfb500-b127-11eb-93f5-8d87339a8a2d.png)

----

It can fetch result based on the pincode provided

![image](https://user-images.githubusercontent.com/43683444/117584117-8a2dd600-b128-11eb-8623-6e55c19c9e75.png)

----

Fetch result by providing city name

![image](https://user-images.githubusercontent.com/43683444/117583841-1939ee80-b127-11eb-89ce-4d67976ed8da.png)

----

It can use the username previously stored, and fetch the result even if the pincode is spelled in words

![image](https://user-images.githubusercontent.com/43683444/117583917-88174780-b127-11eb-9cd9-6d5fcb19e79a.png)

----

Bot can handle the city names spelled incorrectly and fetches most appropriate result

![image](https://user-images.githubusercontent.com/43683444/117583990-f5c37380-b127-11eb-899f-e15eccdafee6.png)
