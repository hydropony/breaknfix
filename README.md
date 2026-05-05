https://owasp.org/Top10/2021/

- [Broken Access Control](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/)
  Covered by leaving DELETE endpoint open for anyone even though the button is missing.
- [Injection](https://owasp.org/Top10/2021/A03_2021-Injection/)
  SQL injection possible in the message field
- https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/
  Session id is in the URL
- CSRF
  A script causing everyone seeing the message containing it to post their token on the website
- https://owasp.org/Top10/2021/A05_2021-Security_Misconfiguration/
  Unnecessary Django stock admin panel included

A message board application. There are users and there are admins. A user can post a message, edit it, and delete it(only their own messages). An admin can delete any message.