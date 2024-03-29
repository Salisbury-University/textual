# GROUP 4 - TEXTUAL BASELINE ANALYSIS 

    Course: COSC425/426
    Client: Dr. Randall Cone
    Group Members: Caroline Smith, Ikomi Moki, Joseph Fernandez, Joshua Comfort, William Townsend

## Project Purpose 

    This project seeks to create a database for textual analysis of the English Language through the 
    scraping of a large amount of public domain data. 

    This project is broken up into three phrases.

## Current Status 

### **End of the Semester** 

    As we approach the end of the fourth sprint, it's important to reflect on the progress we've made so 
    far and prepare for the final stage of the project. Over the past few weeks, we've been working hard 
    on developing new features, fixing bugs, and improving the overall functionality of the project.
    
    As we move towards the end of the development cycle, it's important to remember that we have a finite 
    amount of time to work on the project. With the end of the sprint approaching, it's time to shift our 
    focus towards merging all the branches into a fully finished, working product. This process will 
    involve consolidating all the code and ensuring that all the features are fully functional and working 
    as intended.

    It's important to note that during this phase, we will not be adding any new features to the project. 
    Instead, our focus will be on perfecting the existing features and ensuring that the final product 
    meets all the requirements laid out in the project specification. This will require a high level 
    of collaboration and attention to detail from all team members.

    As we approach the end of this project, it's important to take pride in the work we've accomplished so far. 
    We've overcome numerous challenges and have made significant progress towards our end goal. With just a 
    little more effort, we can deliver a final product that meets or even exceeds our initial expectations. 
    Let's stay focused, work collaboratively, and finish this project with the highest level of quality possible.

### **Sprint Four**: 10 April 2023 - 30 April 2023

    This sprint will be primarily focused on wrapping up any loose ends for the current state of the project.
    We will contnue to add more data to the database all of the way to the end of the semester, work on 
    visualizations for the data, and work on the user interface for the website. It is important to tie 
    up the loose ends in order to have a finished project that our client is happy with.
       
    We will also strive to update the database with clear documentation on the chance that the project gets passed
    down to another COSC425 group in the future. 

### **Sprint Three**: 13 March 2023 - 09 April 2023

    As we move into the final two sprints of the semester, we are going to be focusing on data collection 
    in order to beef up the amount of data in the database, finalize tutorials present on the website
    for anyone who wishes to understand the different vectors of analysis, and begin looking into ways
    to visual the data based off of the analysis that has been done. 
    
    These are all important tasks as they seek to reach the end goal set out at the beginning of the project: 
    create a collection of English textual data that can be used by the public for analysis and various other
    activities. 

### **Sprint Two**: 20 February 2023 - 12 March 2023

    This sprint is continuing the work we began in the last sprint with touching up on parts of the project
    that we looked at last sprint. This includes a focus on demos for the website, restructuring scrapers
    and polishing up analyzers. It is planned for the search page to be finished during this sprint as well,
    which seeks to solve the usability issue for those not directly familiar with the project.
        
    We will also look to create more fleshed out documentation for use by others. This is accomplished
    primarily by the tutorials page on the website, but also by written documentation that will go
    on the repository and potentially on the site itself. Each of the tools should be fully documented.
    Code itself should be as well for the chance that only group picks up the project once the current
    team graduates in the coming spring. 

### **Sprint One**: 30 January 2023 - 19 February 2023

    As we move into COSC426, we are looking more at polishing the code written and parts of the
    project that we worked on last semester. We will also be using GitHub more effectively
    to track our progress on the projects tab and issues. To see the status of any portion of the
    project, view the project board. 
    
    This sprint in particular we will be focused on cleaning up and getting refamiliarized with the 
    code base, since it has been several weeks since we have worked on the project. Members of the
    team will continue where they left off in December in order to polish the website - specifically
    the backend - for a more streamlined experience for the user. This includes a fleshed out search page 
    in addition to more tutorials. There will be additional work on the various analysis tools. 

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
    /src/website -> maintains the website files
    /src/analysis -> maintains the analysis script files

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
    “signals” that deviate from our established information, which allows us to
    see trends in how people are talking. Ultimately we should be able to ask
    ourselves what questions we would like to see answered based on this data. 

    Being able to ask important questions about the way that our language changes
    is crucial for greater human development. Language is a critical portion of
    how every field changes throughout time, from how we write books to how we
    analyze the human body to how we write code. 

    Eventually, this project will encompass more languages than just English, but
    for the time being, we will focus on English. The sheer number of resources
    available to us in English is irreplaceable. 
