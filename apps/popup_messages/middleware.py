# coding: utf-8
from django.template import loader
from django.template.response import TemplateResponse

from .models import PopupMessage


class CheckMessagesMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, TemplateResponse):
            _message = PopupMessage.get_message_for_url(request.path)
            if _message:
                context_data = {
                    'popup_message': _message
                }
                response.content += str(
                    loader.render_to_string(
                        'popup_messages/popup.html', context_data))
        return response
