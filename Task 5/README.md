# Task 5 Writeup

## Task Description

The app uses a bespoke application of the OAUTH protocol to authorize and authenticate TerrorTime users to the chat service. Our intelligence indicates that individual terrorists are provided phones with TerrorTime installed and pre-registered to them. They simply need to enter their username and secret PIN to access the chat service, which uses OAUTH behind the scenes to generate a unique token that is used for authentication. This is a non-standard way of using the protocol, but they believe it to be superior to normal password-based authentication since a unique token is used per login vs. a static password. Whether that is indeed the case is up to you to analyze and assess for possible vulnerabilities. Our forensics team recovered a deleted file from the terrorist's hard drive that may aid in your analysis.

Through other intelligence means, we know that the arrested terrorist is a member of one of many cells in a larger organization. He has shown no signs of someone who is acting in a leadership role -- he simply carries out orders given to him from his cell leader, who is likely relaying information from the top-level organizational leader. To uncover information from the cell leader’s conversations, we need access to their account. The messages are end-to-end encrypted, so without the leader's private key we won't be able to decrypt his messages, but we may be able to learn more about the members of the cell and the organization's structure. Analyze the client and server-side components of the authentication process and find a way to masquerade as arbitrary users without knowing their credentials. Take advantage of this vulnerability and masquerade as the cell leader. Access and review the cell leader’s relevant information stored on the server. Use this information to identify and submit the top-level organizational leader’s username and go a step further and submit a copy of the last (still encrypted) message body from the organization leader’s chat history. It’s suggested to complete task 4 before attempting this task as task 4 aids in discovering the cell leader’s identity.

## Provided Files

* Authentication Program (auth_verify.pyc)

## Walkthrough

### Examining Provided File

For this task, we are given a python program which appears to be an internal component of the OAUTH server used by the app. It is a compiled python file, so if we use a decompiler we can see what it actually looks like. I used uncompyle which can be installed on a command line with:

* pip install uncompyle6

After installing it, you can decompile the program with a command:

* uncompyle6 auth_verify.pyc > auth_verify.py

This python file reveals some important details about the OAUTH protocol that is used by the app. Most notably, that the tokens that are submitted to the server are checked to verify that they are not expired, have the "chat" scope, and are of the type "access_token". However, they do not actually check to verify that the **user** of the token matches the user that we are trying to log in as. This means that once a token is generated, it can be used to log in to the XMPP server by **any** user for the next hour. These tokens can be obtained by:

* Logging into the app and checking LogCat in android studio, which shows the access token.
* Using token.py in this repo to simulate the app login and quickly generate new tokens.

Rather than deal with any kind of man-in-the-middle attacks, when interacting with the XMPP server for tasks 5 and 6, it is far easier to just use a standalone XMPP client. For this, I used Spark (https://www.igniterealtime.org/projects/spark/). Spark is especially useful because it allows a much higher level of configuration as well as a very powerful debugger and raw packet tool that can be used to craft our requests to the server.

### Spark Configuration

After downloading spark, you can configure it by doing the following:

* Click on Advanced button
* Set the host to chat.terrortime.app
* Set port to 443
* Check options for Accept All Certificates, Disable Certificate Hostname Verification, and Start Debugger on Startup
* On the login screen, enter the cell leader username from task 4 (without the domain)
* Enter the generate token for the password
* Enter terrortime.app as the domain
* Click Login button

### Identifying the leader

Once you are logged in, you'll may not see any contacts in the menu. You can go to Contacts -> Show Offline Users to show them. You'll see that there is a group called "management" that contains 3 people. One of these is the organization leader, while the other two are cell leaders. You'll also see a group called something like "cell-0". If you begin logging into the other management leaders then you'll find one of them only has a management group and no cell users. This is the user who is the top organization leader that you can submit for credit.

### Archive Retrieval

Once you get logged in as the top leader, you'll see that if you click on a user there are no messages showing. That is because the messages are actually archived on the server by the app and then retreieved when a user logs in. So they are not displayed in the normal message history. In order to retrieve these messages, you can send a custom packet under File -> Send Packet. The command that should be sent it:

    <iq type='get'>
    <query xmlns='urn:xmpp:mam:tmp' queryid='f27' />
    </iq>

Once you execute this command, you can click on the debugger window and you'll see a log of packets with the title "Message Received". If you look at the contents of those packets there is a body tag containing some json like this (truncated for readability):

`{"messageKey":{"cFcXLsCRzEZTivhekA7P8X1CXHd1H7P+KXR0bdZ5TMo=":"D+7qGQOEoZUbuHHg2XQ...","ubPtHT\/2pPy0mG8YS2I5QHiDhOQuHR+8X+yTLpasrHA=":"ALoRtoATD1AuTJPVOjlYdFM7u...","RhTKbmuEB\/FJQ5b3Ima91tNpyGIcszYUIx3i1YFhWyo=":"FUbja1I2LqjXwdS0r...","fWrGcOPzdcfTdTxPpEaD\/Fk7viuDhs6q2IELGYku5AU=":"AGQ76Jy7x9Uv5RsjJ7T..."},"message":{"iv":"W3qN6vu2YYoOClS3Lcrsiw==","msg":"VClP6RblpoUAQS8T..."},"messageSig":"T4GQaB2hECy54L7v2N5f0BHsozddGEnVk6w21JqvKzE="}`

If you select the very last message and copy the JSON from the message body, you can submit it for credit.

## Walkthrough Video
https://www.youtube.com/watch?v=BrsXWLYG1JE

[![NSA Codebreaker Challenge 2019 - Task 5 Solution](https://img.youtube.com/vi/BrsXWLYG1JE/0.jpg)](https://www.youtube.com/watch?v=BrsXWLYG1JE)

