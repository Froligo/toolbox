# Toolbox

Small tools, rules and systems from the column, each one tested and reviewed before it was shared. Each folder has its own README with how to use it, its assumptions and its limits.

- [Save a key unseen](01-save-a-key-unseen/): A hidden-input shell function that writes an API key to a locked file, then copies that file to a server without it being opened; the key never passes through chat, the screen or shell history.
- [The number check on AI writing](02-number-check/): Refuses an AI-written paragraph that contains any number not in its source data, allowing the rounding people actually do.
- [Approval fingerprint](03-approval-fingerprint/): Ties an approval to a fingerprint of the exact caption and image bytes; change one pixel and the approval no longer matches.
