# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['harambot', 'harambot.cogs', 'harambot.database', 'harambot.ui']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.2.0,<6.0.0',
 'discord>=2.1.0,<3.0.0',
 'dynaconf>=3.1.11,<4.0.0',
 'mysqlclient>=2.1.1,<3.0.0',
 'peewee>=3.15.4,<4.0.0',
 'psycopg2>=2.9.5,<3.0.0',
 'yahoo_fantasy_api==2.7.0']

entry_points = \
{'console_scripts': ['harambot = harambot.bot:run']}

setup_kwargs = {
    'name': 'harambot',
    'version': '0.3.0',
    'description': 'A Yahoo Fantasy Sports bot for Discord',
    'long_description': '# Harambot\n![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Build](https://img.shields.io/github/actions/workflow/status/DMcP89/harambot/pytest.yml?branch=main) ![Version](https://img.shields.io/badge/version-0.3.0--Beta-red)\n\n[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)\n\n\nA Yahoo Fantasy sports bot for Discord.\n\n## Commands\n    /ping                           - Gives the latency of harambot\n    /RIP                            - Pay respects\n    /standings                      - Returns the current standings of the current league\n    /roster "Team name"             - Returns the roster of the given team\n    /stats "Player Name"            - Returns the details of the given player\n    /trade                          - Create poll for latest trade for league approval\n    /matchups                       - Returns the current weeks matchups\n    /waiver                         - Returns the waiver wire tranasactions from the previous 24 hours\n    /configure                      - Configure the bot for your guild\n\n## Prerequisites\n\nIn order to properly configure your bot you will need the following:\n\n* Discord API Token\n* Yahoo API Client Id & Secret\n* Yahoo League ID\n\n### Discord API Token\n\n1. Navigate to https://discord.com/developers/applications and click the "New Application" button\n   ![discord-new-application](/assests/discord-new-application.png)\n2. Give your bot a name\n3. Navigate to the bot section of your application and click the "Add Bot" button\n   ![discord-add-bot](/assests/discord-add-bot.png)\n4. Click the "Copy" button under token to copy your bots API token to your clipboard\n   ![discord-copy-token](/assests/discord-copy-token.png)\n\n\n### Yahoo API Client ID & Secret\n\n1. Navigate to https://developer.yahoo.com/apps/ and click the "Create an App" button\n   ![yahoo-create-app](/assests/yahoo-create-app.png)\n2. Fill out the form as shown below, you can provide your own values for Application Name,  Description, and Homepage URL. Once complete click the "Create App" button\n   ![yahoo-app-details](/assests/yahoo-app-details.png)\n3. Copy the Client ID and Client Secret values\n   ![yahoo-app-secrets](/assests/yahoo-app-secrets.png)\n\n### Yahoo League ID\n\nYou can find your league\'s ID under the settings page of your league\n![yahoo-league-id](/assests/yahoo-league-id.png)\n\n## Deployment\n\n### Heroku\n\nHarambot now supports heroku deployments!\n\nClick the button at the top and fill out the form with your discord token and yahoo api client key and and secret.\n\n![heroku-deployment](/assests/heroku-deployment.png)\n\nOnce the deployment is complete enable the dyno\n\n![heroku-dyno](/assests/heroku-dyno.png)\n\n### Install package from PIP\n\n1. Install the harambot package using pip\n\n        pip install harambot\n\n2. Export the following environment variables\n\n   ```\n   export DISCORD_TOKEN=\'[YOUR DISCORD TOKEN]\'\n   export YAHOO_KEY=\'[YOUR YAHOO API CLIENT ID]\'\n   export YAHOO_SECRET=\'[YOUR YAHOO API CLIENT SECRET]\'\n   export DATABASE_URL=\'[YOUR DATABASE URL]\'\n   ```\n\n3. Run the bot\n\n        harambot\n\n### Run from source\n1. Clone this repository\n\n        git clone git@github.com:DMcP89/harambot.git\n        cd harambot\n\n2. Export the following environment variables\n\n   ```\n   export DISCORD_TOKEN=\'[YOUR DISCORD TOKEN]\'\n   export YAHOO_KEY=\'[YOUR YAHOO API CLIENT ID]\'\n   export YAHOO_SECRET=\'[YOUR YAHOO API CLIENT SECRET]\'\n   export DATABASE_URL=\'[YOUR DATABASE URL]\'\n   ```\n\n3. Run the bot.\n\n    ### On local machine\n        make run\n    ### With Docker\n        make build-image\n        make run-docker\n\n## Setup\n\n### Add the bot to your guild\n1. Generate a OAuth url from the discord developer portal using the bot scope and the following permissions:\n\n* Send Messages\n* Send Messages in Threads\n* Embed Links\n* Attach Files\n* Read Message History\n* Add Reactions\n* Use Slash Commands\n\nThe permission value should be 277025507392\n\n![discord-oauth](/assests/discord-oauth-generator.png)\n\n2. Set the gateway intents\n\nIn order for the bot to work properly it requires the following intents:\n\n* Sever Members Intent\n* Message Content Intent\n\n![discord-intents](/assests/discord-intents.png)\n\n3. Navigate to the generated url in a web browser and authorize the bot for your guild\n\n![discord-oauth-url-1](/assests/discord-oauth-url-authorize-1.png)\n![discord-oauth-url-2](/assests/discord-oauth-url-authorize-2.png)\n\n### Configure your guild\n\n* Once your bot is added to your guild you can configure it by sending a direct message to the bot with the following command:\n\n\n![discord-config-commnd](/assests/harambot_configure_1.png)\n\n* Use the Login with Yahoo button to authenticate with Yahoo and get your Yahoo token\n\n\n![discord-config-yahoo](/assests/harambot_configure_4.png)\n\n* Use the Configure Guild button to configure your guild for the bot\n\n\n![discord-config-guild](/assests/harambot_configure_2.png)\n\n\n* You can reconfigure your guild by running the configure command and clicking the Configure Guild button.\n\n\n![discord-config-guild](/assests/harambot_configure_3.png)\n\n\n## Command Examples\n\n### $stats Rashaad Penny\n\n![player-details](/assests/player_details.PNG)\n\n\n### $roster Lamb Chop\'s Play-Along\n\n![roster](/assests/roster.PNG)\n\n\n### $standings\n\n![standings](/assests/standings.PNG)\n\n\n### $matchups\n\n![matchups](/assests/matchups.PNG)\n\n\n### $trade\n\n![trade](/assests/trade.PNG)\n\n\n### $RIP "My Season"\n\n![rip](/assests/rip.PNG)\n',
    'author': 'DMcP89',
    'author_email': 'davemcpherson@wochstudios.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DMcP89/harambot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
