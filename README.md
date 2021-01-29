# Mudrex
Send external webhook signals to Mudrex platform.

## Dependencies
Mudrex requires:
* Python (>=3.7)
* requests

## Usage

```
from mudrex import WebhookSignal
signal = WebhookSignal(id=..., )
signal.long_entry()  # send long entry signal
signal.long_exit()  # send signal to exit long position
signal.short_entry()  # send short entry signal
signal.short_exit()  # send signal to exit short position
```