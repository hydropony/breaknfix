# breaknfix

A small Django web app with intentional security flaws, designed to demonstrate common web vulnerabilities from the [OWASP Top 10 (2021)](https://owasp.org/Top10/).

## Installation

This app can be installed and run locally with [uv](https://docs.astral.sh/uv/).

1. Install uv (if you don't have it):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/hydropony/breaknfix.git
   ```
3. Navigate to the project directory:
   ```bash
   cd breaknfix
   ```
4. Install dependencies and create a virtual environment:
   ```bash
   uv sync
   ```
5. Run the server:
   ```bash
   uv run python mysite/manage.py runserver
   ```

## Flaws

### FLAW 1: Broken Access Control

**Source:** [`views.py#L108`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L108)

A user should only be able to delete posts they created. However, the delete endpoint does not verify whether the post belongs to the requesting user, and deletes the post based only on its ID. This is a [Broken Access Control](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/) vulnerability. As a result, any user can send a GET request to delete any post, which violates the intended access rules. Since the post IDs are sequential, an attacker can easily target a particular post by predicting its ID. See the [screenshots](https://github.com/hydropony/breaknfix/tree/main/screenshots/flaw-1) for the attack flow: an attacker deletes another user's content by guessing their post's ID.

**Fix:** Add a check that the post belongs to the requesting user to the filtering conditions. With this change, even if an attacker guesses the target post ID, the query will match nothing unless they own the post, and therefore the request produces no changes.
[`views.py#L114`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L114)

---

### FLAW 2: SQL Injection

**Source:** [`views.py#L82`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L82)

The new-post handler constructs a raw SQL query via an f-string. This means user input is directly inserted into the query, mixing data and executable code. The query is executed with the `executescript` function, which allows multiple statements in a single call, opening a straightforward path to [SQL injection](https://owasp.org/Top10/2021/A03_2021-Injection/). The attacker can append any statement after the INSERT that handles saving the post to the database. As a result, the vulnerability exposes unrestricted access to the application database, including modifying other people's posts, dropping tables, or reading sensitive security data. See the [screenshots](https://github.com/hydropony/breaknfix/tree/main/screenshots/flaw-2) for the attack flow; the SQL injection source code can be found in the repository ([`injection.sql`](https://github.com/hydropony/breaknfix/blob/main/injection.sql)).

**Fix:** Stop writing SQL manually for handling database interactions and switch to an ORM, e.g. Django's built-in ORM. ORMs and parameterized queries carry the data separately from the SQL code, removing the attacker's ability to inject extra statements.
[`views.py#L93`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L93)

---

### FLAW 3: Identification and Authentication Failures

**Source:** [`views.py#L31`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L31)

The current authentication flow's single credential is the username stored as plain text in a cookie. A cookie like `username=admin` is not really a secret. An attacker can easily impersonate any user by manually setting this cookie in their browser. The corresponding vulnerability category is [A07:2021 Identification and Authentication Failures](https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/). See the [screenshots](https://github.com/hydropony/breaknfix/tree/main/screenshots/flaw-3) for the attack flow.

**Fix:** Switch to Django's built-in authentication flow, which issues randomized session IDs and keeps a table in the database to map the IDs to users. On the client's side, there is only a session ID cookie that consists of random characters and is refreshed at each login, making forging it impractical.
[`views.py#L50`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L50)

Related fixes at other endpoints ensure the user is authenticated before performing actions, since currently none of the endpoints verify this.

---

### FLAW 4: Cross-Site Request Forgery (CSRF)

**Source:** [`views.py#L108`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L108)

The delete endpoint accepts the post ID as a path parameter and does not check the HTTP method. This opens up a cross-site request forgery vulnerability: a script on a malicious site can issue GET requests to the delete endpoint and remove the victim's posts. The attacker embeds an `<img>` tag pointing to the delete endpoint, and when the victim's browser loads it, the request is sent automatically. Find the CSRF script code in the repository ([`csrf.html`](https://github.com/hydropony/breaknfix/blob/main/csrf.html)); see the [screenshots](https://github.com/hydropony/breaknfix/tree/main/screenshots/flaw-4) for the attack flow.

**Fix:** Accept the post ID via form data in a POST request. Django has built-in CSRF protection middleware that protects form data from tampering by giving a CSRF token to the browser and checking for it submitted with the data.
[`views.py#L101`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/views.py#L101) | [`board.html#L32`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/templates/board.html#L32)

---

### FLAW 5: Security Misconfiguration

**Source:** [`settings.py#L26`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/settings.py#L26)

The `DEBUG` flag is enabled, causing the app to display full stack traces to users on errors. In addition, requesting a nonexistent page reveals all registered URL routes. This information helps an attacker figure out the internals of the application and reach a broader attack surface area. This corresponds to [A05:2021 Security Misconfiguration](https://owasp.org/Top10/2021/A05_2021-Security_Misconfiguration/). See the [screenshots](https://github.com/hydropony/breaknfix/tree/main/screenshots/flaw-5) for the attack flow.

**Fix:** Disable debug mode for non-developmental use. With it disabled, Django returns generic error pages and does not leak any internal exception details to users. Moreover, the stock Django admin panel may not be necessary: in that case, it should be removed from the list of active URLs, as it can be targeted by brute-force attacks. For a real deployment, secure headers, allowed hosts, and the secret key must all be configured appropriately as well.
[`settings.py#L27`](https://github.com/hydropony/breaknfix/blob/main/mysite/mysite/settings.py#L27)