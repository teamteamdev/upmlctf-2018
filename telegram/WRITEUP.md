# Telegram: Write-up

Перед нами Telegram-прокси Dante (из условия таска). Посмотрим, как работает *авторизация* в этом прокси.

Оказывается, она работает через PAM — т.е. в прокси можно авторизоваться под тем же логином, что и в линухе 
на хост-машине.

Раз это машина с флагами, значит при наличии шелла можно их найти. Зайдем под юзером `proxy`:

```bash
$ ssh proxy@socks.ctf.upml.tech
proxy@socks.ctf.upml.tech's password:
...
This account is currently not available. See you later.
Connection to socks.ctf.upml.tech closed.
```

Заметим две вещи:

1. Нам выводится весь MotD — значит, шелл запустили, а потом вышли из него
2. Нам выводится сообщение `This account is currently not available. See you later.`

Если бы у юзера был заблокирован шелл (например, в `/usr/sbin/nologin`), нам бы просто вывелось
`This account is currently not available.`

Это значит, что сообщение выводится при запуске шелла, к примеру, через `.bashrc` или `.profile`, 
а дефолтный шелл всё же `sh` или `bash`.

Пробуем что-то другое: 

```bash
$ sftp proxy@socks.ctf.upml.tech
proxy@socks.ctf.upml.tech's password:
subsystem request failed on channel 0
Couldn't read packet: Connection reset by peer
```

Не работает... Остался ещё один вариант — можно передавать произвольные команды при запуске `ssh`, чтобы 
не входить в интерактивный режим (удобно для автоматического запуска команд). Работает это так:

```bash
$ ssh proxy@socks.ctf.upml.tech ls -la
proxy@socks.ctf.upml.tech's password:
total 16
drwxr-xr-x 2 root root 4096 Jul 30 20:04 .
drwxr-xr-x 4 root root 4096 Jul 30 19:14 ..
-rwxr-xr-x 1 root root   70 Jul 30 19:17 .profile
-rw-r--r-- 1 root root   57 Jul 30 19:20 super_secret_file.txt
```

Работает! Теперь можно вывести файл точно так же:

```bash
$ssh proxy@socks.ctf.upml.tech cat super_secret_file.txt
proxy@socks.ctf.upml.tech's password:
TOTALLY SECRET FLAGS!!!!

uctf_lock_proxy_users_properly
```

Флаг: **uctf_lock_proxy_users_properly**
