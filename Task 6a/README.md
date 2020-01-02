# Task 6a Writeup

## Task Description

The ability to masquerade as a TerrorTime user is helpful, even when we are not able to access the plaintext version of their messages. We want to be able to send "spoofed" messages (i.e., messages appearing to be from the user we are masquerading as) to other TerrorTime users as a way of disrupting their attack plans. Critically, any conversation we have as the masqueraded user should never be visible to that user the next time they access their account. But complicating matters is the fact that all messages sent and received through TerrorTime are archived on the chat server and downloaded each time a user logs in to their account. For this task, identify a vulnerabilty that will allow you to send/receive messages as a TerrorTime user without that user ever seeing those messages the next time they access their account. To prove your solution, submit the encrypted message body of a spoofed message that was sent from the organization leader to a cell leader. Submit the full client id of the cell leader you chose. Put the organization leader's account in a state such that replies to your spoofed message will never be seen by them, but still readable by you.

## Walkthrough

### V-Cards

For this task, we will be using Spark again. Please see the writeup for Task 5 for setup instructions.

If you recall the message JSON that you submitted for task 5, you'll notice that there are several "message keys" along with the actual message itself. That is because each message in this app is sent using key wrapping (https://en.wikipedia.org/wiki/Key_Wrap) so that each message is signed with the public keys of each of the participants in the conversation. This way, no matter which if them accesses the archive, they will always be able to decrypt the message using their on private key as long as they have one that matches a public key signature included in the message.

So the first thing we're going to need to know is how to get the public key for a user in the same way that the app does. For this, we can log in to Spark as the top leader and access their v-card with the following command in a raw packet:

`<iq id='v1' type='get'><vCard xmlns='vcard-temp'/></iq>`

If you look in the debugger window, you will see the response to your query which contains the v-card of the user and a DESC element that contains their public key. So what happens if we remove it?
  
## DANGER DANGER DANGER DANGER
## BACK UP THIS KEY BEFORE CONTINUING

If the public key is removed from the user's v-card, then a future message that you send will be readable by yourself and the cell leader but it **will not** be readable by the top leader, because it is not signed with their public key, as it is not on the server anymore.

This can be done by sending the following raw packet to the server:

`<iq id="v1" type="set">
  <vCard xmlns="vcard-temp">
    <DESC></DESC>
  </vCard>
</iq>`

As soon as they log back in, the top leader's app will add their public key back to the server and it will be like nothing happened. However, during this interim time, we can send spoofed messages that they will not be able to see. And responses from other users will not be viewable either because they will not be signed with their public key.

### Message Spoofing

The easiest way to send the spoofed message to the cell leader is to do it through the android app. Open the clientDB.db file in your SQLite browser and change the xname field to the top leader username. The way the app handles authentication makes this possible because the cid is sent for authentication and then the xname is sent to the chat server, so they can be different.

Next, use an online RSA generator (or one of your desktop if you want) to create a new 2048 RSA key pair. I used https://travistidwell.com/jsencrypt/demo/

Copy the public key you generated into the pubkey field in the database and make sure you put a line break after the final line before saving it. We don't need to worry about the private key because we don't care about decrypting this message for the task.

Upload the DB to your emulator and log in using the same credentials that you figured out in task 4. You'll notice that you are now logged in as the top leader, based on the contacts that you see. Click on the cell leader from Task 4 and send them any message that you like. What has happened in the background is that the public key you generated was added to the top leader's v-card when you logged in, and now the message that you sent it signed with your new key and the cell leader's key.

Now we just need to recover the JSON of the message in the same way as Task 5.

### Archive Retrieval

Once you get logged in as the top leader on Spark, you can send another archive request:

`<iq type='get'>
<query xmlns='urn:xmpp:mam:tmp' queryid='f27' />
</iq>`

Once you execute this command, you can click on the debugger window and you'll see a log of packets with the title "Message Received". If you look at the contents of those packets there is a body tag containing some json like this (truncated for readability):

`{"messageKey":{"cFcXLsCRzEZTivhekA7P8X1CXHd1H7P+KXR0bdZ5TMo=":"D+7qGQOEoZUbuHHg2XQ...","ubPtHT\/2pPy0mG8YS2I5QHiDhOQuHR+8X+yTLpasrHA=":"ALoRtoATD1AuTJPVOjlYdFM7u...","RhTKbmuEB\/FJQ5b3Ima91tNpyGIcszYUIx3i1YFhWyo=":"FUbja1I2LqjXwdS0r...","fWrGcOPzdcfTdTxPpEaD\/Fk7viuDhs6q2IELGYku5AU=":"AGQ76Jy7x9Uv5RsjJ7T..."},"message":{"iv":"W3qN6vu2YYoOClS3Lcrsiw==","msg":"VClP6RblpoUAQS8T..."},"messageSig":"T4GQaB2hECy54L7v2N5f0BHsozddGEnVk6w21JqvKzE="}`

If you select the very last message and copy the JSON from the message body, you can submit it for credit along with the username of the cell leader to which you sent the message.

## Walkthrough Video
https://www.youtube.com/watch?v=QiBxLU8mjn8

[![NSA Codebreaker Challenge 2019 - Task 6a Solution](https://img.youtube.com/vi/QiBxLU8mjn8/0.jpg)](https://www.youtube.com/watch?v=QiBxLU8mjn8)

