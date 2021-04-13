#### Dylan Evans - ePortfolio 

## Professional Assessment

## Code Review

[![](http://img.youtube.com/vi/lm5LciJP5fw/0.jpg)](http://www.youtube.com/watch?v=lm5LciJP5fw "Code Review Example Video")

## First Enhancement and Narrative

[First Enhancement Files](https://github.com/DylanEvans-dba/DylanEvans-dba.github.io/tree/main/Milestone%202%20Artifacts)
   
The first artifact that I have decided to examine is a restfull API written in  
Python that I developed for a stock ticker application that I was assigned to  
produce for CS-340 a few terms back, so late 2020. It functioned as an intermediary  
between the front-end stock ticker application and the back-end MongoDB database that  
stored the stock information as JSON data.  

I chose this artifact because it encompasses several facets of software design in  
my mind. It is a Python-based API that was written for a web-based application with a   
MongoDB database on the backend that stores data in JSON format and whose native query   
language was JavaScript. This API effectively represents the centerpiece of a collection   
of other files, functions, applications, and more that served as the various, unrelated   
portions of this stock ticker app. All held together solely by the glue of the API that 
connected them. 

Moving on from poetic waxing, a lot of testing went into the design of this API 
at the time that I was designing the project, but in all honesty so much time has passed 
that I’m afraid any serious “enhancements” I would make to the code would only result in 
less-than-desirable outcomes. As such, I have opted to improve the artifact by improving 
readability. While the code is (debatably) about as cleanly formatted and readable as it  
could be, I felt the comments could use some cleaning up and clarifying. I have unified the   
formatting of existing comments by enforcing grammatical standards throughout. I have also   
clarified the language of existing comments as well as added new comments to hopefully help   
fill in some potential lapses in clarity in the code that was not already explained by other  
comments.   

I feel that I have sufficiently met the course requirements with this enhancement.   
Yes, there is the strong potential that I could have made a more impactful enhancement to   
the artifact. Perhaps improved its efficiency or further modularized the code. However, I   
again felt that it was in the best interest of the code as a cohesive, and functional, artifact   
that I limited my rusted expertise to more minor improvements. With all of that said, I do feel   
that readability is extremely important in software design in every instance except job security   
when you are the one person that currently has the job. Even in that instance, future you will  
be thankful for the time taken to make their life easier.  

While enhancing this artifact have less learned than reinforced my stance on readability   
of code. Looking over my comments from the pre-enhanced artifact where its mix of punctuation   
standards as well as grammatical spacing and capitalization made it difficult to differentiate   
code from comment in some instances. I hope that my added enhancements has remedied this issue 
and made future me, as well as anyone else reading this code, a bit more at ease.   

## Second Enhancement and Narrative

[Second Enhancement Files](https://github.com/DylanEvans-dba/DylanEvans-dba.github.io/tree/main/Milestone%203)

The second artifact that I selected is a Java application that I wrote for CS-320 that functioned 
as an interface and data storage solution for a medical practice. It features user login logic, 
menu options, and tons of underlying functionality associated with those options that it calls 
from other files. 

I chose this artifact as my example for algorithms and data structures because it features several 
algorithms as part of its functional logic including while loops, if loops, and switch cases. It 
also stores menu items as a list and calls that list to populate the menu. I have decided to improve 
the comments of this artifact to help clarify exactly what each part of the artifact does. After 
cleaning up the existing comments, improving readability and adding more detail, I have also added 
several more comments to each section of the code. 

## Third Enhancement and Narrative

[Third Enhancement Files](https://github.com/DylanEvans-dba/DylanEvans-dba.github.io/tree/main/Milestone%204)

For my final artifact which represents my experience with Databases, I decided to chose a query that I recently optimized at work. This query served as the language behind a pre-built search that our users could run in our CRM known as a “Smartfolder”. These smarfolders query the SQL database to pull rows of data from client files. This allows our users to easily find files that meet pre-determined criteria so they can more easily perform their jobs. A few users in our company apart from myself can write SQL queries so they are able to add or edit smartfolders as needed. This query was originally written by one such user. 

The query was brought to my attention when I received a ticket that complained of slowness in our CRM. After investigating I determined that the issue lied with the smartfolder that uses this query. While the query was fairly straightforward by our usual standards, it was taking over 30 seconds to execute in the database and the execution plan showed that every single row in multiple tables was being read multiple times.

My first step in troubleshooting was to clean up the formatting to improve readability. The query was originally a jumble of code with no indentation or proper spacing and it didn’t follow SQL formatting standards. With everything cleaned up, I noticed that there was an OR operator at the bottom of the WHERE clause that had been left out of a parenthetical in the previous line. I moved the close parenthesis down to its correct position and the query executed in less than a second. This again has solidified my belief in the importance of readability and proper formatting. 
