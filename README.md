## DevOps-QR-Code
We should attach an IAM Role, using IRSA for the python pod to access the s3 bucket.
1. Create that role.
2. Create an SA
3. Attach that service account to the pod

## CORS
The cors issues - commented the cors middleware section. 
- Re-build the images and test in local kind.
- Push them if they are working to dockerhub.
- Remove the accesskeys as envs in yaml manifests 