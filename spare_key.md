# Spare Key

<img src="./images/media/image22.jpeg" />
Let’s look at Spare Key first.

<img src="./images/media/image23.png" />
We click on the terminal and are presented with our challenge.

<img src="./images/media/image24.png" />
We start off simple by doing some basic enumeration of out Azure CLI for “The Neighborhood” tenant.

This challenge starts out as a pretty simple follow-the-prompt type challenge to help us get an understanding of what’s going on.

<img src="./images/media/image25.png" />
We list the resource groups with <span class="mark">az group list -o table</span>, then find the storage accounts with <span class="mark">az storage account list –resource-group rg-the-neighborhood -o table</span>

Next, we need to find what website is present. We use <span class="mark">az storage blob service-properties show --account-name neighborhoodhoa --auth-mode login</span> to use the current Azure AD login to securely query and display the global Blob Storage configuration settings for Azure Storage Account neighborhoodhoa. We see that there is a website present here.

We next use <span class="mark">az storage container list --account-name neighborhoodhoa –auth-mode login</span> to view what containers exist within the storage account.

<img src="./images/media/image34.png" /><img src="./images/media/image35.png" />

We get $web and public as our two containers. We then need to search for what files are contained with the static website container, so we use <span class="mark">az storage blob list --account-name neighborhoodhoa --container-name '$web' --output table --auth-mode login</span> to view all of the files in a table. We see standard index.html and about.html files, however we also see iac/terraform.tfvars listed here! This isn’t something that should be left out to public view…

<img src="./images/media/image36.png" />
Our next step is to use <span class="mark">az storage blob download --account-name neighborhoodhoa --container-name '$web' --name 'iac/terraform.tfvars' --file /dev/stdout --auth-mode login | less</span> to examine this file further.

<img src="./images/media/image38.png" />
We see that this contains all of the information about the Terraform Variables for the HOA Website Deployment, including the SAS token which provides full access!
