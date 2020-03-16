# Bachelor

File "minimum" contains your minimum code from "https://github.com/otree-tools/jbef-channels". I added a money IntegerField (initial=1000) in the Player class. For testing purposes I extended your code, so every time an answer is submitted, 100 is subtracted from that value. Until here everything worked fine. 

Before adding more test features to the code (for learning by doing), I decided to make a copy of that project, so I would not "destroy" it. You find it in file "min". In the code I renamed every "minimum" to "min". Anyway it doesn´t work like the original code. The "subtracting 100 from the money" feature still works. The problem is that the following strange thing occurs: After submitting the first answer, the "Tasks attempted so far" counter jumps to a random number X and the "Tasks correct so far" counter jumps to X-2.
I really don´t get why this is happening, because the code is just a copy of a working code. I hope by understanding why this is happening, I will understand Django a bit more and can apply this knowlege for writing my crowdfunding project. Is there anything else I have to change, except renaming all the "minimum" to "min"?

File "bach_test" contains a prototype of my crowdfunding project without the use of Django. Everything works so far. But you will see that it´s a pretty unsatisfying experience without real-time interactions.

I will upload a file with a simplified version of my crowdfunding project using Django tomorrow. Today I had a job interview, so I couldn´t have a look into it. The last days I was busy trying to understand the bug in the "min" file.

I think the main problem is, that I don´t really understand how to code the url-pattern (f.e. url_pattern = (r'^/tasktracker/(?P<player_id>[0-9]+)$')) in consumers.py and the routing. Which sources did you use to teach yourself how to do it? The Django-docs didn´t really help me, because I don´t know how to do the transition to oTree.
