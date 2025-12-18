# System Requirements for Mergington High School Activities API

This document outlines the functional and non-functional requirements currently fulfilled by the application.

## Functional Requirements

### Activity Viewing
- **FR1**: The system shall provide an endpoint to retrieve a list of all available extracurricular activities.
- **FR2**: Each activity shall include the following details: description, schedule, maximum number of participants, and current list of participants.
- **FR3**: The system shall serve a static web interface that displays the list of activities in a user-friendly format.

### Activity Signup
- **FR4**: The system shall provide an endpoint to allow students to sign up for an activity using their email address.
- **FR5**: The system shall validate that the activity exists before allowing signup.
- **FR6**: The system shall prevent signup if the activity is at maximum capacity.
- **FR7**: The system shall prevent duplicate signups for the same student and activity.
- **FR8**: Upon successful signup, the system shall add the student's email to the activity's participant list and return a confirmation message.
- **FR9**: The web interface shall allow users to select an activity and enter an email to sign up, displaying success or error messages accordingly.

### Activity Unregistration
- **FR10**: The system shall provide an endpoint to allow students to unregister from an activity using their email address, validating that the activity exists and the student is currently signed up.
- **FR11**: Upon successful unregistration, the system shall remove the student's email from the activity's participant list and return a confirmation message.
- **FR12**: The web interface shall display a delete icon next to each participant; clicking it shall unregister the participant from the activity and update the display.

### User Interface
- **FR13**: The web interface shall display activities as cards, showing description, schedule, available spots, and current participants (without bullet points, with delete icons).
- **FR14**: The web interface shall include a form for signing up, with fields for email and activity selection.
- **FR15**: The web interface shall update the activity list after a successful signup or unregistration to reflect changes in participants.

## Non-Functional Requirements

### Performance
- **NFR1**: The application shall handle in-memory data storage for activities, suitable for small-scale usage.
- **NFR2**: The API shall respond to requests within reasonable time limits for a development environment.

### Usability
- **NFR3**: The web interface shall be accessible via a standard web browser and provide clear feedback for user actions.

### Security
- **NFR4**: The application shall validate input data (e.g., email format, activity existence) to prevent invalid operations.
- **NFR5**: No authentication is required for viewing or signing up, as per current implementation.

### Technology Stack
- **NFR6**: The backend shall be implemented using FastAPI with Python.
- **NFR7**: The frontend shall use HTML, CSS, and JavaScript for static content.
- **NFR8**: The application shall run on a server supporting Uvicorn for deployment.