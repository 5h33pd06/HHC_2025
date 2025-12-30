# Owner

<img src="./images/media/image97.png"/>

<img src="./images/media/image98.jpeg" />
<img src="./images/media/image99.png"/>
<img src="./images/media/image100.png"/>

We can head over to the park and talk with James the Goose for our next challenge. We click on the terminal and we are greeted with another Azure CLI challenge. It looks like this one will have us learning some more advanced queries with conditional filtering.  
  
We start off with `az account list --query "\[\].name"` to get a list of all accounts.

<img src="./images/media/image101.png" />

Next, we’ll do some more advanced queries using conditions and assigning custom names to the fields to make things easier to identify.

<img src="./images/media/image102.png" />

We’ll use `az account list --query "\[?state=='Enabled'\].{Name:name, ID:id}"` to do a query for only accounts that are enabled, and then display the results with our custom field names of “Name” and “ID”.

<img src="./images/media/image103.png" />

Our next step is to use `az role assignment list --scope "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64" --query \[?roleDefinition=='Owner'\]` to look at the owner of the first listed subscription.

<img src="./images/media/image104.png" />

We get a message that the group present is supposed to be a PIM enabled group but that no PIM activations are present. PIM (Privileged Identity Management) in Azure is a service within Microsoft Entra ID that reduces security risks by providing **just-in-time (JIT)** and **approval-based access** to privileged roles in Azure, Microsoft Entra ID, and other services, instead of granting standing, permanent admin access. It allows users to activate elevated permissions temporarily (e.g., for a few hours), requiring justification, MFA, and approvals, thereby minimizing the attack surface and ensuring least privilege. 

<img src="./images/media/image105.png"/>

We need to look at all of the other subscriptions now. We can run that exact same command on each of the other subscriptions and check the groups. We find that there’s another group called “IT Admins” for the subscription ending in “a617”. We can use`az ad group member list --group` 
<img src="./images/media/image106.png"/>

`6b982f2f-78a0-44a8-b915-79240b2b4796 --output table | less` to see the membership of that group.

We see that this is a nested group, which is a group inside of another group. We want to go a step further into the next group and see what membership is in there. We need to look at id 6b982f2f-78a0-44a8-b915-79240b2b4796 and we can use `az ad group get-member-groups --group 6b982f2f-78a0-44a8-b915-79240b2b4796 | less` to do that.

<img src="./images/media/image107.png" />

We see that Firewall Frank has permanent Owner access instead of using PIM.

And with that, we have completed all of the Act I challenges! We can now move on to the Act II challenges that have been unlocked.
