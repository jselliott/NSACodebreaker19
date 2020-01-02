# Task 4 Writeup

## Task Description

While analyzing the TerrorTime SQLite database found on the terrorist’s device, analysts discovered that the database has cached credentials but requires a pin to log in. If we can determine how the credentials are protected and find a way to recover the pin, we should be able to masquerade as the arrested terrorist. Perform reverse engineering to identify how the terrorist’s credentials are protected and submit the terrorist's Client ID and Client Secret. Once you have uncovered their credentials, masquerade (i.e., login) as him using the TerrorTime app. Review their chat history and assess additional information regarding their organization. Though the app encrypts messages back and forth, the terrorists have previously spoken in some form of code to ensure their plans were protected. To prove completion of this task, you will need to analyze the terrorist's conversation history in order to uncover/deduce the following information:

1. Terror Cell Leader's Username
1. The date on which the action will occur

## Walkthrough

### Device Setup

This is the first time that we will be actually starting up the TerrorTime app. Before starting this task you will need to install Android Studio and configure a virtual device. If you are unfamiliar with this process, then you can read the guide here:

https://developer.android.com/studio/run/managing-avds

Once you have the device configured and started, you can drag and drop the provided APK file (Version 2 is available after finishing task 1) onto the emulator screen and it will install it. When you start the app, you'll see that it accepts a username and pin to log in. There are also options for registering a new user or provisioning the device for an existing user.

In the case of task 4, we can use the clientDB from task 3 to provision the device for us. While the emulator is running, you can view the files on the device by clicking on View -> Tool Windows -> Device File Explorer. Then you can find the clientDB on the device at:

* /data/data/com.badguy.terrortime/databases/clientDB.db

Right-click on this file and click upload, then you can select clientDB.db file from task 3. Now the device is set up as if it was the arrested terrorist who is using the app.

### Login

If you open the clientDB.db file in your SQLite Browser then you can see the username of the arrested terrorist in the cid field (which stands for Client ID). However, the pin is a little trickier. If you look at the checkpin field, you'll see a blob of hex bytes that appear to be an encoded form of the 6-digit pin. In this case, it turns out that the field contains a SHA-256 hash of the user's pin.

Since there are a limited number of 6-digit pins possible, we can iterate through all of them with a simple python script, generate the SHA-256 hash and compare it to the bytes from the DB. When we find a match, then the 6-digit user pin will be revealed. (See pin.py)

Once we have the username and pin, we can put them into the emulator and log in as the terrorist from task 3.

### Intel Gathering

For this task, we need to gather the cell leader's username and the time of the action. After logging in, you will see two conversations. If you look at each one, you'll notice that one of them is very informal and refers to things like "not dissapointing sir", etc. While the other one is more formal, revealing that this is the cell leader. Make a note of the username to submit for credit.

For the action date, you'll see a mention of a holiday, something like "Two days before Valentine's Day". And then later there will be a specific time like 1930. Using a unix time stamp converter in this case, you can put in 04/12/2020 19:30 and get back the timestamp 1555097400, which you can submit for credit. (Yours will be different)

## Walkthrough Video
https://www.youtube.com/watch?v=F8ptbLlQWoE

[![NSA Codebreaker Challenge 2019 - Task 4 Solutions](https://img.youtube.com/vi/F8ptbLlQWoE/0.jpg)](https://www.youtube.com/watch?v=F8ptbLlQWoE)

