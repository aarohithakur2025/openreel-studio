# User-owned Compute / BYOC-BYOK Model

## Goal

OpenReel should be a public **control plane**, not a public GPU bill.

- OpenReel handles planning, validation, workflow submission, job status and output handling.
- The user supplies the compute/backend.
- Generation consumption belongs to the connected provider/account according to its current quota, billing and terms.
- The project does not promise free generation and does not pool developer-owned credits for public users.

## Architecture

```
User
  |
  v
OpenReel Studio
  |
  +--> Local ComfyUI / WanGP / other compatible local backend
  |
  +--> User-controlled remote provider/API (only when verified)
  |
  +--> User-controlled GPU notebook/session
```

## Developer economics

The developer can distribute the tool without committing to a GPU bill for every user. Separate revenue channels can exist around the open-source project, such as sponsorships, donations, support, templates, or hosted convenience where the relevant upstream licenses and provider terms permit it.

**User compute credits are not developer revenue.** They are consumed by the provider that owns the account/quota.

## Required safety gates

Before adding a remote backend:

1. Verify authentication method.
2. Verify who owns the quota/credits.
3. Verify current pricing and free-tier limits.
4. Verify API/hosting/model license terms.
5. Show the user what account/backend will be charged or quota-limited.
6. Do not store provider secrets in Git.
7. Do not silently fall back to another provider.
8. Default to a dry-run/preflight when cost cannot be verified.
9. One controlled job at a time.
10. No automatic retry loops.

## Important limitation

A tool author cannot generally make an arbitrary provider charge a user's account merely because the tool is open-source. The provider must support that authentication/account model. OpenReel therefore uses a provider-adapter model rather than assuming every service works the same way.

## Monetization boundary

Potential project revenue is separate from generation consumption:

- GitHub Sponsors/donations
- paid support or implementation
- optional hosted convenience, where licenses/terms permit
- templates or extensions, where licenses permit
- commercial support for organizations

No claim of income is made until actual users/revenue exist.
