https://owasp.org/Top10/2021/

- [Broken Access Control](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/)
  Covered by leaving DELETE endpoint open for anyone even though the button is missing. Done.
- [Injection](https://owasp.org/Top10/2021/A03_2021-Injection/)
  SQL injection possible in the message field -- Fixed
- https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/
  Identification only results in a token with username in it  -- Fixed, now django auth functions are used. Django gives out sessionid cookie, checks it with every request.  
- CSRF
  A script causing everyone seeing the message containing it to post their token on the website -- script done, fix done
- https://owasp.org/Top10/2021/A05_2021-Security_Misconfiguration/
  DEBUG=True

A message board application. A user can post a message, and delete it(only their own messages). An admin can delete any message.