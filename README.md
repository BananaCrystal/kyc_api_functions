# Banana Crystal Know Your Customer (KYC) Serverless Functions

https://codebuild.us-east-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiVnErZWNoa3RoeFBtU2hQM0FDS2pTa1hkUlo4TGZtN3hhYUtKenMrTjlOdjQyM3VjWjdkVEF5NUkzM1Y4SnNIQi9EUjR5QWxOZm0xNDd1MlZ6bUc5aGJFPSIsIml2UGFyYW1ldGVyU3BlYyI6Ijg3VnRzL3lDZytJSm5Rd3kiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master

## Functions

## AML-Check

Serverless function that checks whether a person's attribute (first name, last name, etc) is part of a sanctioned list to meet the Know Your Customer (KYC) check requirements.

## Updates to AML-CHECK

To update/refresh the list

1. Go to the  [U.S. Treasury Financial Sactions OFAC Santions List](https://home.treasury.gov/policy-issues/financial-sanctions/other-ofac-sanctions-lists)
2. Download the respective lists as follows:
   a. Complete Specially Designated Nationals List (in TEXT format) [sdnlist.txt](https://www.treasury.gov/ofac/downloads/sdnlist.txt)
   b. Consolidated Sanctions List (in CSV format) [cons_prim.csv](https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv)
3. Upload the files (sdnlist.txt and cons_prim.csv) to the s3 bucket `bananacrystal-kyc-api-aml-bucket-<env/stage>`
4. Clear the bucket/file cache


## Requirements

* Python
* Node version manager (e.g. nvm)
* Node
* [Serverless](https://www.serverless.com/framework/docs/getting-started/)

## Deployments

Merges to develop auto-deploy to dev 
Merges to master auto-deploy to production

## Environments

Configure your AWS profiles, see [Environments](https://github.com/BananaCrystal/environments)

## Continous Integration

Merges to develop auto-deploy to dev and merges to master auto-deploy to production.

```
Branches        Environment       AWS Account/Profile

develop         dev                bananacrystal-dev
master          prod               bananacrystal-prod
```
## Manual Deployments

`serverless deploy --stage <dev|prod> --profile <yourname-dev|your-name-prod>  --region <us-east-2|your-region>`

Optional: if you just need to deploy one of the function pass in the function parameter (see serverless cli for more info).




