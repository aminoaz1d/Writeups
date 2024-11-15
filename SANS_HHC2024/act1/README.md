# Act 1

[Back to main](../README.md)

Act 1 had more challenges that, generally, were less game focused.

## Challenge 1: curling

The curling challenge revolved around the use of the `curl` command to carry out various tasks. You are presented with a terminal with which you need to interact:

![A terminal with instructions for the curlingfun challenge](img/1.curlingfun.PNG)

### Silver

Silver was straightforward - I just needed to answer the following questions

1) Unlike the defined standards of a curling sheet, embedded devices often have web servers on non-standard ports.  Use curl to retrieve the web page on host "curlingfun" port 8080.

```bash
curl curlingfun:8080
```

2) Embedded devices often use self-signed certificates, where your browser will not trust the certificate presented.  Use curl to retrieve the TLS-protected web page at https://curlingfun:9090/

```bash
curl -k https://curlingfun:9090
```

3) Working with APIs and embedded devices often requires making HTTP POST requests. Use curl to send a request to https://curlingfun:9090/ with the parameter "skip" set to the value "alabaster", declaring Alabaster as the team captain.

```bash
curl -k --data "skip=alabaster" https://curlingfun:9090
```

4) Working with APIs and embedded devices often requires maintaining session state by passing a cookie.  Use curl to send a request to https://curlingfun:9090/ with a cookie called "end" with the value "3", indicating we're on the third end of the curling match.

```bash
curl -k -H "Cookie: end=3;" https://curlingfun:9090
```

5) Working with APIs and embedded devices sometimes requires working with raw HTTP headers.  Use curl to view the HTTP headers returned by a request to https://curlingfun:9090/

```bash
curl -k -I https://curlingfun:9090
```

6) Working with APIs and embedded devices sometimes requires working with custom HTTP headers.  Use curl to send a request to https://curlingfun:9090/ with an HTTP header called "Stone" and the value "Granite".

```bash
curl -k -H "Stone: Granite" https://curlingfun:9090
```

7) curl will modify your URL unless you tell it not to.  For example, use curl to retrieve the following URL containing special characters: https://curlingfun:9090/../../etc/hacks

```bash
curl -k --path-as-is https://curlingfun:9090/../../etc/hacks
```

"Great work! 
 
Once HHC grants your achievement, you may close this terminal."

Yay!

### Gold

To locate the gold challenge, I ran the `ls` command

```bash
alabaster@curlingfun:~$ ls
HARD-MODE.txt  HELP
```

I then needed to read `HARD-MODE.txt` to get the instructions:

```bash
alabaster@curlingfun:~$ cat HARD-MODE.txt 
Prefer to skip ahead without guidance?  Use curl to craft a request meeting these requirements:

- HTTP POST request to https://curlingfun:9090/
- Parameter "skip" set to "bow"
- Cookie "end" set to "10"
- Header "Hack" set to "12ft"
```

This is similar to previous solutions:

```bash
curl -k --data "skip=bow" -H "Cookie: end=10;" -H "Hack: 12ft" https://curlingfun:9090/
```

Which works and responds with:

```bash
Excellent!  Now, use curl to access this URL: https://curlingfun:9090/../../etc/button
```

Naturally:

```bash
alabaster@curlingfun:~$ curl -k --path-as-is https://curlingfun:9090/../../etc/button

Great!  Finally, use curl to access the page that this URL redirects to: https://curlingfun:9090/GoodSportsmanship
```

Not too bad:

```bash
alabaster@curlingfun:~$ curl -k -L https://curlingfun:9090/GoodSportsmanship

Excellent work, you have solved hard mode!  You may close this terminal once HHC grants your achievement.
```

That's a wrap on Gold!

## Challenge 2: Frosty Keys

Frosty keys is a slightly more interesting challenge involving discovering the PINs for an ATM-like machine.

![A numerical pad, similar to a telephone, with a sticky note taped to it and a digital screen below.](img/2.frosty_keys_pad.PNG)

### Silver

The Silver challenge can be solved via brute force or informed guessing, but we'll save that for later and instead look at intended solutions.

#### Discovering the digits - With Light

Before completing this challenge, you are instructed to find a UV flashlight to look at the keypad with. When doing so, I could shine it over the numbers and see how they are used:

![The keypad with a UV flashlight shining on it exposes a fingerprint on the 8 key.](img/2.frosty_keys_print.PNG)

Using this method, I determined that the character set is `2,6,7,8`.

#### Discovering the digits - With Javascript

I examined the game's source code and found the list of keys that would be highlighted:

```javascript
// check if flashlight is over special keys
        function checkOverlap() {
            clearOverlays();
            const keysToCheck = ['2', '7', '6', '8', 'Enter'];
```

This reveals the same list of `2,6,7,8`. Realistically, this was enough to guess the solution with a quick glance, but I'll follow through with the intended solution.

#### Decoding the Sticky Note

When I clicked on the sticky note it was shown much more clearly:

![A sticky note showing some numbers separated by colons.](img/2.frosty_keys_hhc2024-stickynote.png)
Using the [book](https://frost-y-book.com/) we were instructed to find before the challenge, each of these sets of numbers corresponds to `[page]:[word]:[char]` for a total of 5 characters:

![A book with the letter S circled as it is the 1st character of the 6th word of the 2nd page.](img/2.frosty_keys_book.PNG)

The first hint corresponds to the character `S` as it is the first character of the sixth word of the second page of the book, 2:6:1. The rest of the characters follow below:

| Hint   | Character | Telephone key |
| ------ | --------- | ------------- |
| 2:6:1  | S         | 7             |
| 4:19:3 | A         | 2             |
| 6:1:1  | N         | 6             |
| 3:10:4 | T         | 8             |
| 14:8:3 | A         | 2             |
This method of encoding is known as an Ottendorf Cipher, which is alluded to in the game's source:

```javascript
this.load.image('note', '/static/images/note.png'); // note about Ottendorf
```

After decoding the cipher, I discovered the secret word was `SANTA`. Unsurprisingly, these characters all corresponded to the characters `2,6,7,8` previously discovered, so entering it encoded as `72682` and pressing enter on the keypad was successful for getting Silver.

![The keypad displays the solution, 72682, and an overlay on the screen reads "Success! You have defeated the Frosty Keypad!!!!](img/2.frosty_keys_silver.PNG)

Upon success, you are rewarded with a file named `shreds.zip` to be used in [Challenge 3: Hardware Hacking 101 Part 1](#### Challenge 3: Hardware Hacking 101 Part 1)

### Gold

The hints point to another solution and suggest you should brute force to get it.  To carry this out, I made two assumptions:

1. The character set would be the same, remaining `2,6,7,8`.
2. The length of the code would remain the same, specifically five characters wrong.

This combination meant an upper bound of 1024 pins, which was small enough to not worry about getting wrong.

When submitting a code (pressing Enter), the browser issues the following request:

```http
POST /submit?id=null HTTP/2
Host: hhc24-frostykeypad.holidayhackchallenge.com
Cookie: ...headers omitted for brevity...

{"answer":"72682"}
```

I used Burp Intruder to quickly carry out the brute force attack with minimal work, with the following configuration:

![Burp Intruder with the payload position in the answer parameter. The payload type is set to Brute Forcer and the settings match the two assumptions above.](img/2.frosty_keys_burpintruder1.PNG)

This began working, but I was quickly met with errors in Burp as the API started returning 429 errors. Disabling Automatic Throttling or manually triggering the 429 in Repeater revealed the the error message returned from the server was:

```http
HTTP/2 429 Too Many Requests
Server: gunicorn
Date: Thu, 14 Nov 2024 22:04:20 GMT
Content-Type: application/json
Content-Length: 89
Via: 1.1 google
Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000

{"error":"Too many requests from this User-Agent. Limited to 1 requests per 1 seconds."}
```

Seeing that the filtering was being carried out by `User-Agent` was unusual, so I modified the Intruder parameters to also change the `User-Agent` by inserting another payload position at the end of that header and setting Intruder to Battering Ram mode:

![Burp Intruder is now shown to be configured to use Battering ram attack mode and insert another payload into the User-Agent header.](img/2.frosty_keys_burpintruder2.PNG)

This stopped the errors and eventually revealed a 200 response for the code `22786`:

![The keypad displays the solution, 22786, and an overlay on the screen reads "Success! You have defeated the Frosty Keypad!!!!](img/2.frosty_keys_gold.PNG)

Far out!

## Challenge 3: Hardware Hacking 101 Part 1

Hardware Hacking 101 Part 1 revolves around connecting to Santa's Little Helper (SLH) using a NP2103 UART Bridge (a clear play on the CP2103 USB-to-UART bridge) in an attempt to get a shell. Opening the challenge you are shown a visual representation of the SLH, the bridge, and a USB terminal device:

![A cartoon table showing a visual representation of the SLH, the bridge, and a USB terminal device](img/3.hw101pt1_table.PNG)

### Silver

#### Reconstruction - `shreds.zip`

`shreds.zip` contained 1000 `1x1000` pixel images that vaguely looked like they belonged together in one big `1000x1000` pixel image. In one of the hints, Marcel Nougat gave me a link to [heuristic_edge_detection.py](https://gist.github.com/arnydo/5dc85343eca9b8eb98a0f157b9d4d719) to help reconstruct the image. I needed to install some libraries (I think it requires `pillow` and `numpy`), but after that it was pretty simple to run, yielding:

![The shreds reassembled into a cartoon scroll, but they are backward and sliced improperly.](img/3.hw101pt1_assembled_image.png)

This was readable enough, but I didn't *actually* do the above at first. Before I noticed the hint, I asked ChatGPT to reassemble it and got:

![The scroll is reassembled properly and shows UART configuration parameters](img/3.hw101pt1_final_reconstructed_image.jpg)

This scroll gave me the UART configuration listed below:

| Parameter                       | Value  |
| ------------------------------- | ------ |
| Baud                            | 115200 |
| Parity                          | Even   |
| Data                            | 7 bits |
| Stop bits ("stoppits" \[sic]\]) | 1 bit  |
| Flow Control                    | RTS    |

Moving on...

#### Wiring

The NP2103 had labels but the SLH did not, so I just assumed that the pinouts were the same between the two (I noticed SLH *was* labelled while writing up and I hadn't noticed, so that is highlighted below) . I clicked the USB cable to connect the NP2103 to the terminal device and clicked the power button to turn it on:

![The devices with labels and buttons circled. Seriously, I'm pretty sure that GRTV label wasn't there...](img/3.hw101pt1_wiring.PNG)

Just make sure you swap the TX and RX wires between the two devices - if the SLH is transmitting on a specific pin (TX) you want that to go to the NP2103's receive pin (RX).

I used the arrow keys to configure the UART parameters and made sure to set the Port to `USB0` for the USB cable:

![The terminal device with the UART parameters set](img/3.hw101pt1_params.PNG)

I clicked start:

![Magic smoke coming out of a burning integrated circuit](img/3.hw101pt1_smoke.PNG)

And got the no-no smoke. A quick look at the NP2103 revealed a voltage switch, which I changed from `5v` to `3v` and clicked start again:

![A terminal window with a success message overlayed on top of the game screen](img/3.hw101pt1_silver.PNG)

That's Silver. Yippee!

### Gold

 Gold doesn't require you to use the graphical UI. I examined `main.js` and found the following hint:
 
```javascript
// Build the URL with the request ID as a query parameter
// Word on the wire is that some resourceful elves managed to brute-force their way in through the v1 API.
// We have since updated the API to v2 and v1 "should" be removed by now.
// const url = new URL(`${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/v1/complete`);
const url = new URL(`${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/v2/complete`);
```

This implied that `v2` was not good and `v1` was what I was after. I intercepted the submission from my original solve and modified it to submit to `v1`:

```http
POST /api/v1/complete HTTP/2
Host: hhc24-hardwarehacking.holidayhackchallenge.com
Cookie: ...headers omitted for brevity...

{"requestID":"[REDACTED]","serial":[3,9,2,2,0,3],"voltage":3}
```

And this gave me Gold!

## Challenge 4: Hardware Hacking 101 Part 2

Hardware Hacking 101 Part 2 presents you with a shell on the Santa's Little Helper (SLH) device. Initially, it gives you the option to boot or modify u-boot parameters, but u-boot is a fake (I attempted to `setenv bootargs init=/bin/bash` to get `root`, but the u-boot environment doesn't seem functional) so that was just a fun reference to real embedded environments:

![The challenge begins with a U-Boot Boot Menu](img/4.hw101pt2_uboot.PNG)

The goal of this challenge is to grant administrative rights to id `42` in Santa's Little Helper.

### Silver

To start, I selected option 1 to boot into a bash terminal and was greeted with usage instructions for the `slh` command:

```bash
--------------------------------------------------------
                   ___     _      _  _   
                  / __|   | |    | || |  
                  \__ \   | |__  | __ |  
                  |___/   |____| |_||_|  
                _|"""""|_|"""""|_|"""""| 
                "`-0-0-'"`-0-0-'"`-0-0-' 
--------------------------------------------------------
  Santa's Little Helper - Access Card Maintenance Tool

          Tool Name: slh

options:
  -h, --help            show this help message and exit
  --view-config         View current configuration.
  --view-cards          View current values of all access cards.
  --view-card ID        View a single access card by ID.
  --set-access ACCESS_LEVEL
                        Set access level of access card. Must be 0 (No Access) or 1 (Full Access).
  --id ID               ID of card to modify.
  --passcode PASSCODE   Passcode to make changes.
  --new-card            Generate a new card ID.
--------------------------------------------------------
```

This appears to require a passcode, but I decided to try without one anyway:

```bash
slh@slhconsole\> slh --set-access 1 --id 42
Invalid passcode. Access not granted.
```

Since that didn't work, I needed to find the passcode. Running `ls` revealed a `.bash_history` file:

```bash
slh@slhconsole\> ls -lha
total 156K
drwxrwxr-t 1 slh  slh  4.0K Nov 13 14:44 .
drwxr-xr-x 1 root root 4.0K Nov 13 14:44 ..
-r--r--r-- 1 slh  slh   518 Oct 16 23:52 .bash_history
-r--r--r-- 1 slh  slh  3.9K Sep 23 20:02 .bashrc
-r--r--r-- 1 slh  slh   807 Sep 23 20:02 .profile
-rw-r--r-- 1 root root 128K Nov 13 14:44 access_cards     
slh@slhconsole\> cat .bash_history 
cd /var/www/html
ls -l
sudo nano index.html
cd ..
rm -rf repo
sudo apt update
sudo apt upgrade -y
ping 1.1.1.1
slh --help
slg --config
slh --passcode CandyCaneCrunch77 --set-access 1 --id 143
df -h
top
ps aux | grep apache
sudo systemctl restart apache2
history | grep ssh
clear
whoami
crontab -e
crontab -l
alias ll='ls -lah'
unalias ll
echo "Hello, World!"
cat /etc/passwd
sudo tail -f /var/log/syslog
mv archive.tar.gz /backup/
rm archive.tar.gz
find / -name "*.log"
grep "error" /var/log/apache2/error.log
```

There is a line with the password `CandyCaneCrunch77` in it being used to set id `143` to admin (`1`). I changed the id to `42` and ran the command:

```bash
slh@slhconsole\> slh --passcode CandyCaneCrunch77 --set-access 1 --id 42 

       *   *   *   *   *   *   *   *   *   *   *
   *                                             *
*      ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄     *
 *  $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$$\  $$$$$$\   $$$$$$\  * 
  * $$  __$$\ $$  __$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$\ *
   *$$ /  $$ |$$ /  \__|$$ /  \__|$$ |      $$ /  \__|$$ /  \__| *
    $$$$$$$$ |$$ |      $$ |      $$$$$\    \$$$$$$\  \$$$$$$\   
   *$$  __$$ |$$ |      $$ |      $$  __|    \____$$\  \____$$\  *
  * $$ |  $$ |$$ |  $$\ $$ |  $$\ $$ |      $$\   $$ |$$\   $$ | *
*   $$ |  $$ |\$$$$$$  |\$$$$$$  |$$$$$$$$\ \$$$$$$  |\$$$$$$  |   *
 *  \__|  \__| \______/  \______/ \________| \______/  \______/  *
*         *    ❄             ❄           *        ❄    ❄    ❄   *
   *        *     *     *      *     *      *    *      *      *
   *  $$$$$$\  $$$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  $$\  *
   * $$  __$$\ $$  __$$\ $$  __$$\ $$$\  $$ |\__$$  __|$$  _____|$$  __$$\ $$ | *
  *  $$ /  \__|$$ |  $$ |$$ /  $$ |$$$$\ $$ |   $$ |   $$ |      $$ |  $$ |$$ |*
  *  $$ |$$$$\ $$$$$$$  |$$$$$$$$ |$$ $$\$$ |   $$ |   $$$$$\    $$ |  $$ |$$ | *
 *   $$ |\_$$ |$$  __$$< $$  __$$ |$$ \$$$$ |   $$ |   $$  __|   $$ |  $$ |\__|*
  *  $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$$$ |   $$ |   $$ |      $$ |  $$ |   *
*    \$$$$$$  |$$ |  $$ |$$ |  $$ |$$ | \$$ |   $$ |   $$$$$$$$\ $$$$$$$  |$$\ *
 *    \______/ \__|  \__|\__|  \__|\__|  \__|   \__|   \________|\_______/ \__|  *
  *                                                            ❄    ❄    ❄   *
   *      *    *    *    *    *    *    *    *    *    *    *    *    *    *                                                                                                                                        

Card 42 granted access level 1.
```

Fin.

### Gold

To solve Gold, the elves state you should modify the program's database directly and provide a link to a [CyberChef recipe](https://gchq.github.io/CyberChef/#recipe=HMAC(%7B'option':'UTF8','string':''%7D,'SHA256')) for a hashing algorithm.

I first tried to find the database:

```bash
slh@slhconsole\> ls -lha
total 156K
drwxrwxr-t 1 slh  slh  4.0K Nov 13 14:44 .
drwxr-xr-x 1 root root 4.0K Nov 13 14:44 ..
-r--r--r-- 1 slh  slh   518 Oct 16 23:52 .bash_history
-r--r--r-- 1 slh  slh  3.9K Sep 23 20:02 .bashrc
-r--r--r-- 1 slh  slh   807 Sep 23 20:02 .profile
-rw-r--r-- 1 root root 128K Nov 13 14:44 access_cards
slh@slhconsole\> file access_cards 
access_cards: SQLite 3.x database, last written using SQLite version 3040001, file counter 4, database pages 32, cookie 0x2, schema 4, UTF-8, version-valid-for 4
```

Using `file`, I discovered a file `access_cards` that was a [`sqlite`](https://www.sqlite.org/) database. I used the `sqlite3` command to open and explore the database:

```sql
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open access_cards
sqlite> .schema
CREATE TABLE access_cards (
            id INTEGER PRIMARY KEY,
            uuid TEXT,
            access INTEGER,
            sig TEXT
        );
CREATE TABLE config (
            id INTEGER PRIMARY KEY,
            config_key TEXT UNIQUE,
            config_value TEXT
        );
sqlite> select * from config;
1|hmac_secret|9ed1515819dec61fd361d5fdabb57f41ecce1a5fe1fe263b98c0d6943b9b232e
2|hmac_message_format|{access}{uuid}
3|admin_password|3a40ae3f3fd57b2a4513cca783609589dbe51ce5e69739a33141c5717c20c9c1
4|app_version|1.0
sqlite> select * from access_cards where id = 42;
42|c06018b6-5e80-4395-ab71-ae5124560189|0|ecb9de15a057305e5887502d46d434c9394f5ed7ef1a51d2930ad786b02f6ffd
sqlite> select * from access_cards where id = 143;
```

All the relevant information was listed in the combination of `config` and `access_cards`:

| Config Parameter    | Value                                                            |
| ------------------- | ---------------------------------------------------------------- |
| hmac_secret         | 9ed1515819dec61fd361d5fdabb57f41ecce1a5fe1fe263b98c0d6943b9b232e |
| hmac_message_format | {access}{uuid}                                                   |

| Card ID | UUID                                 | Permission |
| ------- | ------------------------------------ | ---------- |
| 42      | c06018b6-5e80-4395-ab71-ae5124560189 | 0          |

I plugged this information into CyberChef:

![A CyberChef recipe outputting the proper signature](img/4.hw101pt2_cyberchef.PNG)

I updated the database with this signature:

```sql
sqlite> update access_cards set access=1, sig="135a32d5026c5628b1753e6c67015c0f04e26051ef7391c2552de2816b1b7096" where id=42;
sqlite> 
       *   *   *   *   *   *   *   *   *   *   *
   *                                             *
*      ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄     *
 *  $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$$\  $$$$$$\   $$$$$$\  * 
  * $$  __$$\ $$  __$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$\ *
   *$$ /  $$ |$$ /  \__|$$ /  \__|$$ |      $$ /  \__|$$ /  \__| *
    $$$$$$$$ |$$ |      $$ |      $$$$$\    \$$$$$$\  \$$$$$$\   
   *$$  __$$ |$$ |      $$ |      $$  __|    \____$$\  \____$$\  *
  * $$ |  $$ |$$ |  $$\ $$ |  $$\ $$ |      $$\   $$ |$$\   $$ | *
*   $$ |  $$ |\$$$$$$  |\$$$$$$  |$$$$$$$$\ \$$$$$$  |\$$$$$$  |   *
 *  \__|  \__| \______/  \______/ \________| \______/  \______/  *
*         *    ❄             ❄           *        ❄    ❄    ❄   *
   *        *     *     *      *     *      *    *      *      *
   *  $$$$$$\  $$$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  $$\  *
   * $$  __$$\ $$  __$$\ $$  __$$\ $$$\  $$ |\__$$  __|$$  _____|$$  __$$\ $$ | *
  *  $$ /  \__|$$ |  $$ |$$ /  $$ |$$$$\ $$ |   $$ |   $$ |      $$ |  $$ |$$ |*
  *  $$ |$$$$\ $$$$$$$  |$$$$$$$$ |$$ $$\$$ |   $$ |   $$$$$\    $$ |  $$ |$$ | *
 *   $$ |\_$$ |$$  __$$< $$  __$$ |$$ \$$$$ |   $$ |   $$  __|   $$ |  $$ |\__|*
  *  $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$$$ |   $$ |   $$ |      $$ |  $$ |   *
*    \$$$$$$  |$$ |  $$ |$$ |  $$ |$$ | \$$ |   $$ |   $$$$$$$$\ $$$$$$$  |$$\ *
 *    \______/ \__|  \__|\__|  \__|\__|  \__|   \__|   \________|\_______/ \__|  *
  *                                                            ❄    ❄    ❄   *
   *      *    *    *    *    *    *    *    *    *    *    *    *    *    *       
```

Now Act 1 is done!

## Conclusion

Act 1 started to introduce more technical contents to the challenge. Can't wait for [Act 2](../act2/README.md)!
