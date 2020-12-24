# What is Dumbo?

![image](https://drive.google.com/uc?export=view&id=1Fp0gYQTJMMsETRXMAL2eDla-M-OC1EIW)

Dumbo is a service based web appication that lets its user upload, store and serach through documents. Other websites can integrate the Dumbo services in their application.



## How does it work?

Dumbo stores the documents in the cloud. Tags are generated for the documents basing on their content; these tags can be used to search them. 
The user can choose to remove or add new tags, further increasing the functionality.

## Sign Up

![image](https://drive.google.com/uc?export=view&id=1gyK9PHc0tCXKr9hz9TfxVhevrTU8_Yrf)

To get started the user needs to create an accont in dumbo. 
The user can either choose to create a completely new account or can use his Google or Facebook account to create it.

## Upload

![image](https://drive.google.com/uc?export=view&id=19gsW0CP81bFJqkOxTWXsnR-3Skhx-3Fi)

To '+' in the navbar opens up a dialog box that allows the user to upload a document in the cloud. 
A document can be made public or important by checking the respective check boxes.

## OCR
Once the document is uploaded into the cloud, the documment is sent to Google Vision API which in turn uses its OCR functionality to extract the text from the document.

## NLP
The extracted text data is fed to the Google NLP API which generates the required tags for the documents.

## Search 

![image](https://drive.google.com/uc?export=view&id=17hFzH4gbgUAw5XJMEdiu9njI6F5H5efo)

The user can search for the documents using the tags and names of the documents. 

Common tags are generated based on the data from all the users in Dumbo.

![image](https://drive.google.com/uc?export=view&id=16BIJ-1lNGllEwB6HDd_6-Yud5cXsRKo7)

The user can add custom important tags for faster accessibility.

![image](https://drive.google.com/uc?export=view&id=1qIojHFH6xGRCqDUD2B6iw-LP_IiIJA-G)


## Delete

![image](https://drive.google.com/uc?export=view&id=15fRgFIWGI3z_RoiThqs5mZS-Lz0oHAif)

The users space in Dumbo is limited, so the user can delete his documents sending them in to the trash can. 
The user can even add a date auto-delete the documents.
The documents can then be deleted permanently from the trash can.
The documents can even be restored from trash.

## Profile

![image](https://drive.google.com/uc?export=view&id=1HTPJWkPSPGo8rmpze4DFCvT9pXKFkB0o)
![image](https://drive.google.com/uc?export=view&id=15_CBSEAZ11dw6NblFiZaOEZtept9Nwfu)

All the dumbo users get a dashboard. All their account details and some stastics can be seen in the profile page.
The user can even reset the password from this page (not applicable for thirdy party authenticated appplications).
Other profile related info can be modified here.

# Exposed API's
## 1. Upload from
  A service when integrated in other applications allows the users to upload documents from their dumbo profile to ther applications.

## 2. Upload to
  A service when integrated in other applications allows the users to upload documents to theri dumbo profile from other applications.

## 3. Public Document View
  A service when integrated in other applications allows the users to view all the documents in a dumbo profile using their username.
  
  

