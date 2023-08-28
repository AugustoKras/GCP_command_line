##KMS and encryption Questions
 
You want data on Compute Engine disks to be encrypted at rest with keys managed by Cloud Key Management Service (KMS). Cloud Identity and Access Management (IAM) permissions to these keys must be managed in a grouped way because the permissions should be the same for all keys.
What should you do?

    A. Create a single KeyRing for all persistent disks and all Keys in this KeyRing. Manage the IAM permissions at the Key level.
    B. Create a single KeyRing for all persistent disks and all Keys in this KeyRing. Manage the IAM permissions at the KeyRing level. 
    C. Create a KeyRing per persistent disk, with each KeyRing containing a single Key. Manage the IAM permissions at the Key level.
    D. Create a KeyRing per persistent disk, with each KeyRing containing a single Key. Manage the IAM permissions at the KeyRing level.

**B. Create a single KeyRing for all persistent disks and all Keys in this KeyRing. Manage the IAM permissions at the KeyRing level.
-----------------------------------------------------------------------------------------------------

What are the steps to encrypt data using envelope encryption?
A.
✑ Generate a data encryption key (DEK) locally.
✑ Use a key encryption key (KEK) to wrap the DEK.
✑ Encrypt data with the KEK.
✑ Store the encrypted data and the wrapped KEK.
B.
✑ Generate a key encryption key (KEK) locally.
✑ Use the KEK to generate a data encryption key (DEK).
✑ Encrypt data with the DEK.
✑ Store the encrypted data and the wrapped DEK.
C.
✑ Generate a data encryption key (DEK) locally.
✑ Encrypt data with the DEK.
✑ Use a key encryption key (KEK) to wrap the DEK.
✑ Store the encrypted data and the wrapped DEK.
D.
✑ Generate a key encryption key (KEK) locally.
✑ Generate a data encryption key (DEK) locally.
✑ Encrypt data with the KEK.
Store the encrypted data and the wrapped DEK.

**C is the correct solution because KEK is never generated on the client's side, KEK is stored in GCP.
-----------------------------------------------------------------------------------------------------

Your company is storing sensitive data in Cloud Storage. You want a key generated on-premises to be used in the encryption process.
What should you do?

    A. Use the Cloud Key Management Service to manage a data encryption key (DEK).
    B. Use the Cloud Key Management Service to manage a key encryption key (KEK).
    C. Use customer-supplied encryption keys to manage the data encryption key (DEK).
    D. Use customer-supplied encryption keys to manage the key encryption key (KEK). 

 **The anwser is:C
This is a Customer-supplied encryption keys (CSEK).
We generate our own encryption key and manage it on-premises. 
A KEK never leaves Cloud KMS.There is no KEK or KMS on-premises.

Encryption at rest by default, with various key management options
https://cloud.google.com/security/encryption-at-rest
