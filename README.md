# SparkGitHubBot

To help with the understanding of bots, we put together a walkthrough of a Github to Spark integration – official integrations with Github exist now, and will be expanded, so this is purely for demonstration purposes (but you can use the code now if you want an integration you can more directly control).

The bot listens for commits and comments on a particular repo, and then posts the details into a group or team room. The below parameters will be included in the message to a Spark room:

* Author Name
* Committer Name
* Pusher Name
* Commit id
* Commit time
* Repository
* Link to the Commit
* Comment
* Comment Link
* Comment User
* Repo
* Commit id

To build this bot, check this [step by step guide](https://developer.ciscospark.com/blog/blog-details-8228.html).


