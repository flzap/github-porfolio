This repository contains my work done during an internship as a Data Management Specialist with the REM. My job was to classify technical drawings for a large-scale project. 

First of all, our database could provide us with an Excel containing the document number of all the drawings in the project (around 16,000) as well as their specific drawing number. Other information is provided, but
the documentation is too often incorrect, and each drawing would have to be opened to obtain the correct information.

First, I created a macro with Power Query to perform an initial sort according to their sector (station, substation...). Next, I used Robot Process Automation (RPA)
with Power Automate Desktop to automatically download drawings from each sector according to their document number. After that, I trained an artificial intelligence with AI Builder to read the information 
directly from the drawings using Optical Character Recognition (OCR). I used it on a Power Automate workflow so that by transferring the drawings 
previously downloaded with RPA to a specified folder, an Excel file will be created containing all the information read by OCR. To make it easier for a user to use this feature,
I developed an application via Power Apps allowing drawings to be transferred and the Excel with drawing data to be obtained on the same interface. Finally, Python code was used to perform a second sort according to the data in the Excel
using the CSV library. It compares the drawings in two sectors and outputs whether any drawings contain outliers, whether there are duplicates, and which drawing types are not in one of the two sectors. 


