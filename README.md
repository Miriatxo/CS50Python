# DONOSTIA CITY CULTURAL EVENTS SEARCH ENGINE
#### Video Demo: https://youtu.be/KBGwUYs4kts
#### Description:

The present folder includes the following files: project.py contains the main program I implemented; requirements.txt lists all the pip-installable libraries the program requires; results.py contains API query results that I used to build the query function of project.py; and test_project.py contains tests for some of the functions in project.py that can be executed with Pytest.

This project allows the user to get real-time information on upcoming cultural events in the city of Donostia-San Sebastián, Spain. The project uses Python and queries the public API Open Data Euskadi, which provides access to data about cultural events in the Basque Country (the region of Spain where Donostia is located). The API responds with a JSON object containing (among other things) a list of dictionaries corresponding to the search results, which my program then cleans, filters, and translates into English before printing them on the terminal in an easy-to-read format. Alternatively, if no results are found that match the search criteria, the user is informed of this and the program ends.

The only required search criterion is the type or category of event. Additionally, the user can choose to specify the date, and a keyword. The type and date, if a date is provided, are used to query the API, while the keyword is used, if provided, to filter out results from the JSON response. This is dictated by the API.

To build my query function, I made a document for myself, results.py, where I recorded the API queries I made to see how the information in the API is structured (the event types there are, etc.). I copied and pasted in this document the results I got from each query, and used this information to build my query function. It turns out that the API expects one URL if the user enters only the type of event as a search criterion, and a differently structured URL if the user inputs the type and date of the event as search criteria. So my query function builds the URL it uses to query the API one way or another, depending on whether the user entered only the type, or both the type and the date of the event.

If the user selects only the type of cultural event they want to search for, they will get all upcoming events in that category. There are seven types of event:

1. Music
2. Art
3. Theater
4. Dance
5. Cinema
6. Children
7. Course

I used a regex and the re library to validate user input.

As to the search criterion of date, I used the dateutil library to validate user input. The URL provided by the API to search for events by type and date takes the parameters of day, month, and year (besides type). So, if the user enters a date in any reasonable format, the program converts it to a date in YYYY-MM-DD format, and then splits this date into three variables: year, month, and day, which it uses to build the URL.

This search structure of 7 types, a specific date, and a keyword does not utilize all of the contents and capabilities of the API, but I'm creating a tool aimed at city visitors rather than locals, so I chose to filter and order the information this way. I think my structure is more simple and user-friendly for a visitor than the complex structure of Kulturklik (kulturklik.euskadi.eus), the official cultural information dissemination website of the Basque Government, which is aimed at locals who already know the municipalities and institutions and thus benefit from a more fine-grained range of search options.

Even though this search engine is aimed at short-term visitors, I included courses as well. The average visitor is a tourist who stays less than a week, but there is a growing number of visitors who choose to rent a property for a short period to explore the city while they work remotely, and some of these visitors will be interested in short cooking courses, surf courses, and the like.

However, I filtered out events in the JSON object that take longer than three months, such as longer courses. Visitors who stay longer are not my target users, since I take it they would prefer to use a fuller cultural acitivities website aimed at locals, such as Kulturklik for the whole region or Donostia Kultura (donostiakultura.eus) for Donostia.

I also filtered out activities that are in Basque, assuming visitors don't speak Basque. And, since the API covers the whole region but my program only provides information on Donostia, I filtered out events outside of Donostia. Language is not a search parameter supported by the API; and if municipality is passed in as a search parameter, date must be passed in too, but I wanted the date to be optional because visitors are often flexible with dates. So I was forced to query the API for results outside of Donostia and in Basque as well, and filter these results out from the JSON response afterwards.

Finally, if the user enters a keyword when prompted, the program implements this keyword as an additional filter, when selecting which events in the JSON object to output as search results. This is because there is no keyword parameter in any of the URLs offered by the API, so the keyword is used to process API query results rather than form API queries, just like with language and municipality.

I used the duck and ChatGPT for asking all kinds of conceptual and technical questions in the process of learning what I needed to learn to complete this project. I discovered that these tools are still in a stage where they make all sorts of mistakes all the time, and even repeat mistakes shortly after accepting them as mistakes. So I always took their answers with a grain of salt; but they have been of great help throughout. For instance, I couldn't present query results in the form of tables because an event's description is often several paragraphs long and doesn't fit into a table cell. I was about to take much longer to complete this project than I had anticipated in order to build a Flask application to present query results, but I avoided doing this thanks to ChatGPT's suggestion of presenting query results on the terminal in the form or "cards" rather than tables, which also make it visually clear where an event ends and another begins.

