# Git-Hooks

These are the hooks which I made while working on Git Migration. Might be helpful for you too.

commit-msg: It is called whenever user commits message and verifies the required format. Here I have used bugz module to interact with bugzilla. It will check the required bug state, message length and proper format of commit message.

mailhook: It will be called as soon as user pushes the code. It is to convey set of users that this changes have been pushed by this user and so on.

Only dependency is bugz module in python which is easily available. 
pip install bugz
