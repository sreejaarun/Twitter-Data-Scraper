Twitter Data Scraper
Overview
This is a Python-based Twitter data scraper that allows you to extract tweets and user information based on keywords, hashtags, or usernames. The scraped data is stored in a MongoDB database and saved in a CSV file.

Installation
To install the required packages, run:
pip install -r requirements.txt

Usage
Before running the script, you need to fill in your Twitter API credentials in the twitter.py file.
To run the script, use the following command:
streamlit run twitter.py

You will be prompted to enter the keywords, hashtags, or usernames you want to scrape. Once you enter them, the script will start scraping the data.
The scraped data will be saved in a MongoDB database named twitter_data and in a CSV file in the data folder.

Credits
This project was created by Sreeja and is licensed under the MIT License.

Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request.
