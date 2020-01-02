# Task 2 Writeup

## Task Description

The TerrorTime APK file contains metadata that describes various security properties of the application that we want to know. Since we now have a copy of the APK thanks to the military operation described in Task 1, we need you to identify and submit the following:

1. App Permissions
1. The SHA256 hash of the Code Signing Certificate
1. The Common Name of the Certificate Signer

## Provided Files

* Captured Traffic (terrortime.pcapng)

## Walkthrough

APK files are actually zip archives containing some metadata about the app along with various resources and the compiled code itself. Change the file extension to .zip and you can extract it using your archive utility of choice. Then open AndroidManifest.xml and you'll see the permissions that are required near the top (They are the all-caps strings that start with android.permission.).

To get the certificate information about the apk, you can use the apksigner utility that comes with Android Studio (your path to it may vary if it is not already in your PATH variable). Then command will be:

* apksigner verify --print-certs terrorTime1.apk

This will print the sha256 hash of the certificate as well as the common name (Starts with CN=)

## Walkthrough Video
https://www.youtube.com/watch?v=SgESdA6BrDY

[![NSA Codebreaker Challenge 2019 - Task 1-3 Solutions](https://img.youtube.com/vi/SgESdA6BrDY/0.jpg)](https://www.youtube.com/watch?v=SgESdA6BrDY)

