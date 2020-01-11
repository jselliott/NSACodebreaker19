# Task 1 Writeup

## Task Description

There are many challenges that we will need to overcome in order to exploit TerrorTime. The first is that we do not yet have a copy of it. We have learned few details through intelligence sources, but the terrorists have managed to keep the app hidden. It is not publicly available on any App Store. Fortunately, as part of a recent military operation, specialized collection gear was forward deployed near the terrorist's area of operations. This resulted in a trove of collected traffic and we need your help to analyze it. Your first task is to find and extract a copy of the TerrorTime Android Package (APK) file from the packet capture. Submit the APK's SHA256 hash. This will help us search other intelligence sources for connections to users. To test out the app, we also need the registration information their leadership uses to register each client. Analyze the packet capture for this data and submit the registration information for 2 clients (in any order).

## Provided Files

* [Captured Traffic (terrortime.pcapng)](terrortime.pcapng)

## Walkthrough

In order to complete this task, we can simply open the provided packet capture in Wireshark and then export HTTP objects (File -> Export Objects -> HTTP). This will reveal two files that you can save: terrorTime.apk and README.developer

You can get the sha-256 hash of the apk file by using the following commands depending on your platform:

* sha256sum terrorTime.apk (Linux/OSX)
* Get-FileHash terrorTime.apk (Windows PowerShell)

To retrieve the client credentials, you can open the README file and you'll see two test accounts formatted like user--vhost-number@terrortime.app and a client secret. The submission should be formatted like:
  
    test1--vhost-1234@terrortime.app:secret1
    test2--vhost-1234@terrortime.app:secret2

## Walkthrough Video
https://www.youtube.com/watch?v=SgESdA6BrDY

[![NSA Codebreaker Challenge 2019 - Task 1-3 Solutions](https://img.youtube.com/vi/SgESdA6BrDY/0.jpg)](https://www.youtube.com/watch?v=SgESdA6BrDY)

