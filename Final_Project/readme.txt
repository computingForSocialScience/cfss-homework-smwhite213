
NOTES ON RUNNING SCRIPTS

My final project can be viewed by running the following:
1) sentimentscrape_final.py
2) analyze.py

Please be mindful of the notes in sentimentscrape_final.py. Running the full script takes approximately 30 minutes. (Of the 539 congresspeople in the 114th Congress, a little more
than 500 had active twitter accounts with at least one tweet. The "full script" scrapes
Twitter for several tweets from each congressperson. The "test version" only scrapes
Twitter for 10 tweets from about 27 congresspeople.)

Currently, the code for the full program is commented out and replaced with 
code that should take about 30 seconds to run. Note that this code will write to 
sentiments_testruns.csv, and not to sentiments.csv.

Currently, analyze.py reads from sentiments.csv, but you can change which code is commented
out in order to pull from sentiments_testruns.csv if you prefer.

All csv files and boxplots currently saved in github are for the full data set (not test runs).

Please let me know if you have any questions!

-Shannon
smwhite213@uchicago.edu