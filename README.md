# Data Mining Project - Good Old Games
Data mining project - Roy and Magen

## Description
In this project so far, we chose to scrape the website GOG.com (https://www.gog.com/).
GOG.com is a digital distribution platform – an Online store with a curated selection of games,
an optional gaming client giving you freedom of choice, 
and a vivid community of gamers.

GOG scrapping for the given data:

- game_title - The game title.
- game_sku - The game stock keeping unit.
- game_score - The score of the game, given by the gamers.
- game_price_base - The base price in (USD).
- game_price_final - The final price after discount (USD).
- game_price_discount - The percentage of discount.
- game_url - The URL of the specific game.
- genre - List of game's genre.
- works_on (supported operating systems) - i.e. macOS/Windows/Linux etc...
- release_date - The game release data.
- company - List of development & publishers of the game.



**for common knowledge:**

occasionally the scraper is getting blocked by the website, detecting that a machine is connecting to it, in this case a stale element reference is raised and will be printed to the screen, the scraper will reattempt and either it will skip the page indicating it's index number or it will cease to scrape and use the data that was scraped to this point. in any case it's not causing the program to crash.


### **CLI**
**arguments**: -m, -p, -c, -d

**-m**: selects whether to scrape through: 

----------**'everything'** - every game for sale in the website (default)	

----------**'on_sale'** - games that are on a temporary discount

----------**'new'** - games that were recently released

**-p**: price filter: 

-----------**'u5**',**'u10',** **'u15'** :  corresponds to games sold with prices under 5,10,15 usd

-----------**'a25'** - games sold with price above 25 usd

-----------**'free'** - games that are free to download

-----------**default** - no price filter

**-c**: users choice:

-----------**'screen'** - print the results to the screen (default)

-----------**'db'** - write the results to the Data-Base

-----------**'both'** - print the results to the screen and write them to the Data-Base

**-d**: create database:

---------**'yes'** - create the database

---------**'no'** - do not create the database (default)



### **CLI examples:**

<python3 main.py -m new -p u10 -c both> -> new games under 10 usd, prints both to screen and writes to the Data-Base

<python3 main.py -c both >  -> scrapes through all games with no price filter, prints results to the screen and writes to db

<python3 main.py -p free> -> scrapes through all the free games and writes them to the screen

<python3 main.py -p free -d yes> -> scrapes through all the free games and writes them to the screen, create the database schema regardless

## Repository Prerequisites

### **Python Libraries**
To Scrap the site, we had to use several external libraries, such as bs4 and Selenium. 
You can find all the required libraries in the added requirements.txt file.
To run the script on your local machine, please install those libraries.



### **Troubleshooting Selenium Webdriver**
After installing those libraries, we suggest focusing on "selenium webdriver". 

Selenium can work with different browsers. 																											We decided to go on with the most popular today, Google Chrome. 
Therefore:

1. Please verify that Google chrome is installed on your local machine.

2. On Google chrome itself: 

    click the 3 dots on the URL bar -> Help -> About Google chrome -> Copy your google chrome version
    (for example: Version 88.0.4324.190 (Official Build) (64-bit)).

3. Enter the following link: https://sites.google.com/a/chromium.org/chromedriver/downloads

4. Find your chrome version from step 2, choose your current operating system (macOS, Linux, etc...)
    and download the zip file to your local machine.

5. The zip file contains a file called chromedriver.
    (!) which needs to be added to the folder of the main script.

     **chromedriver** - responsible for the automation and communication between the python script and the browser itself. 

    **Attention:** In some cases, it requires downloading few versions until you find the correct one. 
    By default, we left chromedriver.exe, which compatible with Win 64 & Chrome 88.0.4324.190. Make sure you replace it with your chromedriver.



### **Troubleshooting MySQL DB**
In order to save the results into MySQL DB, please verify that your local machine runs proper instance of
the MySQL DB. We recommend to work with MySQL version 8.0 due to Syntax, Stability and Security reasons.

Please verify that you have proper user with writing privileges, and you remember the user name and the password of that account (we will use it in the Instructions part).

#### Database ERD Diagram: GOG_SCRAPPER_DB

​	![alt text](https://i.ibb.co/8jVCm5J/ERD-Diagram.png)

​	The DB includes 4 different tables:

1. game_titles - The main table. Each row includes unique about each game.

2. game_prices - Each row contains the quote of the game price for the Python running date.
3. game_genres - Each game can contain up to 3 rows of genres.
4. game_scores - Each row contains th quote of the game score for the Python running date.

#### Why we use "quote" in the Prices & Scores tables?

​	In order to Analyze the prices and popularity overtime, we would like to save script's previous results.

#### Creating the Scrapper DB

​	Our scrapper can print into screen, write into DB or both (for further info please read the Cli help).
​	In order to establish the writing into DB it's mandatory to **create the DB**. 

​	In order to load empty DB into your local machine, you have to run the SQL script "create_db_GOG.sql".
​	The file is located with MySQL folder within the repository. You can use either **MySQL Shell** or MySQL     	Workbench to run the script.

​	After running the script, you can use the query "use databases;" to verify that the DB successfully loaded.

#### Configure your MySQL credentials into the Script

​	Only on the first time, you must configure some variables in order to establish protected connection 
​	between Python and MySQL:

​			1. Open the config.py file.

​			2. Change "mysql_user" value into your MySQL user-name.

​			3. Change "mysql_password" value into your MySQL password.

​	<u>Install MySQL - Python connector</u>

​	Please install the Python connector:  https://dev.mysql.com/downloads/connector/python/

#### Known issue with MySQL connector 

​	If after the first run the of the Python Script you get the following error: 

​	mysql.connector.errors.NotSupportedError: Authentication plugin 'caching_sha2_password' is not 
​	supported

​	Please change the variable "mysql_native_authentication" into True (config.py file).

​	

## Running the Python Script

In order to start the scrapping work, please run the main.py file using Python(please see CLI commands section). The chrome browser will pop out until
all the pages will be collected. Please don't touch the computer at that time, since it can hurt the process
of Selenium. There are over 98 pages in GOG. Therefore it can take some time.
So you're asking why it's taking so long?
Basically, on each page, we collect all the game URL. 
Usually, the chrome opens over the script, so you can't see what is printed (And please don't try, 
it can hurt Selenium).
From time to time, we print which pages aren't scrapped.

After we finished collecting all games' URL, you'll start to see how the script is printing to
 stdout each game's detail in a row. 

## PROJECT FILES MODULES & CLASSES
**main.py** - calls the import URL module, gets all the game URL, and uses grequest to get the responses concurrently in batches. Each response is sent to game_page_scrapper.py, which prints the game data into stdout. 

**import_urls.py** - goes through the website pages and parses all game URL, returns a list of all games URL.

**game_scrapper.py -** Returns ALL the available data from the game's page URL. 

**import_game_details.py -** Contains all the functions that scrape the data, uses bs4.

**import_game_data.py -** Merging general data with game details

**mysql_writer** - Contains WebsiteDB class. This class is responsible for writing the scrapper into DB.

**config.py** - contains constants, key strings, and URL.

**arguments_parser.py** - parser arguments fro CLI to filter and direct the program.

**api_twitch.py** - Downloads the top 1000 games from Twitch API.

**db_creator** - creates the database schema and tables if the user pleases .

## API

We tested a Query between the game_titles and our new api source: twitch rankings. We found great matching after cleaning the title name (as the key).
Our future plan for this source is to enrich our knowledge about the games.

Some background:
Twitch is the world's leading live-streaming platform for gamers and the things we love. Watch and chat now with millions of other fans from around the world. (Twitch's website).

Why we need Twitch:Goog old games (i.e. GOG), is part of the gaming store industry (opponents: Epic Games (Fortnite) and Steam).
We had a lack of knowledge about the popularity of those  titles. Therefore, we brought with the API connection new data about the popularity of 1,000 titles.

It's important to understand, GOG is officially selling very old games. On the other side, we tested simple join between the two tables and we found great matching.

**The logic of the API:**
1. Importing new Token.
2. By using that client id, secret code and Token, we connect to the developer area API.
3. We decided to bring currently only the "top games" option. In the future we may consider to add more tables.
4. Each record includes title id, name, clean name (for joining) and art work (of the box).
5. The first record is 1st place, the 2nd place and so on... until 1000 samples.
6. We will use it in our future Dashboards on AWS using some SQL magic to generate some cool insights.

Good to know: Our script has the ability to re-try up to 3 times failures with the API on each loop (due to pagination).
After the 3rd failure, our script will raise an Error about the error code. (2** - Success, all the rest is failure).

## GIT HUB REPOSITORY
https://github.com/MagenLahat/Data-mining.git


