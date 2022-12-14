# GROUP 4 - TEXTUAL BASELINE ANALYSIS 

    Course: COSC425/426
    Client: Dr. Randall Cone
    Group Members: Caroline Smith, Ikomi Moki, Joseph Fernandez, Joshua Comfort, William Townsend

## Project Purpose 

    This project seeks to create a database for textual analysis of the English Language through the scraping of a large amount of public domain data. 

    This project is broken up into three phrases.

## Current Status 

### **COSC425 Final Presentation/Post Sprint Three**

    We were sucessful in completing our third sprint goals. We have a working website which 
    contains information pertaining to the data that is present in the database. We have 
    over 16 million data samples present in our database at this time, which is a huge
    achievement. 
    
    As we move into te future, we will be working on making our website more responsive. We 
    want to add visualizations, which will be a large part of phase three. We additionally 
    want to be able to have the website hosted non-locally. Hopefully this will occur over
    winter break.
    
    The tools we are continuing to use are the same, with bootstrap, JavaScript, and Python.

### **Sprint Three**: 7 November 2022 - 5 December 2022

    We were successful in our second sprint goals. We continued to build our 
    scrapers and refine our analysis scripts. We also got the preliminary database set up
    (thanks to Chris!) and are beginning to push data to the database. 
    
    The third sprint will be focused on finishing up our remaining scrapers (for Amazon
    and Yelp), building the database, and building a preliminary website. We need to figure
    out how we are going to host our website, but for the time being it will be hosted locally.
    
    The tools that we will primarily be using are bootstrap (HTML/CSS), JavaScript, and Python. 

### **Sprint Two**: 17 October 2022 - 7 November 2022
    
    We were successful in our first sprint goals. We researched, built scrapers, and
    prototyped and built scripts (including neural networks) to analyze and create
    necessary metadata. We additionally reviewed fundamental ideas in Python.
    
    This next sprint will be focused on refining what we created in the first sprint.
    We will also begin to look towards the future in phase 2; we will begin to scope
    out ideas for our database design and implementation. We also need to speed up (or
    implement) parallelization in some areas. 
    
    We hope to, by the end of this spint, have a prototype database and potentially
    prototype interface with said database. 

### **Sprint One**: 19 September 2022 - 17 October 2022

    In the first sprint we will primarily focus on research, which includes
    looking into more sources to scrape, reviewing Python, learning functional
    programming, and working to understand the scope of our project. 

    We will also begin to develop a preliminary webscraper so we can get a feel
    for the different portions of the website we will need to analyze. It will
    also give us a first crack at parallelizing a program of this scale for the
    fastest scraping. 

## Repository Structure 

    (This may not be how it appears currently.)

    /src/ -> stores all of our source files 
    /src/webscraping -> maintains all of our webscraping files 
    /src/backend -> maintains the backend files
    /src/frontend -> maintains the front end files

## The Project Breakdown 

### **Phase One:** Information Acquisition

    We will be gathering a large number of public domain sources for scraping.
    Think of websites like Wikipedia, Project Gutenberg, or the Internet Archive;
    all of these sources will be instrumental in creating our repository of
    information.

    The difficulty comes in identifying whether the sources are technically in
    the public domain, since a lot of the Internet, although freely available, is
    under some sort of copywriting protection. 

    The other part of this phase will be creating a parallelized Python webscraper
    that will read the webpage. The information we are currently looking at is the
    texts of various webpages, but also metadata such as the data, time, original
    source, location, and tags, which are less rigidly defined in our current
    state.

    Using these, we can classify documents to make their storage in our database a
    simpler endeavor. 

### **Phase Two:** How to Store and Provide Information

    Gathering the data is half of the battle. This phase is focused on finding a
    good way to store and present the information. In order for easy functionality 
    with Python, we will most likely use a NoSQL database like MongoDB for fast
    access. We will additionally create a website to act as the front-end of our
    project. The tools that we will use for the website are undecided currently,
    but most likely will include Bootstrap for the front-end design. 

    We will begin this phase after we are happy with our webscraping efforts from
    phase one. This will most likely be the most tedious portion of the project
    since we want the user experience to be quick and efficient, especially
    accessing the database. 

### **Phase Three:** The Future

    The primary purpose of this project is to study the way that language changes
    over time. Using the baseline that we create, we want to be able to analyze
    ???signals??? that deviate from our established information, which allows us to
    see trends in how people are talking. Ultimately we should be able to ask
    ourselves what questions we would like to see answered based on this data. 

    Being able to ask important questions about the way that our language changes
    is crucial for greater human development. Language is a critical portion of
    how every field changes throughout time, from how we write books to how we
    analyze the human body to how we write code. 

    Eventually, this project will encompass more languages than just English, but
    for the time being, we will focus on English. The sheer number of resources
    available to us in English is irreplaceable. 
