# Task 6b Writeup

## Task Description

Though we might be unable to decrypt messages sent and received in the past without a user's private key, it may still be possible to view future messages in the clear. For this task generate a new public/private key pair and make whatever changes are necessary such that all future messages sent/received within TerrorTime may be decrypted with this private key. Critically, you can not disrupt future legitimate conversations between users.

## Walkthrough

This is actually probably one of the easiest tasks in the entire challenge but it is just a little tedious to pull off. If you recall from task 6a, we were manipulating the v-card of the top leader to remove their public key and replace it with your own so that you could spoof messages that they would not be able to see later. So what would happen if you simply left their key alone but added your own key in addition to it? Now every time that they sent or received a message, it would be signed with their legitimate key as well as your own key, making it so you could read it in plaintext. That is exactly what we will be doing!

To get credit for this task, you must be able to read the messages of EVERY user on the server. So you need to generate a new 2048 RSA keypair (https://travistidwell.com/jsencrypt/demo/) and place it in the pubkey column in the clientDB. Then you just have to change the xname field to each user on the server (starting with any of the ones you've already encountered). Upload the modified DB to your emulator and log in using the credentials from task 4. When you log in as them on the app, it will automatically insert your new key into their v-card.

Each server has 10 users, including the test users from Task 1. So after you have logged in as all 10 users, you can submit the generated public and private key for credit. You can use the contact list to discover new users.

### Common Problems

If you get a message that the user will not be able to read future messages, then you may have forgotten to restore the top leader's original public key after 6a. Refer to those instructions to see how to set it back.

## Walkthrough Video
https://www.youtube.com/watch?v=fzGrm2OVizM

[![NSA Codebreaker Challenge 2019 - Task 6b Solution](https://img.youtube.com/vi/fzGrm2OVizM/0.jpg)](https://www.youtube.com/watch?v=fzGrm2OVizM)

