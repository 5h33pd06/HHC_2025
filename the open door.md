# The Open Door
<img src="./images/media/image60.png"/>

<img src="./images/media/image61.png"/>
<img src="./images/media/image62.png"/>

While we’re by the hotel, we’ll stop with Lucas and do the Open Door challenge.

<img src="./images/media/image63.png"/> 

We’re at another Azure CLI challenge. This time, we’re looking for a misconfigured Network Security Group (NSG) rule allowing unrestricted access to ports like RDP or SSH.  
  
First off, we look at the <span class="mark">az group list</span> which prints out the resource groups in JSON format, and then we use <span class="mark">az group list -o table</span> which changes it into a more concise table format. This is a nice demonstration to see how different formats can be shown to more easily read data. This shows us that we have two different groups.

Next, we’ll look at what NSGs are available by using <span class="mark">az network nsg list -o table</span>

<img src="./images/media/image64.png"/>
<img src="./images/media/image65.png"/>
<img src="./images/media/image66.png"/>
This listing shows us that there are 5 different NSGs we can work with and what Resource Group they belong in. We are told to look at nsg-web-eastus from theneighborhood-rg1. If we use <span class="mark">az network nsg show --name nsg-web-eastus --resource-group theneighborhood-rg1 | less</span> then it presents us with all of the data for the NSG.  
  
Next, we are told to look at the nsg-mgmt-eastus NSG from ResourceGroup theneighborhood-rg2. We’ll use <span class="mark">az network nsg rule list --nsg-name nsg-mgmt-eastus --resource-group theneighborhood-rg2 | less</span> to view the info for this NSG.

<img src="./images/media/image67.png" />

Next, we need to look at the rest of the NSG rules and examine their properties. After we find the right one
<img src="./images/media/image68.png" />
eastus nsg-web-eastus theneighborhood-rg1

eastus nsg-db-eastus

theneighborhood-rg1

eastus nsg-dev-eastus theneighborhood-rg2

eastus nsg-mgmt-eastus theneighborhood-rg2

eastus nsg-production-eastus theneighborhood-rg1


<img src="./images/media/image69.png" />

We’ll use the same command as before to view each NSG rule. I won’t show each result here, but we’re looking for a rule that contains RDP or SSH. We find that nsg-production-eastus has a section named “Allow-RDP-From-Internet”. This can definitely cause a vulnerability issue!

We can then use <span class="mark">az network nsg rule show --name Allow-RDP-From-Internet --nsg-name nsg-production-eastus --resource-group theneighborhood-rg1 | less</span> to fully examine this rule by itself to complete our challenge.
