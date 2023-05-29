
# Telegram to Discord Message Bot — Forward Telegram Messages to Discord 

## Description
Forwardgram is a free and open source, telegram to discord message bot. It enables one to forward messages from Multiple Telegram channels to one (or more) Telegram/Discord channels of your own. This python bot monitors multiple telegram channels. When a new message/entity is sent, it will parse the response and forward it to a discord channel using your own personalized bot. It will also forward the same message to your own Telegram channel.

### Dependencies

1. Python 3.6+ 
2. [Anaconda Python Console](https://www.anaconda.com/products/individual) (Optional, makes pip install debugging go away)
3. Create your own discord bot, add it to your server and retrive token. Follow Steps [here](https://www.writebots.com/discord-bot-token/).
4. Have a Telegram account with valid phone number


### Installing and Setup
1. Clone this repository
2. Open your choice of console (or Anaconda console) and navigate to cloned folder 
3. Run Command: `python3 -m pip install -r requirements.txt`.
4. Fill out a configuration file. An exmaple file can be found at `config.yml-sample`. 


### First Run and Usage

1. Change the name of `config.yml-sample` to `config.yml`

#### Filling `config.yml` file

* Create a two channels on Telegram as `channel_send` and `channel_recieve` and fill in their channel ids in config.yml
* Add your Telegram `api_id` and `api_hash` to config.yml | Read more [here](https://core.telegram.org/api/obtaining_api_id)
* Add your `discord_bot_token` to config.yml | Read more [here](https://www.writebots.com/discord-bot-token/)
* Add your `discord_1_channel` channel id. Remember when you remove extra discord channels you have to update code in `discord_messager.py` under comment `DISCORD SERVER START EVENT` and `MESSAGE SCREENER`

#### Editing `discord_messager.py`

* Whenever you add and delete discord channels in `config.yml`; `discord_messager.py` will have to be updated. If you know basic python you will understand the code.
* Multiple send/recieve telegram channels in `config.yml` can added without any code change.

2. Read the Version History and Changelog and below before running the script.

3. Run the command `python3 forwardgram.py config.yaml`

```
***PLEASE NOTE:  In the first time initializing the script, you will be requried to validate your phone number using telegram API. This happens only at the first time (per session name).
```

## Authors

* Karan Kapuria
* voidbar
* Sqble

<a href="https://www.buymeacoffee.com/kapuriakaran" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Version History and Changelog

* 1.0 Initial Release 
	* Shows `SystemExit: None` when discord messages are sent successfully. This is because we trigger `discord_messager.py` as subprocess when a new telegram message is sent in `channel_send` 


## License

This project is licensed under the MIT License - see the LICENSE.md file for details
