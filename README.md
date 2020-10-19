# Banana Crystal Know Your Customer (KYC) Serverless Functions

#aml-check

Serverless function that checks whether a person's attribute (first name, last name, etc) is part of a sanctioned list to meet the Know Your Customer (KYC) check requirements.

## Requirements

* Python
* Node
* [Serverless](https://www.serverless.com/framework/docs/getting-started/)

## Updates

To update/refresh the list

1. Go to the  [U.S. Treasury Financial Sactions OFAC Santions List](https://home.treasury.gov/policy-issues/financial-sanctions/other-ofac-sanctions-lists)
2. Download the respective lists as follows:
   a. Complete Specially Designated Nationals List (in TEXT format) [sdnlist.txt](https://www.treasury.gov/ofac/downloads/sdnlist.txt)
   b. Consolidated Sanctions List (in CSV format) [cons_prim.csv](https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv)
3. Upload the files (sdnlist.txt and cons_prim.csv) to the s3 bucket `opendax-aml-bucket-<stage/env>`
4. Clear the bucket/file cache


## Deployments

Merges to develop auto-deploy to dev 
Merges to master auto-deploy to production

## Environments

Configure your AWS profiles, see [Environments](https://github.com/BananaCrystal/environments)

## Functions

### kyccheck

See (kycheck readme)[kyccheck/app/REAME.md]

## Continous Integration

Merges to develop auto-deploy to dev and merges to master auto-deploy to production.

Branches        Environment       AWS Account/Profile
develop         dev                bananacrystal-dev
master          prod               bananacrystal-prod

## Manual Deployments

1. Go to the root of the respective function (e.g. cd kyccheck/app) 
2. serverless deploy --stage <dev|prod> --profile <yourname-dev|your-name-prod>  --region <us-east-2|your-region>
