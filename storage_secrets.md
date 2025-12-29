# Storage Secrets
<img src="./images/media/image37.png" />
Now that we’ve completed that challenge, let’s look over at Grace and the Storage Secrets terminal.

<img src="./images/media/image39.png"/>
We are again presented with an Azure CLI environment within the “neighborhood” tenant. This time we’re just told to find where a security vulnerability exists.

<img src="./images/media/image40.png"/><img src="./images/media/image41.png" />
After it’s connected, we are presented with a helpful command to view the Azure CLI help messages. Looks like we’re in for another follow-the-prompt challenge. We are introduced to the helpful command of <span class="mark">| less</span> which lets us sroll through long results. This will definitely be useful in this challenge and others!

<img src="./images/media/image42.png"/>
We first run <span class="mark">az account show | less</span> which will display information about the currently active Azure account and subscription that our CLI session is using and returns it in a JSON format.

<img src="./images/media/image43.png"/>

<img src="./images/media/image44.png" />
Next, we run <span class="mark">az storage account list | less</span> which lists all Azure Storage Accounts we have access to in the current subscription. We are looking for the storage account with a vulnerability, and we can quickly see that “neighborhood2” is set to “allowBlobPublicAccess”: true”. This misconfiguration allows containers and blobs inside the storage account to be made publicly accessible over the internet, without authentication.

We are then told to use <span class="mark">az storage account show --name neighborhood2 | less</span> which displays all configuration and security details for the “neighborhood2” Azure Storage Account in a scrollable format so they can be easily reviewed and searched.

<img src="./images/media/image45.png" />

Our next step gives us a link to Microsoft’s page which provides some other useful options to use to list containers within neighborhood2. If we use <span class="mark">az storage container list --include-deleted --account-name neighborhood2</span> we will see that there are two containers listed: public and private. There aren’t any deleted containers here, but that could be useful in other investigations.

<img src="./images/media/image46.png" /><img src="./images/media/image47.png"/>

We are directed to next look at the blob list in the public container for neighborhood2. We can use <span class="mark">az storage blob list --container-name public --account-name neighborhood2 | less</span> to view this. We see there are three files located within, and we are next directed to download and view the blob file named admin\_credentials.txt.

Next, if we use <span class="mark">az storage blob download --account-name neighborhood2 --container-name public --name 'admin\_credentials.txt' --file /dev/stdout | less</span> then we are able to dump the entire contents of the file and get all of the secret info!
