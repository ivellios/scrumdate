# scrumdate

In some situations you may need to create daily update of the stuff you were working on
based on the pivotal stories of your project.
You could simply share your work progress via its dashboard. But let's assume this is not possible at a time.

So every day you create an update note. Step by step adding new stories and links, while working on the stuff.
But it takes time!

**Why should you waste your time, while you can generate this status automatically? Over just a few years you
can save that way even one month of your working time.**

This tool can help you to automate the process, so you can really focus on your work.

It connects with your pivotal via official API, pulls information for search `mywork:"INITALS"`, where initals
are provided by you. It then creates a simple report of your daily actions adding classic teamwork and code reviews.

You should always review the result! But still, it will be much faster, than manually copying story names and their URLs.

This tool is just an example. You know better how your updates should be formatted, so feel free to create a fork
and adjust whatever you need.

## Use cases

You can use this code with some FaaS (e.g. AWS Lambda) and connect it to your communication app.
Discord or slack let you create your own bots or define own slash commands, so you can quickly retrieve the daily note
and adjust it before sending forward.

## Known issues

 - [ ] Check for deployments tag checks its creation daste which is not the same as the date of adding the tag to the story
 - [ ] This tools should use events API for checking on the stories recent changes and if they were done today, then properly map to status
