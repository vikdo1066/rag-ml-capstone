# Acme Corp Data Handling Policy

Effective date: 1 January 2026. This policy covers all personal data and confidential business data that Acme Corp creates, receives, or processes, including data in laptops, cloud projects, tickets, chat, and backups. It applies to employees, contractors, and vendors with system access. The Data Protection Officer is reachable at privacy@acme.example.


## 1. Classification
Data has four labels, which must be set on repositories, buckets, and tickets where the tools allow it.

- Public: already published by Acme (marketing site, open-source repos marked Apache-2.0). No special handling.
- Internal: default for company operations (org charts, non-sensitive runbooks). Share only with people on an Acme account.
- Confidential: client names under NDA, unpublished architecture, HR files, production credentials. Share need-to-know only, encrypt in transit and at rest, do not put in personal email.
- Restricted: special-category personal data (health, union membership), government identifiers, full payment card numbers, production dumps with live PII. Requires a named owner, access logging, and Legal approval before any new system stores it.

If you are unsure, treat the data as Confidential.


## 2. Collection and purpose
Collect the minimum personal data needed for a documented purpose. Do not scrape personal profiles to build marketing lists. Do not reuse candidate interview notes for product research. Client data in a sandbox must be synthetic or anonymised unless the contract and a DPIA say otherwise. Production data must not be copied to laptops or to unmanaged cloud folders.

Legal bases we rely on include contract (to deliver the product), legitimate interests (security logging), and consent where we email individuals who are not client contacts. Consent must be recorded and withdrawable.


## 3. Storage and tools
Company data lives in approved systems: Google Workspace, our GitHub organization, and Google Cloud projects owned by Acme. Storing Confidential or Restricted data in personal Drive, WhatsApp, USB sticks, or consumer AI chat products is forbidden. Unapproved SaaS is shadow IT under the Expense Policy as well as this policy.

Encryption: disks of company laptops must be encrypted; GCS buckets holding Confidential data must use uniform bucket-level access and customer-managed or Google-managed encryption; secrets belong in Secret Manager, not in git, CI logs, or screenshots.

Retention: recruiting data 12 months after the role closes unless the candidate agrees to a talent pool; employee data for the duration of employment plus 7 years for payroll; production logs 90 days unless a security investigation holds them; client project data per the contract, then deletion or return within 30 days of offboarding.


## 4. Access and sharing
Access is granted by role, reviewed quarterly, and removed on the last working day. Shared passwords and long-lived personal access tokens in wikis are prohibited. External sharing of Confidential data requires a DPA and a ticket to Security. Do not add personal Gmail as an editor on company documents.

When using AI coding assistants, do not paste Restricted data, credentials, or full customer records. Public models are treated as an external recipient.


## 5. Incidents
A personal data breach or suspected unauthorised access must be reported to security@acme.example within 4 hours of discovery, including what was exposed, how many people, which systems, and whether encryption keys were involved. Do not wait for a complete investigation. Security leads containment; Legal decides whether to notify a supervisory authority. Individuals must not attempt to hide an incident to “fix it first.”

Lost devices must be reported the same day so IT can wipe them.


## 6. Subject rights and vendors
Requests for access, deletion, or objection must be sent to privacy@acme.example. Do not answer them yourself from a mailbox search. Vendors who process personal data for us need a written contract with subprocessors listed. Buying a new vendor that will see Confidential data requires Security review before the first record is sent.

Breaches of this policy are handled under the Code of Conduct. Wilful exfiltration of client data is treated as gross misconduct.
