#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: vps-access.sh COMMAND TARGET [OPTIONS]

Grant this machine temporary SSH access to a VPS without the private key
ever leaving this machine.

TARGET is user@host or user@host:port (port defaults to 22).

Commands:
  grant TARGET [--hours N]  Create a fresh ed25519 key pair and print a one-liner
                            for the user to run on the VPS. The key is authorized
                            with an sshd-enforced expiry (default 24 hours, max 720).
  revoke TARGET             Remove this machine's grant from the VPS (best effort)
                            and delete the local key pair.
  --help                    Show this help

Keys are stored in ~/.ssh/vps-access/. The VPS needs OpenSSH 8.2 or newer.
EOF
}

die() {
    printf 'vps-access: %s\n' "$*" >&2
    exit 1
}

parse_target() {
    local target="$1"

    [[ "$target" =~ ^([A-Za-z0-9._-]+)@([A-Za-z0-9.-]+)(:([0-9]+))?$ ]] \
        || die "invalid target '$target' (expected user@host[:port])"
    user="${BASH_REMATCH[1]}"
    host="${BASH_REMATCH[2]}"
    port="${BASH_REMATCH[4]:-22}"
    (( port >= 1 && port <= 65535 )) || die "invalid port: $port"
    key="$HOME/.ssh/vps-access/${user}@${host}_${port}"
}

connect_command() {
    printf "ssh -i %q -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=accept-new -p %s %s@%s" \
        "$key" "$port" "$user" "$host"
}

agent_host="$(uname -n)"
[[ "$agent_host" =~ ^[A-Za-z0-9.-]+$ ]] || die "unsupported local hostname: $agent_host"
marker="vps-access@${agent_host}"
marker_pattern="/ ${marker//./\\.}\$/d"

grant() {
    local hours=24

    while (( $# > 0 )); do
        case "$1" in
            --hours)
                [[ -n "${2-}" ]] || die "--hours requires a value"
                hours="$2"
                shift 2
                ;;
            *)
                die "unknown option: $1"
                ;;
        esac
    done
    [[ "$hours" =~ ^[0-9]+$ ]] && (( hours >= 1 && hours <= 720 )) \
        || die "--hours must be an integer from 1 to 720"

    command -v ssh-keygen > /dev/null || die "ssh-keygen is required"

    mkdir -p "$HOME/.ssh/vps-access"
    chmod 700 "$HOME/.ssh" "$HOME/.ssh/vps-access"
    rm -f "$key" "$key.pub"
    ssh-keygen -q -t ed25519 -N "" -C "$marker" -f "$key"

    local expiry expiry_human pubkey
    expiry="$(date -u -d "+${hours} hours" +%Y%m%d%H%MZ)"
    expiry_human="$(date -u -d "+${hours} hours" '+%Y-%m-%d %H:%M')"
    pubkey="$(< "$key.pub")"

    cat <<EOF
Target:  ${user}@${host}:${port}
Expires: ${expiry_human} UTC

Run this on the VPS as ${user}:

(umask 077 && mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && sed -i '${marker_pattern}' ~/.ssh/authorized_keys && echo 'expiry-time="${expiry}",no-agent-forwarding,no-X11-forwarding ${pubkey}' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys && echo "vps-access granted until ${expiry_human} UTC")

Connect command:

$(connect_command) '<command>'
EOF
}

revoke() {
    (( $# == 0 )) || die "revoke takes no options"
    [[ -f "$key" ]] || die "no key for ${user}@${host}:${port}"

    if ssh -i "$key" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=accept-new \
        -o ConnectTimeout=10 -p "$port" "${user}@${host}" \
        "sed -i '${marker_pattern}' ~/.ssh/authorized_keys"; then
        echo "Removed grant from ${user}@${host}:${port}"
    else
        echo "Could not reach ${user}@${host}:${port} with the key (already expired or unreachable); remote entry left as is" >&2
    fi
    rm -f "$key" "$key.pub"
    echo "Deleted local key $key"
}

(( $# > 0 )) || { usage; exit 1; }
case "$1" in
    --help | -h)
        usage
        ;;
    grant | revoke)
        command="$1"
        [[ -n "${2-}" ]] || die "$command requires a target"
        parse_target "$2"
        shift 2
        "$command" "$@"
        ;;
    *)
        die "unknown command: $1"
        ;;
esac
