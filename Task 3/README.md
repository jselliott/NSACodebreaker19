# Task 3 Writeup

## Task Description

Analysts found TerrorTime installed on a device that was taken from a terrorist arrested at a port of entry in the US. They were able to recover the SQLite database from the TerrorTime installation on the device, which should provide us with more in-depth knowledge about the terrorist's communications and the TerrorTime infrastructure. Your goal for this task is to analyze the database and submit the addresses of the TerrorTime OAUTH (authentication) and XMPP (chat) servers.

## Provided Files

* Database (clientDB.db)

## Walkthrough

For this task, we are provided with an SQLite database that is taken from the device of an arrested terrorist. You can open it by using a database browser like DB Browser for SQLite (https://sqlitebrowser.org/). In the "Clients" table, you will see two columns, xsip and asip, that contain the domain names of the XMPP and OAUTH servers:

* chat.terrortime.app
* register.terrortime.app

Ping these two domains to get the IP addresses to submit for credit.

## Walkthrough Video
https://www.youtube.com/watch?v=SgESdA6BrDY

[![NSA Codebreaker Challenge 2019 - Task 1-3 Solutions](https://img.youtube.com/vi/SgESdA6BrDY/0.jpg)](https://www.youtube.com/watch?v=SgESdA6BrDY)

