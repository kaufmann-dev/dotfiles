---
name: vps-access
description: Get temporary, auto-expiring SSH access to the user's own Linux server or VPS without the private key leaving this machine. Use when the user wants the agent to access, inspect, or operate on their server over SSH and no working key exists yet.
---

# VPS Access

The agent creates the key pair locally and hands the user a one-liner that
contains only the public key. The user runs it on the VPS. sshd itself enforces
the expiry (`expiry-time` in `authorized_keys`), so no cleanup job is needed.

Script: `bash {skill_path}/scripts/vps-access.sh` (`--help` for details).

## Steps

1. Get the target as `user@host[:port]` from the user. Do not guess it.
2. If `~/.ssh/vps-access/<user>@<host>_<port>` already exists, run the connect
   command below with `true`. If it succeeds, skip to step 5.
3. Run `bash {skill_path}/scripts/vps-access.sh grant <target>`. Add
   `--hours N` only if the user asks for a different duration (default 24).
   Show the user the printed one-liner verbatim in a fenced code block. Tell
   them to paste it into a shell on the VPS, logged in as that user, and to
   reply once it prints `vps-access granted`.
4. Verify by running the connect command with `true`. If it fails, check the
   likely causes with the user:
   - VPS OpenSSH is older than 8.2: `expiry-time` is unsupported and the key is rejected
   - wrong user, or the one-liner was run as a different user
   - firewall or wrong port
   - `PubkeyAuthentication no` in `sshd_config`
5. Run every remote command through the connect command the script printed:

   ```bash
   ssh -i ~/.ssh/vps-access/<user>@<host>_<port> -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=accept-new -p <port> <user>@<host> '<command>'
   ```

   Never print, copy, or transmit the private key.
6. Access ends at the expiry time on its own. Already-open sessions keep
   running, but new logins are refused. If the user wants to end it early, run
   `bash {skill_path}/scripts/vps-access.sh revoke <target>`.

A new `grant` for the same VPS account replaces this machine's earlier grant.
