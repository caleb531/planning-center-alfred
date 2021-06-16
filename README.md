# Planning Center for Alfred

*Copyright 2021 Caleb Evans*  
*Released under the MIT license*

Planning Center for Alfred is an Alfred 4 workflow designed to help churches
with various Planning Center functions, like searching for people.

## Connecting to your Planning Center account

### 1. Generate Personal Access Token

1. Visit https://api.planningcenteronline.com/oauth/applications
2. Scroll down to the _Personal Access Tokens_ section
3. Click the _Create one now_ button
4. Copy the _Application ID_ and _Secret_; save them to a safe place

Do not share the Application ID and Secret with anyone. Together, they grant
access to your entire Planning Center account, so they should be handled with
great care.

![Create one now](screenshot-create.png)
![Copy ID and Secret](screenshot-copy.png)

### 2. Enter ID and Secret into workflow

When you first import the workflow into Alfred, you'll have the opportunity to
specify the ID and Secret generated in the previous step.

![Workflow wariables](screenshot-variables.png)

## Usage

### Search for People

To search for people, use the `pcp` command. For example, `pcp caleb` will
search the people in your Planning Center account for `caleb`.
