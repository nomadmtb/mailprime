![](https://raw.github.com/nomadmtb/mailprime/master/README_FILES/icon.png)

MailPri.me
==========

What is MailPri.me?
-------------------
> MailPrime is a web-based email campaign tracking service written with Django.

What does it do?
----------------
> MailPrime allows users with an account to create N email campaigns. With each
> campaign, users are able to add recipients to each campaign. Campaigns also
> consist of N messages. These messages will get sent to the recipients of a
> campaign.

What do I still need to do?
---------------------------
* Create more templates.
* Create api/action for sample campaign-invitation.
* Add counter to Message obj to keep total recipients consistent after people unsubscribe.
	* Or, just keep a count of people who unsubscribed and display it in the message stats.
* HTML escape message-body when creating a new message.
* Add Edit-Message page.
* Redesign the structure of the pages, make it look better.
* Build cronjob scheduler to deploy messages.
* Build overall-campaign stats page.
