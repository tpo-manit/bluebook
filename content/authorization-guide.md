---
title: "Auto Authorization Guide"
url: "/authorization-guide"
summary: "Authorization Guide for colleges that don't use google workspace"
---

Please note that this is only intended for people that have an Academic Email but can't use it because their university doesn't use Google Workspace.

To get your email auto authorized please send your non academic email (that you want to use) in body of the email using your academic email to [bluebook.auth@gmail.com](mailto:bluebook.auth@gmail.com).
      
Please note that only one proxy email (non academic email) is allowed per academic email.


### How it works
- We use an AppScript to check for new emails from (*.ac.in) domain emails.
- Whenever there is a new email we parse out the proxy email from body using regex.
- We check if there is already a proxy email registered for this academic email, if yes we send back an email telling this to the requesting user.
- Otherwise we add the proxy email to our DB and allow the Google Form to Validate your proxy email by updating the regex through GForm API.


Please comment below if you require any clarifications or have any doubts.