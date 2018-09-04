# Kids' Activities
### A Website to Keep Track of Educational Events for Children

## Overview
This repository is meant to create and maintain a website that gathers information from various locations that regularly host events and gather their schedules into one place so that parents don't have to go searching around the internet to find events for their children. The idea is meant to be expandable to any number of cities, but for the moment, we only have events for Washington, DC.

In terms of the actual files in this repository, most of the heavy lifting is done by the Python scripts (and by [HTML5 UP](https://html5up.net) for creating the lovely template that we used to make this website). The Python scripts gather information about upcoming events from various institutions around Washington, DC and insert them into the HTML files for the website with the necessary formatting. This then creates an interactive map that displays where the events are with a marker with a radius proportional to the number of events at that location.

The website is updated automatically using the following bash script:
```bash
#!/bin/bash
cd ~/Kids-Activities
python3 collect-data.py
python3 make-table.py
git add map.html geojson.js
git commit -m "daily event update"
git push
```
This script, paired with the tool Cron, allows the website to update automatically every time the events change. (We still have to push manually, though.)

### Details
The Python files are written for Python 3.6. The file `collect-data.py` uses Python's `requests` library to pull the contents of the websites for each of several museums and cultural centers throughout the city. Then, the code looks for specific tags that each website uses to tag important details like the time and event information. From here, it formats these data into a CSV file for use by other programs, including only the events that are occurring within the next week.

The file `make-table.py` then formats the data from the CSV file into the appropriate JavaScript and HTML syntax and inserts them into the appropriate spots in the files for the website. These spots are marked with comment tags, e.g., `<!-- Tables Begin Here -->` so that the script can tell where to place the newly formatted data. The coordinates defining the shapes indicating the location and number of events are calculated here. Each shape is a 42-sided polygon, since the library that we use does not support circles.

In addition, the file `helpertools.py` contains helper functions useful to both `make-table.py` and `collect-data.py`. It was created mostly to avoid making either of those files too long, but there are some functions that are useful to multiple other files. Finally, the file `tagtest.py` was created as a simple test to determine whether each open tag in an HTML file has a corresponding closing tag. This was in response to a bug resulting from mismatched tags in the interest that it be prevented from happening again.

## In Progress
We are currently working on moving part of the project into PHP so that we can allow users to send information about events to the website. This may also allow us to update the webpage more easily by pulling from pages using PHP, which will run more automatically than a Python script. However, we have not made much progress in this area.

## Next Steps
At the moment, we load in all events from each location irrespective of their appropriateness for children. In time, we hope to be able not only to separate the children's events from the adults' events but also to separate the children's events by age range. In addition, we should at some point add the capability for users/parents to add in their own events and import them into our map.
