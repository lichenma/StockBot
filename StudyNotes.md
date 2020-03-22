# Description 

Stock bot was a weekend project designed to get some beginner context on stock trading using python bots. 


This project was done following an awesome blog post by [Roman Paolucci](https://medium.com/swlh/build-an-ai-stock-trading-bot-for-free-4a46bec2a18) - purely for learning purposes. 


# Quantitative Trading 

Algorithmic trading is increasing in popularity as new technology emerges making it more accessible to more quantitative investors. Python is something worth investigating with its powerful analytical libraries with easy to understand documentation and implementation. This project is aimed at developing an introductory knowledge to core component of developing an algorithmic trading system as well as deploying a trained AI model to execute live trades.  



# Table of Contents 

The project will be broken up into five main steps: 

1. Connecting to a Brokerage House 
2. Trading System Development 
3. AI Trading Model Development 
4. AI Trading Model Deployment 
5. Cloud Deployment 



# Connecting to a Brokerage House 

The beginning step is to connect to a brokerage house which would allow us to receive live data about the securities we are interested in trading. For this project we will be using `Alpaca` which is one of the easiest platforms to begin AI trading. It allows us to do paper trading an monitor progress which is awesome! Create an account and generate an API key. 


Now that we have the API key we can add it to our `Stock_Bot.py` file - a helper function `AlpacaSocket` was created to manage the API connection. 

```python 
class AlpacaSocket(REST): 
    def __init__(self): 
        super().__init__(
            key_id=KEY_ID,
            secret_key=SECRET_KEY,
            base_url=BASE_URL
        )
```

This is all we have for the brokerage connection and we can use an instance of the AlpacaSocket class as a reference to act on the API. We will be requesting stock data to feed into our AI data model. 


# Trading System Development 


