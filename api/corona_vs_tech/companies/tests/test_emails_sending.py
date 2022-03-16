from unittest.mock import patch

from django.core.mail import EmailMessage


def test_send_email_should_succeed(mailoutbox, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0

    email = EmailMessage(
        subject="test subject",
        body="test body",
        to=["playerzawesome@gmail.com"],
    )
    email.send()

    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "test subject"


def test_send_empty_email_should_succeed():
    # client = Client()
    with patch("django.core.mail.EmailMessage.send") as mocked_send_method:
        # response = client.post("/send-email")
        # response_content = json.loads(response.content)
        email = EmailMessage(
            subject="", body="", to=["playerzawesome@gmail.com"]
        )
        email.send()

        # self.assertEqual(response.status_code, 301)
        # self.assertEqual(response_content["status"], "Success")
        # self.assertEqual(
        #     response_content["message"], "Email was sent successfully!"
        # )
        mocked_send_method.assert_called()
