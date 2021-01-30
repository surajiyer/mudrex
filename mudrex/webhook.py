import requests
from typing import Optional, Union


def _get_kwargs(f: callable):
    def wrapper(self, **kwargs):
        self._input_kwargs = {
            k: v for k, v in kwargs.items()
            if v is not None}
        return f(self, **kwargs)
    return wrapper


class WebhookSignal(object):
    """
    Send external signals using webhook to Mudrex algorithmic bot trading platform.
    Based on https://support.mudrex.com/hc/en-us/articles/360050609631-Sending-external-signals-using-webhooks
    """
    DEFAULT_ENDPOINT = "https://mudrex.com/api/v1/signals"

    def __init__(self, signal_strategy_id: str, api_url: str = DEFAULT_ENDPOINT):
        self.signal_strategy_id = signal_strategy_id
        self.api_url = api_url

    def send(self, msg : Union[str, dict]):
        if isinstance(msg, str):
            try:
                msg = eval(msg)
            except:
                raise ValueError("`msg` must be a JSON formatted string or a dictionary.")
        if not isinstance(msg, dict):
            raise ValueError("`msg` must be a JSON formatted string or a dictionary.")
        msg = {str(k): str(v) for k, v in msg.items()}

        # Send a POST request to Mudrex webhook
        r = requests.post(
            self.api_url,
            json=msg,
            headers={"Content-Type": "application/json"})
        return r.status_code, r.reason

    @_get_kwargs
    def long_entry(
        self,
        stop_loss_exact_price: Optional[float] = None,
        stop_loss_exact_percentage: Optional[float] = None,
        stop_loss_trailing_enabled: Optional[bool] = None,
        take_profit_exact_price: Optional[float] = None,
        take_profit_exact_percentage: Optional[float] = None,
        take_profit_trailing_limit_value: Optional[float] = None,
        take_profit_trailing_enabled: Optional[bool] = None,
        reverse_short: Optional[bool] = None,
    ):
        action = (
            "reverse_short_to_long"
            if reverse_short is not None and reverse_short
            else "long_entry")
        msg = {"id": self.signal_strategy_id, "action": action}
        msg.update(self._input_kwargs)
        return self.send(msg)

    @_get_kwargs
    def short_entry(
        self,
        stop_loss_exact_price: Optional[float] = None,
        stop_loss_exact_percentage: Optional[float] = None,
        stop_loss_trailing_enabled: Optional[bool] = None,
        take_profit_exact_price: Optional[float] = None,
        take_profit_exact_percentage: Optional[float] = None,
        take_profit_trailing_limit_value: Optional[float] = None,
        take_profit_trailing_enabled: Optional[bool] = None,
        reverse_long: Optional[bool] = None,
    ):
        action = (
            "reverse_long_to_short"
            if reverse_long is not None and reverse_long
            else "short_entry")
        msg = {"id": self.signal_strategy_id, "action": "short_entry"}
        msg.update(self._input_kwargs)
        return self.send(msg)

    def long_exit(self):
        msg = {"id": self.signal_strategy_id, "action": "long_exit"}
        return self.send(msg)

    def short_exit(self):
        msg = {"id": self.signal_strategy_id, "action": "short_exit"}
        return self.send(msg)
