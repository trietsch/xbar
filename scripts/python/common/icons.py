from dataclasses import dataclass


@dataclass
class Icon(object):
    base64_image: str


class Icons(object):
    AUTHORED = Icon("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAIRlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAABCgAwAEAAAAAQAAABAAAAAAx28c8QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAUVJREFUOBG9kjtOhVAQhnmHBJZgaEjcAKEghkdCaI0NjVjaaLS1t7Oy0tsZO5YBK2ALECsKFgAETnCGcG4OV28wJnoaODPzzcz/A8f91wmCQIrjWPztPJ6C2Ii+/+hJAdd1r6IoOkOIxjYbWJYlY1GSJCeO40y2bU9hGLoYo3IEvHx3EC6KYoDJD1VVXauqeiHLMkcIOcX6pmlmWXttbBMK+75/07btDnOKojwahvGepukHW/tlAxbuum43wuF5nhNFsV/glYmHn0Wq63rEyQgPwzDC2pKu63d5nj9jc8yzG7ASsBkB+BbgV4AJwKKmafdZlr1ADg0dWBjfZwmLo8TzvMsFxsmb8L5BWZZzIzDsXBAEDtfemkw3mT0AXXifTNPk+r6fAH4CzW8QQ8NWmrHw2GH9wJpDg49xq7iATtO/bJX5q8snUfGCsohklvsAAAAASUVORK5CYII=")
    REVIEW = Icon("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAhGVYSWZNTQAqAAAACAAFARIAAwAAAAEAAQAAARoABQAAAAEAAABKARsABQAAAAEAAABSASgAAwAAAAEAAgAAh2kABAAAAAEAAABaAAAAAAAAAEgAAAABAAAASAAAAAEAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAEKADAAQAAAABAAAAEAAAAADHbxzxAAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpMwidZAAABWklEQVQ4EX2RPS9FQRCGj+8aFRqFRCEhPkqNykeiE7VEFP6Exq+4P0Ei0WtFoxStEJUIISoSwfPs7lzOPTf3TZ6zMzu7s3NmqqqqBkFNwQk8wze8wTksgBrIS/fvGts/cAk7sAhbcAbu74OKx7JXvr7soaPa7p+zW+KrZatRiWX7svIF6S/rCKtqwXWycqyYefGfLVt1lhivzRH7hEkPIR9I0hiD2+ym5hUzLTZTPYIJJnRQX15ypnecCLQzlwNxcBR/GF7Kvj1L8sIVHGQ3jcqyvWgserCH/QT3YCwqw8xzNqPd7iZH6gXHqqykIedskhbYsHGYgWNwX7YhFM1NfjjO2VHZLPvyAQ+wCYfwBaewBGooL/n7f3yOahmmc6j9vcCykleYL7u1JFbSbQrxzxvErcIkVhhJMOsySWey+M11YtETK1mpX+3tRSUmiUpuel9pRiOJE7mD2V9KFzzD9nMwuAAAAABJRU5ErkJggg==")

    PULL_REQUEST = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAVCAYAAABPPm7SAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAbVJREFUOBGNlD0ohVEYxw/XZ4muiZHFbMFgllLKJKuFYlAWm0ExKCmT3WBS7qyLO8soE5uPRVEGHxf/33H+b++te+Nfv/s85/l6zznvvTeE+mpWuC2lpmSnk0+sKfk1ZlGritgTxVxmTP63mMnFcAv59ZYWFJXEm7gRaFx8CXK7YlZMCCsbQsFqig7I0rQvXgQ5hmLNpfxBgQqclUQ/K6lPcMY78SzqaVjBU9ElqhQsCYaUBU87E2hIPAly64LGA+FjrcnPdCSPQrZdzKIh+EhzKdYr66GHxFpS4jVZBvg1dci/FSPCQ6lnl4gHZgM8COsB7yl/QWESZ+beMnkRpymKtU/Rp6DGryyfiw/yAIobyZdWN/+fAXUbHfQAnxtr3zV563piNUf4SFWcmS03EjlqULSe2P0bCz2yvrD8TuxjXcs3MWpFn9xuWfDqzkVebiZ2Iqihlp5lEZ1tHIkvDYlJFlKr8I74JZIbFYieqo/wGEMhPCTbnizGO+hMsftkqY39G3KYXBJs70q4CeuHsJNrwYUfC3o2RdS8PjnXjvAluZEC+/wm+NeqiAUR5ad5jXXDX7HwA+nmXWV5F/zGAAAAAElFTkSuQmCC")

    GREEN_CIRCLE = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAARlJREFUOBGVk7FtAkEQRf8MyKGRIKcBJFfgyAGWC6ADElIKQMgFkFlO3IELsCAgcgVINOAcJAgR3DJ/zKGT2V2dN7nT/HkzO7t/BX/W6/dz71RgGIA+Qui6LPIjwKKh+Jg8ztdVxOK/a7oe3BXb/QwBoxCClvHqV0QKCN61fT+e9j4P1LwA4dNm92XwUxVI/guWjU7rhUW806VzPZhVrZEz9iuc+Vhgldp2ahccp6l4UD+wxMwpmHE2JKt+2rnMjEZWr1eVSUxKds3R60oCEUFhJonE64WMVTqsXvZtFlmlPd1ht3o2QoasurfNntnsmGgMWT9EettMvYzlRWOW64yJXoCeprdF5S03DjXmlO+Axa+vsez03+d8BpC2a0RVWrdkAAAAAElFTkSuQmCC")
    GREEN_CIRCLE_SYNC = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAiZJREFUOBGVUz1oU1EUPuc+6zOooC0S6NC1QvwBdWihJSS2pdZJxDr5M4ggOnWy+DolFhed/Bl0sV2kRToZNa1pCkJ1cFGrdHUQiuJoSmru8Ts379aX6uIheefe75zv/N17mbbIRCWXoaDtEpEMkVCXMzN9IeIyNTYeFfKLK0kK+82Zmcz27nTnHSa+Asx4fIu2QvJgde3r2OzoSl1tLkBMfg5yPkkQoSlmygA72oKTVBDkhAZxmeLMLWQQ3pE05mrrlBWRUjKAJlKOYhz3/B5rFwwl1qQh527mF5560nipf1+wM7WKcvd6DNpiJoe2NQf2p2cmuVgEOVo8PswU7JE6veWQSqjCEPMtEK/HQYxykRXTjgVOHwrZhRklkzElYbpAoSxjUvthiwrZ8jj0R++vXLN5VEDR27Iamc1lrCE0jE/aYcb0qRaiN6qd4Jhd335vCWVChNkdkcedFmlTjT5sEsdeL0lTMKQeXYm1r50WWcPuJQaLn33oMJJe1U7ANWJpfnPPfCCqDk6i7CJ6/fxLNnpwcx6TtSPF3KsXE0sDo7Ad9P5otvzXMcbGHz9tvft2rvrdO9+oDJzmgKcxm1SMuWN0NzFaGrwLw1Xv3NTyrLbOZ8NQhpA1guORpB093Stm56+5oendBlBJOqC8kztCqYJ46h9kvcpj6h/o59Pst0Z6JPWkY9fudlRyDJCrDJk78T+sPrHoY7oP8vmWx+Stqv/3Of8GAyfgwIRMWmoAAAAASUVORK5CYII=")
    GREEN_CIRCLE_CHECKMARK = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAbdJREFUOBGVU80rRFEUP+fOYxrlI/bWirCyMIySjI+NjbJTWBArlmp6jZWNUmTjPyB2GIuRhiyF+AOU1GSIjeK9e5xzzXvd1Kvnbu655/x+5/si/Dn5i2y7r2GOAIaBqNWYER8R4DShYDfXV7i3Kaz/Pe79ZK1+/dgAggUiUoHevhFRA8KOam5Ydtv3vsRmHAjZr7wfM3nQJkTKCMVES+OoODGRqpHjkcUrBzIcFtG9HO/QvncTlXaQBQJucl/qmT0jOinHUdCpyPdmY5DPOjINK0kgl4v+FAfCkWY7ptuiiT5PyqmbeniAhEbcZ2YqgApXhaOqajnVF87vzTwRvsFRk276sEyVj02O2hOQzc1jNk0MlZwe1zVU4yQGEKHMlS6vpU+ucucj05poPsRZguJoj+GbIPVNkM31Ht0lAbvXMoWtfCnbRah3QowtMFfJhtk6LmmdI7qrmcKzez3R5BEd8NjCum2scFFW19Nw+3cSCnGD025jwphNCuRgjGYTc6XsFmlaDIxxblS4ne8vLJkmym7zfItxiAbDWMPhh3EgOy27LV7Nh4nwJDbBBP9AYKYEG//f7/wDKPq20ttyqQEAAAAASUVORK5CYII=")

    RED_CIRCLE = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAPRJREFUOBGlU0EOgjAQHKrxGXyAxEdwMPEfXrz6EG+Ei/8w4cAjTPwAzzARnSlthMYainspu7Mz25ZphiDuQPEEDhmwI5Q7uHsBzQq4FABbPsG+IVjdkHhm4chm4+vjlVhPrKbQiUIPYVbAka/MyzHhx3dLkb1E7CRNTiBLt3QcZDpzD9xi247tQsfh9O1aF8amr2eOkVXXQHENlXTbi0JcTfa/aolInrz1cIoEurCYkHeGl9EkECat4v79G428TaV6Ij0jEUdce4nyNjntDJ5vkZXFGQwkT8vbzCs5zHeFq8Mq/w6EszYNWVsOk0mIeI9En/MbQHpAGFjPgP0AAAAASUVORK5CYII=")
    RED_CIRCLE_CROSS = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAYpJREFUOBGVk0tKA0EQhqtjyMozeACj8Q5ZBHIBNSKo4EZ0FQh4BheuHNwoPuNj41aIkDsYNQeYK+hKTfT7OzOTVlScgmLq9f9V1d3j7Js8mZUHZuvOrEZqKknHH2adCbODshklY6FuJERLAHcJbFBcSOPhl9yQ3D5ETYhelfMECfgWvxoC/rC7kNRF4jupcw6weKsJxpx2Hpr1grF3KOihx2gRlQwYdRVV7bYCWofulYIOLABr+X7FrM2IDereE23Mmp1T1xdYIoywRZhqOJnQ4fCR3djv8oHOJBzgG2KL5I6yQiXAOoqeIZgME9h+ZHVVnDWXYDrFZLCxQPDiD3Ec+mK9pR5g2eGgacofUow3nUXoDuvyjNk10y0oziSyHQwXuOEUsU75Ds0IGGsN8BWAeQBtcoadkpSInSkmwe78eI20uGfsE2qya8RegXwOUEtgbH+NfP2l7/HZlJ1DIq57yx8iHZsAuznAesrCjH4avWkCdfxIo/1GlOQi1QqjOr9CCNDTZv9//86fOzh2PypLeVgAAAAASUVORK5CYII=")

    ORANGE_CIRCLE = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAfElEQVQ4T2NkQAOpqanasxxmX0EXB/HTDqTqzJ49+yqyHCOMExoayrYqYPVPbBrRxcI2hLKvXr36F0gcbAApmmGGwQwBG/B/KcN/YmxGV8MYzcDIiM/PhAwFhQkjubbDDB81gIGB8jCgOBopTkhUScqkGoKRmZCTLKnZGQCX5FCXyXSbYwAAAABJRU5ErkJggg==")
    ORANGE_CIRCLE_SYNC = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAbtJREFUOBGtU00ohFEUPW8aSlEsxGq21GDBhlLKYhqspFiJhTCZ1ayoWcxCsrIQzRQb7JSs/NdkobCw8ZNsZ0XJwkZJ85z7fj5m2ChvenPfO/ec+969930KZUOvIIowJgjHOCPOXaA9xgfWVRJ3DjNG+Y3OoBKNWOI+AYWQx0usRpH7LB6RUhm8i88EcOID7nrLBJvEosQ6yvA8g/RJEHuSnFwuBq6I7eIVPdDYLwkgXHtbKJfzNck2mMYbBaMqgR0v0suoZ4IP5NR5jJwia9IWNgXzYvFqjItY5xDnupakS4rlBnLAIucspyQfEq2AUm0/bijeNmJFkcIYxed0NvO8tJrCHIPeejJtTAL4VsnpQpYxyan4i9M2CMB1t7MXxtq/iM3bI1+pmBZ52NkKY20rA5cEKAQ7jU5HOnPYE291xLXmXDOYQpfziSlIgJMAUGhh/gsszzyxe+YtATco71fTONRZDHPfGvD5On+20XpfaJpYtGdPpniIddjirDKYa6N9iTms0DHjyc7u8RGNoJpdCiFNrL3Er7HKWyVtEfm2ec18CQEYQA1OKR78RSxPOSX8//mYvp/818/5E8gChFfaQn19AAAAAElFTkSuQmCC")

    GREY_CIRCLE = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAQhJREFUOBFjZEADqamp2oyMjClAYTcgloNKPwLSu/7//z9n9uzZV6FiYIoRxgkNDWUTFBTsA/IzgZgJJo5G/wPyp79//75o9erVv0ByYANAmgUEBLYDbXZC04CVC3TJvg8fPniCDAHbBLKZWM1gW4EWQV3LwAj18yWgBC5nY3UFUPAf0CV6TNAAI1UzyFCwXpBGUGiTC9xABsCiihxD5MhxOopFIAMeoYiQxnkEMmAXaXpQVO9iAiVPoBAohZEKQNE4hwmatqeTqhuofjpILzgQQWkblDyJNQSkFqQHpJ4ZRFy7du2vsrLyCk5OTiEg1wSI4ZkMJI8EQF6dBswHcSiZCUkBA6nZGQBHemGgvqxYAAAAAABJRU5ErkJggg==")
    GREY_CIRCLE_PAUSE = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAR1JREFUOBGlUzsOgkAQ3cWEhA48AA2liZUnsCDxALRWUth6EEspsKA04QAmFB7CRA7ABaDTkAjOWxcCG2MUJllm5/PeDLs7nCni+/6Mc74ht0vLluGMdFLX9TEMw5v0CcUbw/M83bKsPdlbWlrjV3RFdpDn+S6O4xIxQQCwaZpnqrxUAB9N6uRSFMUKJKISKv8KFlWpkOyWcfnPVwq0bZdlaSBR1/U7tGrDR1JRJ3NNHlgLRiSKogcW9hDVfnuZwAKI0x4qLgiaqxpCYvdaH8IAgmwIUGIyECQjCJLx1yjfdtDtAvffvAH4VVvmBsCKQ8TbxvPsknzbIxcY5EzwSdP06TjOyTCMKZkLWu2QId4RDNOB5mDdG6ZOAvt3nF9NcH5P4R94wQAAAABJRU5ErkJggg==")
