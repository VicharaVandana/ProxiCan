# Activities which are completed in versions

## POC Version

- [x] Base UDS and TP and CAN layer backend implementation
- [x] GUI for configuration window
- [x] Functionality for Configuration window basic
- [x] Basic Help Document Written
- [x] Log File functionality added for Action log, can traffic, TP log and UDS log.
- [x] Configuring window menu for UDS services selection implemented
- [x] Menu for Providing log file name and location implemented


#UDS Services Implemented
- [x] **Service 10**: Diagnostic Session Control
- [x] **Service 11**: ECU Reset
- [x] **Service 22**: Read Data by Identifier
- [x] **Service 2E**: Write Data by Identifier
- [x] **Service 27**: Security Access
- [ ] **Service 28**: Communication Control
- [ ] **Service 14**: Clear Diagnostic Information
- [ ] **Service 19**: Read DTC Information
- [ ] **Service 85**: Control DTC Setting
- [ ] **Service 23**: Read Memory by Address
- [ ] **Service 2A**: Read Scaling Data by Identifier
- [ ] **Service 2C**: Dynamically Define Data Identifier
- [ ] **Service 31**: Routine Control
- [ ] **Service 34**: Request Download
- [ ] **Service 35**: Request Upload
- [ ] **Service 36**: Transfer Data
- [ ] **Service 37**: Request Transfer Exit
- [ ] **Service 38**: Request File Transfer
- [ ] **Service 2F**: Input Output Control by Identifier
- [ ] **Service 86**: Response on Event
- [ ] **Service 83**: Access Timing Parameters

# Guide on Git branches and how to push new changes for each services
The Project is on github repository : https://github.com/VicharaVandana/ProxiCan.git 

For Each service please follow the below steps
1. Get the latest main branch from the remote to your local with below commands in git bash
    `git fetch`
    `git chechout main`
    `git pull`

2. Then create a new branch for the service you are working on with below command
    `git checkout -b <new_branch_name>`
    The format of new branch name is as foloows:
    feature_Service<SIDinhex>_<shortformofServicename>

    For example if we are working on ECU Reset then the branch name shall be `feature_Service11_EcuReset`.
    If multiple services are combined in a single branch (not advised) thenwe have to seperate the services with double underscores as shown below:
    `feature_Service22_RDBI__Service2E_WDBI`

3. Once the new branch is created. Implement the Service changes in that and then add the files to local repository and commit and push the new branch to remote repository with below steps:
    `git add *`
    `git commit -m "<Appropriate comment here>"`
    `git push origin <new_branch_name>`

4. Once the branch is pushed. Please do a self review and create a pull request from your branch to main branch and request for the review. Once the review is complete and if there are no review points then the branch would be merged with main branch and it will be part of deployment.






