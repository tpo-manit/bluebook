// make sure to give permission by manual exec once
// make sure to add GH_TOKEN property, make sure your token is properly scoped
const USERNAME = "tpo-manit";
const REPO = "bluebook";
const GITHUB_API_URL = `https://api.github.com/repos/${USERNAME}/${REPO}/contents/responses/`;

function onSubmit(e) {
    var form = FormApp.getActiveForm();
    var allResponses = form.getResponses();
    var latestResponse = allResponses[allResponses.length - 1];
    var response = latestResponse.getItemResponses();

    var payload = {};

    var allItems = form.getItems();

    for (var i = 0; i < allItems.length; i++) {
        var questionTitle = allItems[i].getTitle();
        var answer = null;

        var itemResponse = response.find(function(item) {
            return item.getItem().getTitle() === questionTitle;
        });

        if (itemResponse) {
          if (itemResponse.getItem().getType() === FormApp.ItemType.FILE_UPLOAD) {
              var files = itemResponse.getResponse();
              answer = files ? files.map(function(fileId) {
                  var fileUrl = `https://drive.google.com/file/d/${fileId}/view?usp=sharing`;
                  makeFilePublic(fileId);
                  return `[https://drive.google.com/file/d/${fileId}/view?usp=sharing](https://drive.google.com/file/d/${fileId}/view?usp=sharing)`;
              }) : [];
          } else {
              answer = itemResponse.getResponse();
          }
        }


        payload[questionTitle] = answer ? (Array.isArray(answer) ? answer : [answer]) : [];
    }

    var responseId = allResponses.length;
    var date = new Date().toISOString().split('T')[0];

    var fileName = `response_${responseId}-${date}.json`;

    var responseData = {
        "timestamp": new Date().toISOString(),
        "email": latestResponse.getRespondentEmail(),
        "data": payload
    };

    var fileContent = JSON.stringify(responseData, null, 2);

    var GITHUB_TOKEN = PropertiesService.getScriptProperties().getProperty("GH_TOKEN");

    createGitHubFile(fileName, fileContent, responseId, GITHUB_TOKEN);
}

function makeFilePublic(fileId) {
    var driveService = DriveApp.getFileById(fileId);
    driveService.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
}

function createGitHubFile(fileName, fileContent, responseId, GITHUB_TOKEN) {
    var url = GITHUB_API_URL + fileName;

    var payload = {
        "message": `[Webhook] Response ${responseId}: ${new Date().toISOString()}`,
        "content": Utilities.base64Encode(fileContent)
    };

    var options = {
        "method": "put",
        "headers": {
            "Authorization": "token " + GITHUB_TOKEN
        },
        "payload": JSON.stringify(payload)
    };

    try {
        var response = UrlFetchApp.fetch(url, options);
        Logger.log("File created successfully: " + fileName);
    } catch (e) {
        Logger.log("Error creating file: " + e.toString());
    }
}
