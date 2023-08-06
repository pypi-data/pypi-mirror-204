/* global personalMessagesSettings */

$(function () {
    'use strict';

    const buttonReadMessage = $('button.btn-read-personal-message');

    $(buttonReadMessage).on('click', function () {
        const element = $(this);
        const sender = element.data('sender');
        const recipient = element.data('recipient');
        const message = element.data('message');
        const messageFolder = element.data('message-folder');
        const url = personalMessagesSettings.urlReadMessage;
        const csrfMiddlewareToken = personalMessagesSettings.csrfToken;

        const posting = $.post(
            url,
            {
                csrfmiddlewaretoken: csrfMiddlewareToken,
                sender: sender,
                recipient: recipient,
                message: message
            }
        );

        posting.done((data) => {
            if (undefined === data || data === '') {
                return;
            }

            const messageContainer = $('.aa-forum-personal-messages-message');

            messageContainer.html('');
            messageContainer.html(data);

            $('html, body').animate(
                {scrollTop: messageContainer.offset().top - 50}, 500
            );

            if (messageFolder === 'inbox') {
                const urlUnreadMessagesCount = personalMessagesSettings.urlUnreadMessagesCount;

                $('#aa-forum-personal-message-id-' + message)
                    .removeClass('panel-aa-forum-personal-messages-item-unread');

                $('#aa-forum-personal-message-id-' + message + ' .btn-mark-personal-message-as-read')
                    .remove();

                // Get new unread count
                const posting = $.post(
                    urlUnreadMessagesCount,
                    {
                        csrfmiddlewaretoken: csrfMiddlewareToken
                    }
                );

                posting.done((data) => {
                    if (data.unread_messages_count > 0) {
                        $('.aa-forum-badge-personal-messages-unread-count')
                            .html(data.unread_messages_count);
                    }

                    if (data.unread_messages_count === 0) {
                        $('.aa-forum-badge-personal-messages-unread-count').remove();
                    }
                });
            }
        });
    });
});
