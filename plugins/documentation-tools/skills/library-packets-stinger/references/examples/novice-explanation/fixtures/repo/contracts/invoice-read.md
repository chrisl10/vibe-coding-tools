# Invoice read contract
Status: Accepted
Revision: 2
Authenticated workspace members may read invoices only within their permitted workspace.
The server checks identity, then invoice permission, then reads invoice data.
An unauthorized caller receives no invoice contents.
No source execution or deployment is established by this contract.
