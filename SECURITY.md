# Security policy

Do not include Telegram API credentials, session files, channel member data,
or downloaded media in issues, pull requests, CI logs, or commits.

If you discover a security issue, use GitHub's private vulnerability reporting
feature when available, or contact the maintainer privately rather than opening
a public issue containing exploit details.

If credentials or a session file are exposed, revoke or rotate the affected
credentials or session first. Adding the filename to `.gitignore` will not
remove an already committed secret from Git history.

CI checks syntax and dependency consistency without connecting to Telegram.
These checks are not a substitute for an authenticated end-to-end test.
