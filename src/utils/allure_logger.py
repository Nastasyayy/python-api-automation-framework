import json
import allure
from typing import Callable, Any


def log_allure_http(
    send_request_func: Callable,
    method: str,
    url: str,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Logs the complete absolute URL, request payload, and server response directly into Allure steps.
    """
    payload = kwargs.get("json") or kwargs.get("data") or ""
    payload_str = (
        json.dumps(payload, indent=2, ensure_ascii=False) if payload else ""
    )

    step_name = f"HTTP Request: {method.upper()} -> {url}"

    with allure.step(step_name):
        if payload_str:
            allure.attach(
                payload_str,
                name="Request Body Payload",
                attachment_type=allure.attachment_type.JSON,
            )

        response = send_request_func(method, url, *args, **kwargs)

        response_status = f"Status Code: {response.status_code}"
        try:
            response_body = json.dumps(
                response.json(), indent=2, ensure_ascii=False
            )
            attach_type = allure.attachment_type.JSON
        except (ValueError, TypeError):
            response_body = response.text
            attach_type = allure.attachment_type.TEXT

        allure.attach(
            response_status,
            name="Response Metadata",
            attachment_type=allure.attachment_type.TEXT,
        )
        if response_body:
            allure.attach(
                response_body,
                name="Response Body Content",
                attachment_type=attach_type,
            )

        return response
