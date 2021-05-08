# covid-chatbot

## Introduction
This repository showcases the working of a Covid-19 information assistant, built with RASA 2.0

The COVID-19 Bot can: 
- Take an Indian pincode as input and provide the covid-19 results 
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
