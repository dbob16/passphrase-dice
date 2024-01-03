# Introduction

This project is a little bit of a Python script which assists users into using EFF.org's Dice-Generated Passphrases. As a result, wordlist.txt is subject to the licensing EFF assigns to their long-wordlist at the time of pushing it.

The wordlist file itself is created by the EFF (Electronic Frontier Foundation).

# Custom Wordlists

As this script just looks into the "wordlist.txt" file, you are free to put in your own wordlists as long as the follow the same general format:

```
[number or dice sequence]   word
```

# Inner workings

The first thing the script does is use SQL Alchemy to create a memory database, and then imports into the memory database all of the line items into said database. This creates a searchable index.

The random function actually uses this database instead, with a random order SQL function, to make sure that custom wordlists can be utilized (4 dice wordlists for instance).