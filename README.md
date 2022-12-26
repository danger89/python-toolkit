# python-toolkit
My customize Python toolkit. Currently implemented commands are as follow:

| Command | Description                            |
| ------- | -------------------------------------- |
| m3u8d   | Download video files via m3u8 url.     |
| webimd  | Download images from an html document. |

# Usage

### m3u8d

```shell
python -m pytk m3u8d [-h] [-n NAME] [-t THREADS] [--use-fake-agent] [--no-verify-ssl] url
```

**Arguments**

- `url`: URL to the requested m3u8 file.
- `name`: Filename of the downloaded video. By default, it's parsed from url.
- `threads`: Number of threads which is used for download. It's `15` by default.
- `use-fake-agent`: If set, `User-Agent` in the header of requests will be generated with `fake-useragent`.
- `no-verify-ssl`: If set, connection will not be verified even if it's an https connection. Be cautious with this option.

### webimd

```shell
python -m python_toolkit webimd [-h] [-i INPUT] [-o OUTPUT] [-t THREADS] [-p PREFIX]
```

**Arguments**

- `input`: The input html document. Please notice that the html is loaded from a file rather than download from an url or from the console, in order to avoid incorrect outcoming caused by dynamic website loading or inefficiency caused by long console input.
- `output`: The directory where download images will be stored.
- `threads`: Number of threads which is used for download. It's `15` by default.
- `prefix`: Prefix of the image url. It's made use of when the source url is relative.

It's highly recommended that you add follow aliases to your `.bashrc` (or `.zshrc` or whatever rc files) so that the commands can be called much more easily.

### Aliases

```bash
alias m3u8d="python -m pytk m3u8d"
alias webimd="python -m pytk webimd"
```

# Roadmap

- Image compression command like [imgbot/Imgbot](https://github.com/imgbot/Imgbot).
